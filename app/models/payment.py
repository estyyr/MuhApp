from sqlalchemy import Column, Integer, String, Numeric, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    payment_type = Column(String(15), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    payment_date = Column(Date, default=date.today)
    method = Column(String(20))
    description = Column(Text)
    reference_no = Column(String(50))


    customer = relationship("Customer")
    invoice = relationship("Invoice")