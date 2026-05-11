from sqlalchemy import Column, Integer, String, BigInteger, Enum, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"
    # ... sisa kode lainnya (id, telegram_user_id, dll)
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    telegram_user_id = Column(BigInteger, unique=True, index=True, nullable=False)
    owner_name = Column(String(100), nullable=False)
    business_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"
    # ... sisa kode lainnya
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    transaction_date = Column(DateTime, server_default=func.now())
    receipt_image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="transactions")