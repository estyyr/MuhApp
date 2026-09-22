from app.database import engine, Base

print("Modeller yükleniyor...")
from app.models.user import User
print("✅ User")
from app.models.customer import Customer
print("✅ Customer")
from app.models.category import Category
print("✅ Category")
from app.models.invoice import Invoice, InvoiceItem
print("✅ Invoice")
from app.models.transaction import Transaction
print("✅ Transaction")
from app.models.payment import Payment
print("✅ Payment")

print("Veritabanı oluşturuluyor...")
Base.metadata.create_all(bind=engine)
print("Tamamdı!")