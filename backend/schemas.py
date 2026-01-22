from pydantic import BaseModel
from typing import List, Optional

# --- Member Schemas ---
class MemberBase(BaseModel):
    name: str

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    bill_id: str

    class Config:
        orm_mode = True

# --- Expense Schemas ---
class ExpenseBase(BaseModel):
    description: str
    amount: float

class ExpenseCreate(ExpenseBase):
    payer_id: int
    beneficiary_ids: List[int] # 経費の対象となるメンバーIDのリスト

class Expense(ExpenseBase):
    id: int
    bill_id: str
    payer_id: int
    payer: Member # 支払った人
    beneficiaries: List[Member] = [] # 恩恵を受けた人

    class Config:
        orm_mode = True

# --- Bill Schemas ---
class BillCreate(BaseModel):
    description: str

class Bill(BaseModel):
    id: str
    description: str
    members: List[Member] = []
    expenses: List[Expense] = []
    class Config:
        orm_mode = True

# --- Settlement Schemas ---
class SettlementTransaction(BaseModel):
    from_member_id: int
    to_member_id: int
    from_member_name: str
    to_member_name: str
    amount: float

