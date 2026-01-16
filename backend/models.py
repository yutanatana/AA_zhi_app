from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 中間テーブル: 経費と受益者を多対多でつなぐ
class ExpenseBeneficiary(Base):
    __tablename__ = 'expense_beneficiaries'
    expense_id = Column(Integer, ForeignKey('expenses.id'), primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'), primary_key=True)

class Bill(Base):
    __tablename__ = "bills"

    id = Column(String, primary_key=True, index=True)
    description = Column(String, index=True)
    
    # Billは複数のMemberとExpenseを持つ
    members = relationship("Member", back_populates="bill", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="bill", cascade="all, delete-orphan")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bill_id = Column(String, ForeignKey('bills.id'), nullable=False)
    
    # Memberは所属するBillを持つ
    bill = relationship("Bill", back_populates="members")
    # Memberが支払ったExpenseのリスト
    paid_expenses = relationship("Expense", back_populates="payer")
    # Memberが受益者となっているExpenseのリスト
    benefited_expenses = relationship(
        "Expense",
        secondary='expense_beneficiaries',
        back_populates='beneficiaries'
    )

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)
    
    bill_id = Column(String, ForeignKey('bills.id'), nullable=False)
    payer_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    
    # Expenseは所属するBillを持つ
    bill = relationship("Bill", back_populates="expenses")
    # Expenseを支払ったMember
    payer = relationship("Member", back_populates="paid_expenses")
    # Expenseの受益者であるMemberのリスト
    beneficiaries = relationship(
        "Member",
        secondary='expense_beneficiaries',
        back_populates='benefited_expenses'
    )
