from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "CRUD Operation in Fast API"}


@app.get("/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


@app.get("/employees/{emp_id}", response_model=schemas.Employee)
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    db_Employee = crud.get_employee(db, emp_id=emp_id)
    if db_Employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_Employee


@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.CreateEmployee, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)


@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    deleted_employee = crud.delete_employee(db=db, emp_id=emp_id)
    if deleted_employee:
        return {"message": "Employee deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f"Employee with id {emp_id} does not exists"
    )


@app.put("/employees/{emp_id}")
def update_employee(
    emp_id: int, employee: schemas.CreateEmployee, db: Session = Depends(get_db)
):
    updated_employee = crud.update_employee(db=db, employee=employee, emp_id=emp_id)
    if updated_employee:
        return {"message": "Employee updated successfully"}
    raise HTTPException(
        status_code=404, detail=f"Employee with id {emp_id} does not exists"
    )
