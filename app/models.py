from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class EmployeeBase(BaseModel):
    name: str = Field(..., description="Employee full name")
    role: str = Field(..., description="Job role or title")
    department: str = Field(..., description="Department name")
    email: str = Field(..., description="Work email address")
    salary: float = Field(..., description="Annual salary")
    is_active: bool = Field(default=True, description="Whether employee is currently active")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    salary: Optional[float] = None
    is_active: Optional[bool] = None

class EmployeeInDB(EmployeeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class EmployeeOut(EmployeeBase):
    id: str