from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine, SessionLocal
from models import Customer, CustomerTransaction, Vendor, VendorTransaction, User, Inventory
from schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerDetailResponse,
    CustomerSaleCreate,
    CustomerSaleResponse,
    InventoryCreate,
    InventoryResponse,
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    VendorPurchaseCreate,
    VendorPurchaseResponse,
    UserCreateByAdmin,
    UserResponse,
    Token,
    VendorReportResponse,
    VendorSummaryItem,
    CustomerReportResponse,
    CustomerSummaryItem,
    InventoryReportResponse,
    InventoryItemReport,
    OverallReportResponse,
    CustomerLedgerResponse,
    VendorLedgerResponse
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_admin
)
Base.metadata.create_all(bind=engine)

# Auto-add payment columns if not present in existing SQLite database
with engine.connect() as conn:
    for tbl in ["vendor_transactions", "customer_transactions"]:
        for col, col_type in [("payment_method", "VARCHAR"), ("payment_reference", "VARCHAR")]:
            try:
                conn.execute(text(f"ALTER TABLE {tbl} ADD COLUMN {col} {col_type}"))
                conn.commit()
            except Exception:
                pass


def seed_default_admin():
    """Ensure the default admin account (admin@ledger.com / admin123) exists on startup."""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@ledger.com").first()
        if not admin:
            default_admin = User(
                name="System Admin",
                email="admin@ledger.com",
                hashed_password=hash_password("admin123"),
                role="admin",
                is_active=True
            )
            db.add(default_admin)
            db.commit()
    finally:
        db.close()


seed_default_admin()

app = FastAPI(
    title="Ledger Board - Vendor Management API"
)


@app.get("/")
def home():
    return {
        "message": "Ledger Board Vendor Management API"
    }


@app.post(
    "/admin/create-user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Admin"]
)
def create_user_by_admin(
    user_data: UserCreateByAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Admin-only endpoint to create new user credentials with admin or user role."""
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
        role=role,
        is_active=True
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

@app.post("/customers", response_model=CustomerResponse, dependencies=[Depends(get_current_user)])
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

@app.get("/customers", response_model=list[CustomerResponse], dependencies=[Depends(get_current_user)])
def get_customers(
    db: Session = Depends(get_db)):
    return db.query(Customer).all()

@app.get("/customers/{customer_id}", response_model=CustomerDetailResponse, dependencies=[Depends(get_current_user)])
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    total_purchase = 0.0
    total_paid = 0.0

    for transaction in customer.transactions:
        if transaction.transaction_type == "purchase":
            total_purchase += transaction.amount
        elif transaction.transaction_type == "payment":
            total_paid += transaction.amount

    remaining_amount = round(total_purchase - total_paid, 2)

    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "address": customer.address,
        "total_purchase": round(total_purchase, 2),
        "total_paid": round(total_paid, 2),
        "remaining_amount": remaining_amount
    }

@app.put("/customers/{customer_id}", response_model=CustomerResponse, dependencies=[Depends(get_current_user)])
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

@app.delete("/customers/{customer_id}", dependencies=[Depends(get_current_user)])
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



@app.post(
    "/customers/{customer_id}/sale",
    response_model=CustomerSaleResponse,
    dependencies=[Depends(get_current_user)]
)
def add_customer_sale(
    customer_id: int,
    sale: CustomerSaleCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if sale.no_of_units <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of units must be greater than zero"
        )

    if sale.per_unit_price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Per unit price must be greater than zero"
        )

    if sale.received_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Received amount cannot be negative"
        )

    # Find inventory item
    item = db.query(Inventory).filter(
        Inventory.product_name == sale.product_name
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Product not found in inventory"
        )

    # Check buying price
    if sale.per_unit_price < item.purchase_price:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Sale price cannot be less than buying price. "
                f"Buying price: {item.purchase_price}"
            )
        )

    # Check stock
    if item.quantity < sale.no_of_units:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock. Available quantity: {item.quantity}"
        )

    # Calculate total
    total_amount = round(
        sale.no_of_units * sale.per_unit_price,
        2
    )

    # Check received amount
    if sale.received_amount > total_amount:
        raise HTTPException(
            status_code=400,
            detail="Received amount cannot be greater than total amount"
        )

    # Validate payment method
    allowed_methods = ["cash", "card", "loan"]

    if sale.payment_method.lower() not in allowed_methods:
        raise HTTPException(
            status_code=400,
            detail="Payment method must be cash, card, or loan"
        )

    payment_method = sale.payment_method.lower()

    # Loan means nothing received
    if payment_method == "loan":
        received_amount = 0
    else:
        received_amount = sale.received_amount

    # Calculate remaining
    remaining_amount = round(
        total_amount - received_amount,
        2
    )

    # Reduce inventory
    item.quantity -= sale.no_of_units

    # ONE transaction only
    new_transaction = CustomerTransaction(
        customer_id=customer_id,
        transaction_type="sale",

        product_name=sale.product_name,
        no_of_units=sale.no_of_units,
        per_unit_price=sale.per_unit_price,

        amount=total_amount,
        received_amount=received_amount,
        remaining_amount=remaining_amount,

        payment_method=payment_method,
        payment_reference=sale.payment_reference,

        description=sale.description
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
    "customer_id": customer_id,
    "product_name": new_transaction.product_name,
    "no_of_units": new_transaction.no_of_units,
    "per_unit_price": new_transaction.per_unit_price,
    "total_amount": new_transaction.amount,
    "received_amount": new_transaction.received_amount,
    "remaining_amount": new_transaction.remaining_amount,
    "payment_method": new_transaction.payment_method,
    "message": "Sale recorded successfully"
}

@app.get("/customers/{customer_id}/ledger",response_model=CustomerLedgerResponse, dependencies=[Depends(get_current_user)])
def get_customer_ledger(customer_id: int,db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    total_purchase = 0.0
    total_paid = 0.0
    for transaction in customer.transactions:
        if transaction.transaction_type == "purchase":
            total_purchase += transaction.amount

        if transaction.payment_method in ["cash", "card"]:
            total_paid += transaction.amount

    remaining_amount = round(total_purchase - total_paid,2)

    return {
        "customer_id": customer.id,
        "customer_name": customer.name,
        "phone": customer.phone,
        "total_purchase": round(total_purchase, 2),
        "total_paid": round(total_paid, 2),
        "remaining_amount": remaining_amount,
        "transactions": customer.transactions
    }

@app.post(
    "/vendors",
    response_model=VendorResponse,
    dependencies=[Depends(get_current_user)]
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



@app.get("/vendors",response_model=list[VendorResponse], dependencies=[Depends(get_current_user)])
def get_all_vendors(db: Session = Depends(get_db)):

    vendors = db.query(Vendor).all()

    return vendors


@app.get("/vendor/{vendor_id}", dependencies=[Depends(get_current_user)])
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
    response_model=VendorResponse,
    dependencies=[Depends(get_current_user)]
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
    "/vendor/{vendor_id}",
    dependencies=[Depends(get_current_user)]
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
    "/vendor/{vendor_id}/purchase",
    response_model=VendorPurchaseResponse,
    dependencies=[Depends(get_current_user)]
)
def add_vendor_purchase(
    vendor_id: int,
    purchase: VendorPurchaseCreate,
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

    if purchase.no_of_units <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of units must be greater than zero"
        )

    if purchase.per_unit_price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Per unit price must be greater than zero"
        )

    total_amount = round(
        purchase.no_of_units * purchase.per_unit_price,
        2
    )

    if purchase.payment_method not in ["cash", "card", "loan"]:
        raise HTTPException(
            status_code=400,
            detail="Payment method must be cash, card, or loan"
        )

    if purchase.payment_method == "loan":
        paid_amount = 0
    else:
        paid_amount = purchase.paid_amount


    if paid_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Paid amount cannot be negative"
        )

    if paid_amount > total_amount:
        raise HTTPException(
            status_code=400,
            detail="Paid amount cannot be greater than total amount"
        )


    remaining_amount = round(
        total_amount - paid_amount,
        2
    )
    item = db.query(Inventory).filter(
        Inventory.product_name == purchase.product_name
    ).first()

    if item:
        # Product already exists
        item.quantity += purchase.no_of_units

        # Update purchase price
        item.purchase_price = purchase.per_unit_price

    else:
        # New product
        item = Inventory(
            product_name=purchase.product_name,
            quantity=purchase.no_of_units,
            purchase_price=purchase.per_unit_price
        )

        db.add(item)
    new_transaction = VendorTransaction(
        vendor_id=vendor_id,
        transaction_type="purchase",

        product_name=purchase.product_name,
        no_of_units=purchase.no_of_units,
        per_unit_price=purchase.per_unit_price,

        amount=total_amount,

        paid_amount=paid_amount,
        remaining_amount=remaining_amount,

        payment_method=purchase.payment_method,
        payment_reference=purchase.payment_reference,

        description=purchase.description
    )

    db.add(new_transaction)

    db.commit()
    db.refresh(new_transaction)

    return {
        "vendor_id": vendor_id,
        "product_name": new_transaction.product_name,
        "no_of_units": new_transaction.no_of_units,
        "per_unit_price": new_transaction.per_unit_price,

        "total_amount": new_transaction.amount,
        "paid_amount": new_transaction.paid_amount,
        "remaining_amount": new_transaction.remaining_amount,

        "payment_method": new_transaction.payment_method,

        "message": "Vendor purchase recorded and inventory updated successfully"
    }



@app.get("/vendors/{vendor_id}/ledger",response_model=VendorLedgerResponse, dependencies=[Depends(get_current_user)])
def get_vendor_ledger(vendor_id: int,db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found")
    total_purchase = 0.0
    total_paid = 0.0

    for transaction in vendor.transactions:
        if transaction.transaction_type == "purchase":
            total_purchase += transaction.amount
        elif transaction.transaction_type == "payment":
            total_paid += transaction.amount

    remaining_amount = round(total_purchase - total_paid,2)

    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.name,
        "contact_number": vendor.contact_number,
        "total_purchase": round(total_purchase, 2),
        "total_paid": round(total_paid, 2),
        "remaining_amount": remaining_amount,
        "transactions": vendor.transactions
    }
    
@app.get("/inventory", response_model=list[InventoryResponse], dependencies=[Depends(get_current_user)])
def get_inventory(
    db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@app.get("/inventory/{item_id}", response_model=InventoryResponse, dependencies=[Depends(get_current_user)])
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found")
    return item

@app.post("/inventory", response_model=InventoryResponse, dependencies=[Depends(get_current_user)])
def create_inventory_item(
    item: InventoryCreate,
    db: Session = Depends(get_db)):
    new_item = Inventory(
        product_name=item.product_name,
        quantity=item.quantity,
        purchase_price=item.purchase_price)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@app.put("/inventory/{item_id}", response_model=InventoryResponse, dependencies=[Depends(get_current_user)])
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
    db.commit()
    db.refresh(item)
    return item

@app.delete("/inventory/{item_id}", dependencies=[Depends(get_current_user)])
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


@app.get(
    "/reports/summary",
    response_model=OverallReportResponse,
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)
def get_overall_summary_report(db: Session = Depends(get_db)):
    # 1. Vendor Transactions (Assuming vendors might still have purchase/payment types, adjust if needed)
    v_transactions = db.query(VendorTransaction).all()
    v_purchased = sum(t.amount for t in v_transactions if t.transaction_type == "purchase")
    v_paid = sum(t.amount for t in v_transactions if t.transaction_type == "payment")
    v_balance = round(v_purchased - v_paid, 2)

    # 2. Customer Transactions (Updated based on payment methods: cash/card = paid, loan = balance)
    c_transactions = db.query(CustomerTransaction).all()
    c_purchased = sum(t.amount for t in c_transactions)
    
    # Cash or Card are instant payments
    c_paid = sum(t.amount for t in c_transactions if t.payment_method in ["cash", "card"])
    
    # Loan is the pending balance
    c_balance = sum(t.amount for t in c_transactions if t.payment_method == "loan")

    # 3. Inventory (Selling price removed, using only purchase price and quantity)
    inv_items = db.query(Inventory).all()
    inv_qty = sum(i.quantity for i in inv_items)
    inv_purchase_val = sum(i.quantity * i.purchase_price for i in inv_items)

    net_balance = round(c_balance - v_balance, 2)

    return OverallReportResponse(
        vendors={
            "total_purchased": round(v_purchased, 2),
            "total_paid": round(v_paid, 2),
            "total_payable_balance": v_balance
        },
        customers={
            "total_purchased": round(c_purchased, 2),
            "total_paid": round(c_paid, 2),
            "total_receivable_balance": round(c_balance, 2)
        },
        inventory={
            "total_products": len(inv_items),
            "total_quantity": inv_qty,
            "total_stock_cost": round(inv_purchase_val, 2)
        },
        net_receivable_payable_balance=net_balance
    )


@app.get(
    "/reports/vendors",
    response_model=VendorReportResponse,
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)
def get_vendor_report(db: Session = Depends(get_db)):
    vendors = db.query(Vendor).all()
    total_purchased = 0.0
    total_paid = 0.0
    vendor_items = []

    for vendor in vendors:
        v_purchased = sum(t.amount for t in vendor.transactions if t.transaction_type == "purchase")
        v_paid = sum(t.amount for t in vendor.transactions if t.transaction_type == "payment")
        v_balance = round(v_purchased - v_paid, 2)
        total_purchased += v_purchased
        total_paid += v_paid
        vendor_items.append(
            VendorSummaryItem(
                id=vendor.id,
                name=vendor.name,
                vendor_role=vendor.vendor_role,
                total_purchase=round(v_purchased, 2),
                total_paid=round(v_paid, 2),
                balance=v_balance
            )
        )

    return VendorReportResponse(
        total_purchased=round(total_purchased, 2),
        total_paid=round(total_paid, 2),
        total_balance=round(total_purchased - total_paid, 2),
        vendors=vendor_items
    )


@app.get(
    "/reports/customers",
    response_model=CustomerReportResponse,
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)
def get_customer_report(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    total_purchased = 0.0
    total_paid = 0.0
    customer_items = []

    for customer in customers:
        # Total purchases (all transactions sum)
        c_purchased = sum(t.amount for t in customer.transactions)
        
        # Payment methods breakdown
        c_cash = sum(t.amount for t in customer.transactions if t.payment_method == "cash")
        c_card = sum(t.amount for t in customer.transactions if t.payment_method == "card")
        c_loan = sum(t.amount for t in customer.transactions if t.payment_method == "loan")
        
        # Total paid is what they paid instantly via cash or card (excluding loan)
        c_paid = round(c_cash + c_card, 2)
        
        # Balance is whatever is left as loan/pending
        c_balance = round(c_loan, 2)
        
        total_purchased += c_purchased
        total_paid += c_paid
        
        customer_items.append(
            CustomerSummaryItem(
                id=customer.id,
                name=customer.name,
                phone=customer.phone,
                total_purchase=round(c_purchased, 2),
                total_paid=c_paid,
                total_cash=round(c_cash, 2),
                total_card=round(c_card, 2),
                total_loan=round(c_loan, 2),
                balance=c_balance
            )
        )

    return CustomerReportResponse(
        total_purchased=round(total_purchased, 2),
        total_paid=round(total_paid, 2),
        total_balance=round(total_purchased - total_paid, 2),
        customers=customer_items
    )

@app.get(
    "/reports/inventory",
    response_model=InventoryReportResponse,
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)
def get_inventory_report(db: Session = Depends(get_db)):
    inventory_items = db.query(Inventory).all()
    total_products = len(inventory_items)
    total_quantity = 0
    total_purchase_val = 0.0
    item_reports = []

    for item in inventory_items:
        cost = round(item.quantity * item.purchase_price, 2)
        total_quantity += item.quantity
        total_purchase_val += cost
        
        item_reports.append(
            InventoryItemReport(
                id=item.id,
                product_name=item.product_name,
                quantity=item.quantity,
                purchase_price=round(item.purchase_price, 2),
                total_purchase_cost=cost
            )
        )

    return InventoryReportResponse(
        total_products=total_products,
        total_quantity=total_quantity,
        total_purchase_value=round(total_purchase_val, 2),
        items=item_reports
    )


for route in app.routes:
    if isinstance(route, APIRoute):
        if route.path.startswith("/customers"):
            route.tags = ["Customers"]
        elif route.path.startswith("/vendor"):
            route.tags = ["Vendors"]
        elif route.path.startswith("/inventory"):
            route.tags = ["Inventory"]
        elif route.path.startswith("/reports"):
            route.tags = ["Reports"]