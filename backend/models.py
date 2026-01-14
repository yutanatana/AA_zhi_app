from sqlalchemy import Column, String, Integer
from .database import Base

class Bill(Base):
    __tablename__ = "bills"

    id = Column(String, primary_key=True, index=True)
    description = Column(String, index=True)
    total_amount = Column(Integer)
