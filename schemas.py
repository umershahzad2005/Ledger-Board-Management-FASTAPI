from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal ,List

class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CustomerDetailResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: Optional[str] = None
    total_purchase: float
    total_paid: float
    remaining_amount: float

    model_config = ConfigDict(from_attributes=True)


class CustomerTransactionCreate(BaseModel):
    transaction_type: str
    product_name: Optional[str] = None
    no_of_units: Optional[float] = None
    per_unit_price: Optional[float] = None
    amount: Optional[float] = None
    description: Optional[str] = None


class CustomerTransactionResponse(BaseModel):
    id: int
    customer_id: int
    transaction_type: str
    product_name: Optional[str] = None
    no_of_units: Optional[float] = None
    per_unit_price: Optional[float] = None
    amount: float
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
      
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


# --- Report Schemas ---
class VendorSummaryItem(BaseModel):
    id: int
    name: str
    vendor_role: str
    total_purchase: float
    total_paid: float
    balance: float


class VendorReportResponse(BaseModel):
    total_purchased: float
    total_paid: float
    total_balance: float
    vendors: list[VendorSummaryItem]

class CustomerSummaryItem(BaseModel):
    id: int
    name: str
    phone: str
    total_purchase: float
    total_paid: float
    balance: float

class CustomerReportResponse(BaseModel):
    total_purchased: float
    total_paid: float
    total_balance: float
    customers: list[CustomerSummaryItem]

class InventoryItemReport(BaseModel):
    id: int
    product_name: str
    quantity: int
    purchase_price: float
    selling_price: float
    total_purchase_cost: float
    total_selling_value: float
    projected_profit: float

class InventoryReportResponse(BaseModel):
    total_products: int
    total_quantity: int
    total_purchase_value: float
    total_selling_value: float
    projected_profit: float
    items: list[InventoryItemReport]

class OverallReportResponse(BaseModel):
    vendors: dict
    customers: dict
    inventory: dict
    net_receivable_payable_balance: float

class LedgerTransactionResponse(BaseModel):
    id: int
    transaction_type: str
    product_name: Optional[str] = None
    no_of_units: Optional[int] = None
    per_unit_price: Optional[float] = None
    amount: float
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CustomerLedgerResponse(BaseModel):
    customer_id: int
    customer_name: str
    phone: Optional[str] = None
    total_purchase: float
    total_paid: float
    remaining_amount: float
    transactions: List[LedgerTransactionResponse]

class VendorLedgerResponse(BaseModel):
    vendor_id: int
    vendor_name: str
    contact_number: Optional[str] = None
    total_purchase: float
    total_paid: float
    remaining_amount: float
    transactions: List[LedgerTransactionResponse]