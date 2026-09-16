from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db,Base,engine
from models import Customer
from schemas import CustomerCreate,CustomerResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "---Welcome To Ledger System---"
    }
@app.post("/customers", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
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
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer