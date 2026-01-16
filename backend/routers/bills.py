import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

import schemas
import models
from database import get_db

router = APIRouter(
    prefix="/bills",
    tags=["bills"]
)

# 割り勘の新規作成
@router.post("", response_model=schemas.Bill, status_code=status.HTTP_201_CREATED)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    # total_amountは不要になった
    bill_id = str(uuid.uuid4())
    db_bill = models.Bill(id=bill_id, description=bill.description)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

# 割り勘の詳細取得
@router.get("/{bill_id}", response_model=schemas.Bill)
def read_bill(bill_id: str, db: Session = Depends(get_db)):
    db_bill = db.query(models.Bill).options(
        joinedload(models.Bill.members),
        joinedload(models.Bill.expenses).options(
            joinedload(models.Expense.payer),
            joinedload(models.Expense.beneficiaries)
        )
    ).filter(models.Bill.id == bill_id).first()
    
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill

# メンバーを割り勘に追加
@router.post("/{bill_id}/members", response_model=schemas.Member, status_code=status.HTTP_201_CREATED)
def add_member_to_bill(bill_id: str, member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    db_member = models.Member(**member.dict(), bill_id=bill_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# メンバーリストを取得
@router.get("/{bill_id}/members", response_model=List[schemas.Member])
def get_bill_members(bill_id: str, db: Session = Depends(get_db)):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill.members

# 立替（経費）を割り勘に追加
@router.post("/{bill_id}/expenses", response_model=schemas.Expense, status_code=status.HTTP_201_CREATED)
def add_expense_to_bill(bill_id: str, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Check if payer and beneficiaries are valid members of the bill
    payer = db.query(models.Member).filter(models.Member.id == expense.payer_id, models.Member.bill_id == bill_id).first()
    if not payer:
        raise HTTPException(status_code=400, detail="Payer is not a valid member of this bill.")

    beneficiaries = db.query(models.Member).filter(
        models.Member.id.in_(expense.beneficiary_ids),
        models.Member.bill_id == bill_id
    ).all()
    
    if len(beneficiaries) != len(expense.beneficiary_ids):
        raise HTTPException(status_code=400, detail="One or more beneficiaries are not valid members of this bill.")

    db_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        bill_id=bill_id,
        payer_id=expense.payer_id
    )
    
    db_expense.beneficiaries.extend(beneficiaries)
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# 割り勘の精算
@router.get("/{bill_id}/settle", response_model=List[schemas.SettlementTransaction])
def settle_bill(bill_id: str, db: Session = Depends(get_db)):
    db_bill = read_bill(bill_id, db) # 既存の関数を利用してデータを読み込む

    if not db_bill.members:
        return []

    balances = {member.id: 0.0 for member in db_bill.members}
    member_map = {member.id: member.name for member in db_bill.members}

    # 各メンバーの貸し借りを計算
    for expense in db_bill.expenses:
        # 支払った人にはプラス
        balances[expense.payer_id] += expense.amount
        
        # 恩恵を受けた人にはマイナス
        if expense.beneficiaries:
            split_amount = expense.amount / len(expense.beneficiaries)
            for beneficiary in expense.beneficiaries:
                balances[beneficiary.id] -= split_amount

    # 債権者（プラス）と債務者（マイナス）に分ける
    creditors = {member_id: balance for member_id, balance in balances.items() if balance > 0.01}
    debtors = {member_id: balance for member_id, balance in balances.items() if balance < -0.01}

    transactions = []

    # 貪欲法で支払いを単純化
    while creditors and debtors:
        # 最も大きい債権者と債務者を見つける
        creditor_id = max(creditors, key=creditors.get)
        debtor_id = min(debtors, key=debtors.get)

        credit = creditors[creditor_id]
        debt = abs(debtors[debtor_id])

        # 送金額を決定
        transfer_amount = min(credit, debt)

        # トランザクションを作成
        transactions.append(schemas.SettlementTransaction(
            from_member_id=debtor_id,
            to_member_id=creditor_id,
            from_member_name=member_map[debtor_id],
            to_member_name=member_map[creditor_id],
            amount=round(transfer_amount, 2)
        ))

        # 残高を更新
        creditors[creditor_id] -= transfer_amount
        debtors[debtor_id] += transfer_amount

        # 残高がゼロに近くなったらリストから削除
        if creditors[creditor_id] < 0.01:
            del creditors[creditor_id]
        if abs(debtors[debtor_id]) < 0.01:
            del debtors[debtor_id]

    return transactions
