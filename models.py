from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)
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


    vendor = relationship(
        "Vendor",
        back_populates="transactions"
    )
