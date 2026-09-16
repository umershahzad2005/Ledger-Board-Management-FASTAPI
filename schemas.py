from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class VendorCreate(BaseModel):
    name: str
    vendor_trade: str


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    vendor_trade: Optional[str] = None


class VendorResponse(BaseModel):
    id: int
    name: str
    vendor_trade: str

    model_config = ConfigDict(from_attributes=True)


class VendorTransactionCreate(BaseModel):
    transaction_type: str
    amount: float
    description: Optional[str] = None


class VendorTransactionResponse(BaseModel):
    id: int
    vendor_id: int
    transaction_type: str
    amount: float
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)