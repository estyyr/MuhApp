from sqlalchemy import Column, Integer, String, Numeric, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id")) 
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    type = Column(String(10), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    transaction_date = Column(Date, default=date.today)
    description = Column(Text)
    reference_no = Column(String(50))

    customer = relationship("Customer")
    invoice = relationship("Invoice")
    category = relationship("Category")