from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import Customer
from schemas import CustomerCreate, CustomerResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.get("/")
def home():
    return {
        "message": "---Welcome To Ledger System---"
    }

@app.post("/customers", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)):
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        address=customer.address
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.get("/customers", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db)):
    return db.query(Customer).all()

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return customer

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int,customer: CustomerCreate,db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not existing_customer:
        raise HTTPException(status_code=404,detail="Customer not found")
    existing_customer.name = customer.name
    existing_customer.phone = customer.phone
    existing_customer.address = customer.address
    db.commit()
    db.refresh(existing_customer)
    return existing_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int,db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
            )
    db.delete(customer)
    db.commit()
    return {
        "message": "Customer deleted successfully"
    }