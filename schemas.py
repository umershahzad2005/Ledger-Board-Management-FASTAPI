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

class CustomerSaleCreate(BaseModel):
    product_name: str
    no_of_units: int
    per_unit_price: float
    received_amount: float = 0
    payment_method: str = "loan"
    payment_reference: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)

class CustomerSaleResponse(BaseModel):
    customer_id: int
    product_name: str
    no_of_units: int
    per_unit_price: float
    total_amount: float
    received_amount: float
    remaining_amount: float
    payment_method: str
    message: str
    model_config = ConfigDict(from_attributes=True)

class CustomerPaymentCreate(BaseModel):
    amount: float
    payment_method: str
    payment_reference: str | None = None
    description: str | None = None


class CustomerPaymentResponse(BaseModel):
    customer_id: int
    payment_amount: float
    payment_method: str
    total_paid: float
    remaining_amount: float
    message: str
    
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


class VendorPurchaseCreate(BaseModel):
    product_name: str
    no_of_units: int
    per_unit_price: float
    paid_amount: float = 0
    payment_method: str = "loan"
    payment_reference: str | None = None
    description: str | None = None

class VendorPurchaseResponse(BaseModel):
    vendor_id: int
    product_name: str
    no_of_units: int
    per_unit_price:float
    total_amount: float
    paid_amount: float
    remaining_amount: float
    payment_method: str
    message: str

class VendorPaymentCreate(BaseModel):
    amount: float
    payment_method: str
    payment_reference: str | None = None
    description: str | None = None


class VendorPaymentResponse(BaseModel):
    vendor_id: int
    payment_amount: float
    payment_method: str
    total_paid: float
    remaining_amount: float
    message: str

class UserCreateByAdmin(BaseModel):
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

class InventoryResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    purchase_price: float
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
    total_purchase_cost: float

    class Config:
        from_attributes = True

# 2. Main Report Response Schema
class InventoryReportResponse(BaseModel):
    total_products: int
    total_quantity: int
    total_purchase_value: float
    items: List[InventoryItemReport]

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