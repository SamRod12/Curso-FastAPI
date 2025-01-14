from sqlmodel import Session
from db import engine
from models import Customer, Transaction

session = Session(engine)
customer = Customer(
    name="Rokardo Zukaritas",
    description="Arquitectura de software",
    email="rokardo@plai.mx",
    age=27
)

session.add(customer)
session.commit()

for x in range(200):
    session.add(Transaction(
        customer_id=customer.id,
        description=f"Test number {x}",
        ammount= 10*x
    ))

session.commit()