from pydantic import BaseModel, ConfigDict
class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: str
    model_config = ConfigDict(from_attributes=True)