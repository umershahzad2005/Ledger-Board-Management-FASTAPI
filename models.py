from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)

    transactions = relationship(
        "CustomerTransaction",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class CustomerTransaction(Base):
    __tablename__ = "customer_transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    transaction_type = Column(String)
    product_name = Column(String)
    no_of_units = Column(Float)
    per_unit_price = Column(Float)
    amount = Column(Float)

    payment_method = Column(String)
    payment_reference = Column(String, nullable=True)

    description = Column(String)

    customer = relationship(
        "Customer",
        back_populates="transactions"
    )
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    vendor_role = Column(String, nullable=False)

    contact_number = Column(String, nullable=True)



    transactions = relationship(
        "VendorTransaction",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )


class VendorTransaction(Base):
    __tablename__ = "vendor_transactions"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id"),
        nullable=False
    )

    transaction_type = Column(
        String,
        nullable=False
    )

    product_name = Column(
        String,
        nullable=True
    )

    no_of_units = Column(
        Float,
        nullable=True
    )

    per_unit_price = Column(
        Float,
        nullable=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    description = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    payment_reference = Column(String, nullable=True)


    vendor = relationship(
        "Vendor",
        back_populates="transactions"
    )
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)