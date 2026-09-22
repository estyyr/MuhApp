from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key = True, autoincrement=True)
    company_name = Column(String(200), nullable = False)
    contact_name = Column(String(100))
    tax_number = Column(String(20))
    tax_office = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(50))
    balance = Column(Numeric(12,2), default = 0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    invoices = relationship("Invoice", back_populates = "customer")