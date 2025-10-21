from flask import Flask, jsonify, request, abor     
from pymongo import MongoClient
from app.common import db as db_conf
from bson import ObjectId

app = Flask(__name__)


client = MongoClient(db_conf.MONGODB_URI)
database = client[db_conf.DB_NAME]
employees = database.employees


def doc_to_out(doc):
    return {"id": str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"}}


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json() or {}
    if "name" not in data:
        abort(400, "name required")
    res = employees.insert_one(data)
    doc = employees.find_one({"_id": res.inserted_id})
    return jsonify(doc_to_out(doc)), 201


@app.route("/employees/<emp_id>")
def get_employee(emp_id):
    if not ObjectId.is_valid(emp_id):
        abort(400, "invalid id")
    doc = employees.find_one({"_id": ObjectId(emp_id)})
    if not doc:
        abort(404)
    return jsonify(doc_to_out(doc))


@app.route("/employees")
def list_employees():
    out = [doc_to_out(d) for d in employees.find()]
    return jsonify(out)


@app.route("/employees/<emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    if not ObjectId.is_valid(emp_id):
        abort(400, "invalid id")
    res = employees.delete_one({"_id": ObjectId(emp_id)})
    if res.deleted_count == 0:
        abort(404)
    return jsonify({"deleted": emp_id})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
