from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import Customer, Vendor, VendorTransaction, User,Inventory
from schemas import CustomerCreate, CustomerResponse,InventoryCreate,InventoryResponse
from schemas import (
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    VendorTransactionCreate,
    VendorTransactionResponse,
    UserRegister,
    UserResponse,
    Token
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    require_admin
)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ledger Board - Vendor Management API"
)

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
@app.get("/")
def home():
    return {
        "message": "Ledger Board Vendor Management API"
    }

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"]
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    role = user_data.role if user_data.role in ["admin", "user"] else "user"

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.post(
    "/login",
    response_model=Token,
    tags=["Authentication"]
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint — supports Swagger Authorize button directly.
    In the 'username' field, enter your **email address**.
    Leave client_id and client_secret blank.
    """
    # OAuth2PasswordRequestForm uses 'username' field — we treat it as email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "user_id": user.id}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }


@app.get(
    "/admin/users",
    response_model=list[UserResponse],
    tags=["Admin"]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(User).all()


@app.post(
    "/vendors",
    response_model=VendorResponse
)
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):

    new_vendor = Vendor(
        name=vendor.name,
        vendor_role=vendor.vendor_role,
        contact_number=vendor.contact_number
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor



@app.get("/vendors",response_model=list[VendorResponse])
def get_all_vendors(db: Session = Depends(get_db)):

    vendors = db.query(Vendor).all()

    return vendors


@app.get("/vendor/{vendor_id}")
def get_vendor(vendor_id: int,db: Session = Depends(get_db)):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    total_purchase = 0
    total_paid = 0

    for transaction in vendor.transactions:

        if transaction.transaction_type == "purchase":
            total_purchase += transaction.amount

        elif transaction.transaction_type == "payment":
            total_paid += transaction.amount

    remaining_amount = total_purchase - total_paid

    return {
        "id": vendor.id,
        "name": vendor.name,
        "vendor_role": vendor.vendor_role,
        "contact_number": vendor.contact_number,
        "total_purchase": total_purchase,
        "total_paid": total_paid,
        "remaining_amount": remaining_amount,
        "created_at": getattr(vendor, "created_at", None)
    }


@app.put(
    "/vendor/{vendor_id}",
    response_model=VendorResponse
)
def update_vendor(
    vendor_id: int,
    vendor_data: VendorUpdate,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    if vendor_data.name is not None:
        vendor.name = vendor_data.name

    if vendor_data.vendor_role is not None:
        vendor.vendor_role = vendor_data.vendor_role

    if vendor_data.contact_number is not None:
        vendor.contact_number = vendor_data.contact_number

    db.commit()
    db.refresh(vendor)

    return vendor


@app.delete(
    "/vendor/{vendor_id}"
)
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    db.delete(vendor)
    db.commit()

    return {
        "message": "Vendor deleted successfully",
        "vendor_id": vendor_id
    }


@app.post(
    "/vendor/{vendor_id}/transactions",
    response_model=VendorTransactionResponse
)
def add_vendor_transaction(
    vendor_id: int,
    transaction: VendorTransactionCreate,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    if transaction.transaction_type not in [
        "purchase",
        "payment"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Transaction type must be purchase or payment"
        )

    if transaction.amount is not None:
        amount = transaction.amount
    elif transaction.no_of_units is not None and transaction.per_unit_price is not None:
        amount = round(transaction.no_of_units * transaction.per_unit_price, 2)
    else:
        raise HTTPException(
            status_code=400,
            detail="Must provide either 'amount' or both 'no_of_units' and 'per_unit_price'"
        )

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    new_transaction = VendorTransaction(
        vendor_id=vendor_id,
        transaction_type=transaction.transaction_type,
        product_name=transaction.product_name,
        no_of_units=transaction.no_of_units,
        per_unit_price=transaction.per_unit_price,
        amount=amount,
        description=transaction.description
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@app.get(
    "/vendor/{vendor_id}/transactions",
    response_model=list[VendorTransactionResponse]
)
def get_vendor_transactions(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    transactions = db.query(
        VendorTransaction
    ).filter(
        VendorTransaction.vendor_id == vendor_id
    ).all()

    return transactions

    
@app.get("/inventory", response_model=list[InventoryResponse])
def get_inventory(
    db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@app.get("/inventory/{item_id}", response_model=InventoryResponse)
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found")
    return item

@app.post("/inventory", response_model=InventoryResponse)
def create_inventory_item(
    item: InventoryCreate,
    db: Session = Depends(get_db)):
    new_item = Inventory(
        product_name=item.product_name,
        quantity=item.quantity,
        purchase_price=item.purchase_price,
        selling_price=round(item.purchase_price * 1.10, 2))

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@app.get("/inventory/transaction/{transaction_id}",response_model=InventoryResponse)
def add_transaction_to_inventory(
    transaction_id: int,
    db: Session = Depends(get_db)):

    transaction = db.query(VendorTransaction).filter(VendorTransaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Vendor transaction not found"
        )
    if transaction.transaction_type != "purchase":
        raise HTTPException(
            status_code=400,
            detail="Only purchase transaction can be added to inventory"
        )
    if (
        not transaction.product_name
        or not transaction.no_of_units
        or not transaction.per_unit_price):
        raise HTTPException(
            status_code=400,
            detail="Transaction does not have product details"
        )
    item = db.query(Inventory).filter(Inventory.product_name == transaction.product_name).first()
    selling_price = round(
        transaction.per_unit_price * 1.10,
        2)

    if item:
        item.quantity += int(transaction.no_of_units)
        item.purchase_price = transaction.per_unit_price
        item.selling_price = selling_price
    else:
        item = Inventory(
            product_name=transaction.product_name,
            quantity=int(transaction.no_of_units),
            purchase_price=transaction.per_unit_price,
            selling_price=selling_price)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item
        
@app.put("/inventory/{item_id}", response_model=InventoryResponse)
def update_inventory_item(item_id: int,item_data: InventoryCreate,
    db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )
    item.product_name = item_data.product_name
    item.quantity = item_data.quantity
    item.purchase_price = item_data.purchase_price
    item.selling_price = item_data.selling_price
    db.commit()
    db.refresh(item)
    return item

@app.delete("/inventory/{item_id}")
def delete_inventory_item(item_id: int,db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )
    db.delete(item)
    db.commit()
    return {
        "message": "Inventory item deleted successfully"
    }
for route in app.routes:
    if isinstance(route, APIRoute):
        if route.path.startswith("/customers"):
            route.tags = ["Customers"]
        elif route.path.startswith("/vendor"):
            route.tags = ["Vendors"]
        elif route.path.startswith("/inventory"):
            route.tags = ["Inventory"]