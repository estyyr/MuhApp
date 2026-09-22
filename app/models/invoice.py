from sqlalchemy import Column, Integer, String, Numeric, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key = True)
    customer_id =  Column(Integer, ForeignKey("customers.id"), nullable = False)
    invoice_number = Column(String(50), nullable = False)
    invoice_type = Column(String(10), nullable=False)
    invoice_date = Column(Date, default=date.today)
    due_date = Column(Date)
    subtotal = Column(Numeric(12,2), default=0)
    tax_amount = Column(Numeric(12,2), default=0)
    total_amount = Column(Numeric(12, 2), default=0)
    status = Column(String(20), default = "taslak")
    notes = Column(Text)

    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key = True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    description = Column(String(200), nullable=False)
    quantity = Column(Numeric(10,2), default=1)
    unit = Column(String(20))
    unit_price= Column(Numeric(12,2),  default=0)
    tax_rate = Column(Numeric(5,2),  default=20)
    tax_amount = Column(Numeric(12,2),  default=0)
    total = Column(Numeric(12,2),  default=0)

    invoice = relationship("Invoice", back_populates="items")