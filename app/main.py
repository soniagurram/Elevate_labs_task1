from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.database import MONGODB_URI, DB_NAME
from bson import ObjectId
from typing import List

app = FastAPI(title="Company API")
origins = [
    "http://localhost:5000",  # your frontend origin
    "http://localhost:5001",  # if you run frontend on another port
    "*",  # optional, allow all origins (use with caution in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # can be ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],    # allow all HTTP methods
    allow_headers=["*"], 
)
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URI)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.post("/employees/", response_model=EmployeeOut)
async def create_employee(employee: EmployeeCreate):
    """Create a new employee"""
    employee_dict = employee.dict()
    result = await app.mongodb["employees"].insert_one(employee_dict)
    created_employee = await app.mongodb["employees"].find_one(
        {"_id": result.inserted_id}
    )
    return {**created_employee, "id": str(created_employee["_id"])}

@app.get("/employees/", response_model=List[EmployeeOut])
async def list_employees():
    """List all employees"""
    employees = []
    async for employee in app.mongodb["employees"].find():
        employees.append({**employee, "id": str(employee["_id"])})
    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeOut)
async def get_employee(employee_id: str):
    """Get a single employee by ID"""
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID")
    
    if (employee := await app.mongodb["employees"].find_one({"_id": ObjectId(employee_id)})) is not None:
        return {**employee, "id": str(employee["_id"])}
    
    raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")

@app.put("/employees/{employee_id}", response_model=EmployeeOut)
async def update_employee(employee_id: str, employee_data: EmployeeUpdate):
    """Update an employee"""
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID")

    update_result = await app.mongodb["employees"].update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": employee_data.dict(exclude_unset=True)}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")

    if (updated_employee := await app.mongodb["employees"].find_one({"_id": ObjectId(employee_id)})) is not None:
        return {**updated_employee, "id": str(updated_employee["_id"])}

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    """Delete an employee"""
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID")
        
    delete_result = await app.mongodb["employees"].delete_one({"_id": ObjectId(employee_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
        
    return {"status": "success", "message": f"Employee {employee_id} deleted"}
