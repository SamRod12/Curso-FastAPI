from fastapi import FastAPI, HTTPException, status, APIRouter, Query
from datetime import datetime
import zoneinfo
from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/customers", response_model=Customer , status_code=status.HTTP_201_CREATED, tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers", response_model=list[Customer], tags=['customers'])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}", response_model=Customer, tags=['customers'])
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exists")
    return customer

@router.delete("/customers/{customer_id}", tags=['customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exists")
    session.delete(customer)
    session.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/customers/{customer_id}",response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['customers'])
async def update_customer(customer_id: int ,customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn´t exists")
    
    update_data = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(update_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return  customer

@router.post("/customers/{customer_id}/plans/{plan_id}", status_code=status.HTTP_201_CREATED, tags=['customers'])
async def subscribe_customer_to_plan(customer_id:int, plan_id:int, session: SessionDep, plan_status : StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The customer or plan doesn´t exists")
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get("/customers/{customer_id}/plans", tags=['customers'])
async def list_customer_plans(customer_id:int, session: SessionDep, plan_status: StatusEnum = Query(None)):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where(CustomerPlan.status == plan_status)
    if not plan_status:
        query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id)
    
    plans = session.exec(query).all()
    return plans