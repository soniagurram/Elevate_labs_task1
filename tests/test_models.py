# from app.models import EmployeeCreate, EmployeeOut


# def test_employee_model():
#     data = {"name": "Bob", "role": "Manager"}
#     emp = EmployeeCreate(**data)
#     out = EmployeeOut(id="123", **data)
#     assert out.name == "Bob"


from app.models import EmployeeCreate, EmployeeOut


def test_employee_model():
    data = {
        "name": "Bob",
        "role": "Manager",
        "department": "devops2",
        "email": "Bob@gmail.com",
        "salary": 50000,
        "is_active": True
    }
    emp = EmployeeCreate(**data)
    out = EmployeeOut(id="123", **data)
    assert out.name == "Bob"

