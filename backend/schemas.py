from pydantic import BaseModel

class BillCreate(BaseModel):
    description: str
    total_amount: int

class BillResponse(BaseModel):
    id: str
    description: str
    total_amount: int

    class Config:
        orm_mode = True
