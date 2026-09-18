from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal

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


class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[Literal["admin", "user"]] = "user"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal

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


class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[Literal["admin", "user"]] = "user"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class InventoryCreate(BaseModel):
    product_name: str
    quantity: int
    purchase_price: float
    selling_price: float

class InventoryResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    purchase_price: float
    selling_price: float
    model_config = ConfigDict(from_attributes=True)