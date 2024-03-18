from pydantic import BaseModel
from enum import Enum


class Department(str, Enum):
    S = "Software"
    ML = "Machine Learning"
    QA = "Qualitative Analysis"
    R = "Research"
    D = "Data"


class CreateEmployee(BaseModel):
    name: str
    department: Department


class Employee(BaseModel):
    id: int
    name: str
    department: Department

    class Config:
        orm_mode = True
