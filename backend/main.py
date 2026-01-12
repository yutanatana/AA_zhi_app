import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database Setup (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class Bill(Base):
    __tablename__ = "bills"

    id = Column(String, primary_key=True, index=True)
    description = Column(String, index=True)
    total_amount = Column(Integer)  # Storing as Integer for simplicity (e.g., Yen)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class BillCreate(BaseModel):
    description: str
    total_amount: int

class BillResponse(BaseModel):
    id: str
    description: str
    total_amount: int

    class Config:
        orm_mode = True

# FastAPI App
app = FastAPI()

# CORS Setup
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:8080",  # Alternative port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/bills", response_model=BillResponse)
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    # Use UUID4 for unique, hard-to-guess IDs
    bill_id = str(uuid.uuid4())
    db_bill = Bill(id=bill_id, description=bill.description, total_amount=bill.total_amount)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

@app.get("/bills/{bill_id}", response_model=BillResponse)
def read_bill(bill_id: str, db: Session = Depends(get_db)):
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill
