from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: str
      
class VendorCreate(BaseModel):
    name: str
    vendor_role: str
    contact_number: Optional[str] = None


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    vendor_role: Optional[str] = None
    contact_number: Optional[str] = None


class VendorResponse(BaseModel):
    id: int
    name: str
    vendor_role: str
    contact_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VendorTransactionCreate(BaseModel):
    transaction_type: str
    product_name: Optional[str] = None
    no_of_units: Optional[float] = None
    per_unit_price: Optional[float] = None
    amount: Optional[float] = None
    description: Optional[str] = None


class VendorTransactionResponse(BaseModel):
    id: int
    vendor_id: int
    transaction_type: str
    product_name: Optional[str] = None
    no_of_units: Optional[float] = None
    per_unit_price: Optional[float] = None
    amount: float
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)