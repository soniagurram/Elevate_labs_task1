from app.models import EmployeeCreate, EmployeeOut


def test_employee_model():
    data = {"name": "Bob", "role": "Manager"}
    emp = EmployeeCreate(**data)
    out = EmployeeOut(id="123", **data)
    assert out.name == "Bob"
