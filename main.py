from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Vendor, VendorTransaction

from schemas import (
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    VendorTransactionCreate,
    VendorTransactionResponse
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Ledger Board - Vendor Management API"
)


@app.get("/")
def home():
    return {
        "message": "Ledger Board Vendor Management API"
    }


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
        vendor_trade=vendor.vendor_trade
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
        "vendor_trade": vendor.vendor_trade,
        "total_purchase": total_purchase,
        "total_paid": total_paid,
        "remaining_amount": remaining_amount,
        "created_at": vendor.created_at
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

    if vendor_data.vendor_trade is not None:
        vendor.vendor_trade = vendor_data.vendor_trade

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

    if transaction.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    new_transaction = VendorTransaction(
        vendor_id=vendor_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
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