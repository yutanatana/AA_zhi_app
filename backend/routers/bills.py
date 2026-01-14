import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/bills",
    tags=["bills"]
)

@router.post("", response_model=schemas.BillResponse)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    bill_id = str(uuid.uuid4())
    db_bill = models.Bill(id=bill_id, description=bill.description, total_amount=bill.total_amount)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@router.get("/{bill_id}", response_model=schemas.BillResponse)
def read_bill(bill_id: str, db: Session = Depends(get_db)):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill
