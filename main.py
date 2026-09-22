from app.database import SessionLocal
from app.models.invoice import Invoice, InvoiceItem
from app.models.customer import Customer
import time
from app.models.category import Category
from app.models.payment import Payment
from app.models.transaction import Transaction


def musteri_yonetimi():
    while True:
        print("\n" + "-"*37)
        print(" "*10 +"MÜŞTERİ YÖNETİMİ"+" "*10)

        print("Geri Dönmek İçin 0'a basın")
        print("Müşteri Eklemek İçin 1'e basın")
        print("Müşteri Listesi İçin 2'e basın")
        print("Müşteri Güncelle İçin 3'e basın")
        print("Müşteri Silmek İçin 4'e basın")
        print("Detaylı Müşteri Görüntülemek İçin 5'e basın")
        print("="*30)

        secim = input("Lütfen bir işlem seçin (0-5): ")

        if secim == "0":
            print("Ana Menüye dönülüyor...")
            time.sleep(1)
            break


        elif secim == "1":
            print("YENİ MÜŞTERİ EKLE...")
            print("Menüye geri dönmek için -1'e basın:")
            firma_adi = input("Firma Adı (Zorunlu):")
            if firma_adi == "-1":
                continue
            telefon = input("Telefon Numarası: ")
            email = input("E-posta: ")
            sehir = input("Şehir: ")
            db = SessionLocal()

            yeni_musteri = Customer(company_name = firma_adi, 
                                    phone = telefon,
                                    email = email,
                                    city = sehir
            )

            db.add(yeni_musteri)
            db.commit()
            print(f"'{firma_adi}' başarıyla kaydedildi!")
            time.sleep(1)
            db.close()

        elif secim == "2":
            print("MÜŞTERİ LİSTESİ...")
            time.sleep(1)
            db = SessionLocal()
            musteri_listele(db)
            db.close()

        elif secim == "3":
            print("MÜŞTERİ GÜNCELLE...")
            time.sleep(1)
            db = SessionLocal()
            if not musteri_listele(db):
                db.close()
                continue 
            musteri_id = int(input("Güncellenecek müşteri ID:"))
            musteri = db.query(Customer).filter(Customer.id == musteri_id).first()
            if not musteri:
                time.sleep(1)
                print("Müşteri Bulunamadı!")
            else:
                yeni_ad = input("Yeni firma adı:")
                yeni_tel = input("Yeni telefon numarası:")
                yeni_email = input("Yeni E-posta adresi:")
                yeni_sehir = input("Yeni şehir:")

                if yeni_ad:
                    musteri.company_name = yeni_ad
                if yeni_tel:
                    musteri.phone = yeni_tel
                if yeni_email:
                    musteri.email = yeni_email
                if yeni_sehir:
                    musteri.city = yeni_sehir
                db.commit()
                time.sleep(1)
                print("Başarıyla Güncellendi!!")
            db.close()

        elif secim == "4":
            print("MÜŞTERİ SİL...")
            time.sleep(1)
            db = SessionLocal()
            if not musteri_listele(db):
                db.close()
                continue
            musteri_id = int(input("Silinecek müşteri ID:"))
            musteri = db.query(Customer).filter(Customer.id == musteri_id).first()
            if not musteri:
                time.sleep(2)
                print("Müşteri Bulunamadı!")
            else:
                emin_mi = input(f"'{musteri.company_name}'silinecek. Emin misiniz? (e/h):")
                if emin_mi.lower() == "e":
                    db.delete(musteri)
                    db.commit()
                    print("Silme İşlemi Başarılı")
                else:
                    time.sleep(1)
                    print("İptal edildi.")
            db.close()

        elif secim == "5":
            print("Müşteriler Detaylı Görüntüleniyor...")
            time.sleep(1)
            db = SessionLocal()
            if not musteri_listele(db):
                db.close()
                continue
            musteri_id = int(input("Detaylı görüntülemek istediğiniz müşteri ID: "))
            musteri = db.query(Customer).filter(Customer.id == musteri_id).first()
            if not musteri:
                print("Müşteri Bulunamadı!")
                time.sleep(2)
            else:
                print("\n======= MÜŞTERİ DETAY =======")
                print(f"Firma:{musteri.company_name}")
                print(f"Telefon:{musteri.phone}")
                print(f"E-posta: {musteri.email}")
                print(f"Şehir: {musteri.city}")
                print(f"Sİnce: {musteri.created_at}")
                print(f"Bakiye: {musteri.balance}")
                print("================================")

                print("\n========= FATURALAR =========")
                if musteri.invoices:
                    for f in musteri.invoices:
                        print(f"{f.invoice_number} | {f.invoice_date} | {f.total_amount}TL | {f.status}")
                else:
                    print("Henüz faturası yok.")

                print("\n========= ÖDEMELER =========")
                odemeler = db.query(Payment).filter(Payment.customer_id == musteri.id).all()
                if odemeler:
                    for p in odemeler:
                        print(f"{p.payment_date} | {p.amount} | {p.payment_type}")
                else:
                    print("Ödeme yok.")
                db.close()
        else:
            print("Geçersiz işlem yaptınız, lütfen tekrar deneyin.")
        

def kategori_yonetimi():
    while True:
        print("\n" + "-"*37)
        print(" "*10 +"KATEGORİ YÖNETİMİ" +" "*10)
        print("-"*37)
        print("Geri Dönmek İçin (0)")
        print("Yeni Kategori Eklemek İçin (1)")
        print("Kategori Listelemek İçin (2)")
        print("Kategori Güncellemek için (3)")
        print("Kategori Silmek İçin (4)")
        print("="*30)

        secim = input("Lütfen bir işlem seçin (0-4): ")

        match secim:
            case "0":
                print("Ana Menüye dönülüyor...")
                time.sleep(1)
                break
            case "1":
                print("="*10 +"YENİ KATEGORİ EKLE..."+  "="*10)
                print("Menüye geri dönmek için -1'e basın:")
                kategori_adi = input("Kategori Adı (Örn: Kira, Maaş, Satış):")
                if kategori_adi == "-1":
                    continue
                kategori_turu = input("Kategori Türü (Gelir/Gider):")
                kategori_acıklama = input("Açıklama (Opsiyonel):")
                db = SessionLocal()

                yeni_kategori = Category(name = kategori_adi,
                                         type = kategori_turu,
                                         note = kategori_acıklama,
                                        is_active = True
                )

                db.add(yeni_kategori)
                db.commit()
                print(f"'{kategori_adi}' kategorisi başarıyla kaydedildi")
                time.sleep(1)
                db.close()
            case "2":
                print("="*10 +"KATEGORİ LİSTESİ..." +  "="*10)
                time.sleep(1)
                db = SessionLocal()
                kategori_listele(db)
                db.close()
            case "3":
                print("="*10 +"KATEGORİ GÜNCELLE..." +  "="*10)
                print("-"*10 +"KATEGORİ LİSTESİ..." +  "-"*10)
                time.sleep(1)
                db = SessionLocal()
                if not kategori_listele(db):
                    db.close()
                    continue
                kategori_id = int(input("Güncellenecek kategori ID:"))
                kategori = db.query(Category).filter(Category.id == kategori_id).first()
                if not kategori:
                    time.sleep(1)
                    print("Kategori Bulunamadı!")
                else:
                    yeni_kategoriadi = input("Yeni Kategori adı:")
                    yeni_kategorituru = input("Yeni Kategori türü:")
                    yeni_acıklama = input("Yeni Açıklama:")

                    if yeni_kategoriadi:
                        kategori.name = yeni_kategoriadi
                    if yeni_kategorituru:
                        kategori.type = yeni_kategorituru
                    if yeni_acıklama:
                        kategori.note = yeni_acıklama
                    db.commit()
                    time.sleep(1)
                    print("Başarıyla Güncellendi")

            case "4":
                print("="*10 +"KATEGORİ SİL..." +  "="*10)
                db = SessionLocal()
                if not kategori_listele(db):
                    db.close()
                    continue
                kategori_id = int(input("Silinecek Kategori ID:"))
                kategori = db.query(Category).filter(Category.id == kategori_id).first()
                if not kategori:
                    time.sleep(2)
                    print("Kategori bulunamadı!")
                else:
                    emin_mi = input(f"'{kategori.name}' silinecek emin misiniz? (e/h):")
                    if emin_mi.lower() == "e":
                        db.delete(kategori)
                        db.commit()
                        print("Silme işlemi başarılı")
                    else:
                        print("İşlem iptal edildi.")

                db.close()

            case _:
                print("Geçersiz işlem yaptınız, lütfen tekrar deneyin.")

def fatura_yonetimi():
    while True:
        print("="*30)
        print("FATURA YÖNETİMİ")
        print("="*30)
        print("Ana Menüye geri dönmek için (0)")
        print("Yeni fatura kesmek için (1)")
        print("Faturaları listelemek için (2)")
        print("Fatura detay görüntülemek için (3)")
        print("Faturayı iptal et/silmek için (4)")
        print("="*30)
        secim = input("Seçiminiz (0-4):")

        match secim:
            case "0":
                print("Ana Menüye geri dönülüyor...")
                time.sleep(1)
                break
            case "1":
                print("----- YENİ FATURA OLUŞTUR -----")
                print("MÜŞTERİ LİSTESİ...")
                time.sleep(1)
                db = SessionLocal()
                musteri_listele(db)
                musterifatura_id = int(input("Kime fatura kesilecek ID (İptal için -1):"))
                if musterifatura_id == -1:
                    db.close()
                    continue
                fatura_no = input("Fatura No (Örn:FTR-001):")
                fatura_turu = input("Fatura Türü (SATIŞ/ALIŞ):")

                yeni_fatura = Invoice(
                    customer_id = musterifatura_id,
                    invoice_number = fatura_no,
                    invoice_type = fatura_turu
                )

                print("\n----- FATURA KALEMLERİ EKLENİYOR -----")
                print("Ürün/Hizmet:")

                ara_toplam = 0
                kdv_toplam = 0

                kalem_sayaci = 1
                while True:
                    aciklama = input("Açıklama (İşlemi bitirmek için boş bırakın):")
                    if aciklama == "":
                        break
                    miktar = float(input("Miktar (Adet):"))
                    birim_fiyat = float(input("Birim Fiyat (TL):"))
                    kdv_oranı_input = input("KDV Oranı (Aksi yazılmadığı sürece %20 uygulanır):")
                    if kdv_oranı_input == "":
                        kdv_oranı_input = 20.0
                    else:
                        kdv_oranı_input = float(kdv_oranı_input)
                    

                    kalem_kdv = (birim_fiyat * kdv_oranı_input * miktar) / 100
                    kalem_toplam = (birim_fiyat * miktar) + kalem_kdv

                    yeni_kalem = InvoiceItem( description = aciklama,
                                             quantity = miktar,
                                             unit_price = birim_fiyat,
                                             tax_rate = kdv_oranı_input,
                                             tax_amount = kalem_kdv,
                                             total = kalem_toplam
                    )
                    yeni_fatura.items.append(yeni_kalem)

                    ara_toplam += (miktar * birim_fiyat)
                    kdv_toplam += kalem_kdv
                    kalem_sayaci += 1

                yeni_fatura.subtotal = ara_toplam
                yeni_fatura.tax_amount = kdv_toplam
                yeni_fatura.total_amount = ara_toplam + kdv_toplam

                db.add(yeni_fatura)
                db.commit()
                print(f"{fatura_no} başarıyla kaydedildi.")

            case "2":
                print("="*10 +"FATURA LİSTESİ..." +  "="*10)
                time.sleep(1)
                db = SessionLocal()
                fatura_listele(db)
                db.close()
            case "3":
                print("Faturalar Detaylı Görüntüleniyor...")
                time.sleep(1)
                db = SessionLocal()
                if not fatura_listele(db):
                    db.close()
                    continue
                fatura_id = int(input("Detaylı görüntülemek istediğiniz fatura ID: "))
                fatura = db.query(Invoice).filter(Invoice.id == fatura_id).first()
                if not fatura:
                    print("Fatura bulunamadı!")
                    time.sleep(1)
                else:
                    print("\n======== FATURA DETAY ========")
                    print(f"Fatura No: {fatura.invoice_number}")
                    print(f"Müşteri: {fatura.customer.company_name}")
                    print(f"Tarih: {fatura.invoice_date}")
                    print(f"Durum: {fatura.status}")

                    print("----- KALEMLER -----")

                    for kalem in fatura.items:
                        print(f"{kalem.description} | {kalem.quantity} adet * {kalem.unit_price} TL | KDV: % {kalem.tax_rate} | Toplam: {kalem.total} TL")
                        print("======ÖZET======")
                        print(f"Ara Toplam: {fatura.subtotal} TL")
                        print(f"KDV: {fatura.tax_amount} TL")
                        print(f"Genel Toplam: {fatura.total_amount} TL")
                        print("="*20)

            case "4":
                print("-------FATURA SİL-------")
                print("-----FATURA LİSTESİ-----")
                db = SessionLocal()
                if not fatura_listele(db):
                    db.close()
                    continue
                fatura_id = int(input("Silmek istediğiniz fatura ID: "))
                fatura = db.query(Invoice).filter(Invoice.id == fatura_id).first()
                if not fatura:
                    print("Fatura bulunamadı!")
                    time.sleep(1)
                else:
                    emin_mi = input(f"'{fatura.invoice_number}'silinecek. Emin misiniz? (e/h):")
                    if emin_mi.lower() == "e":
                        for kalem in fatura.items:
                            db.delete(kalem)

                        db.delete(fatura)
                        db.commit()
                        print("Silme İşlemi Başarılı")
                    else:
                        print("İptal edildi.")
                        time.sleep(1)
                db.close()

            case _:
                print("Geçersiz işlem yaptınız, lütfen tekrar deneyin.")

def gg_takibi():
    while True:
        print("="*20)
        print("GELİR / GİDER TAKİBİ")
        print("="*20)
        print("Ana Menüye Dön (0)")
        print("Yeni İşlem Ekle [Gelir/Gİder] (1)")
        print("İşlem Geçmişini [Kasayı] Listele (2)")
        print("İşlem Sil/ İptal Et (3)")
        print("="*20)
        secim = input("Seçiminiz (0-3):")
        match secim:
            case "0":
                print("Ana Menüye geri dönülüyor...")
                time.sleep(1)
                break
            case "1":
                print("----- YENİ İŞLEM EKLE -----")
                db = SessionLocal()
                islem_turu = input("İşlem Türü (GELİR / GİDER):").lower()
                if islem_turu == "gider" or islem_turu == "gelir":
                    kategoriler = db.query(Category).filter(Category.type == islem_turu).all()
                    print(f"\n---- {islem_turu.upper()} KATEGORİLERİ ----")
                    if not kategoriler:
                        print(f"Henüz hiç {islem_turu} kategorisi eklememişsiniz.")
                    else:
                        for k in kategoriler:
                            print(f"ID: {k.id} | {k.name}")

                    kategori_id = int(input("\nKategori ID giriniz: (İptal için -1)"))
                    if kategori_id == -1:
                        print("İptal Edildi.")
                        time.sleep(1)
                        db.close()
                        continue
                    else:
                        tutar = float(input("Tutar (TL): "))
                        aciklama = input("Açıklama (Örn: Mutfak Masrafı):")

                        yeni_islem = Transaction(
                            type = islem_turu,
                            category_id = kategori_id,
                            amount = tutar,
                            description = aciklama
                        )
                        db.add(yeni_islem)
                        db.commit()
                        print(f"{tutar} TL değerindeki {islem_turu.upper()} işlemi kasaya işlendi.")
                        time.sleep(1)
                        db.close()
                    



            case "2":
                print(" ----- KASA İŞLEM GEÇMİŞİ ----- ")
                db = SessionLocal()
                islemler = db.query(Transaction).all()

                if not islemler:
                    print("Kasada henüz kayıtlı işlem yok.")
                else:
                    bakiye= 0
                    for islem in islemler:
                        tutar_gosterim = f"+{islem.amount}" if islem.transaction_type == "gelir" else f"{islem.amount}"

                        if islem.transaction_type == "gelir":
                            bakiye += islem.amount
                        else:
                            bakiye -= islem.amount
                            print(f"ID: {islem.id} | Tür: {islem.transaction_type.upper()} | Kategori: {islem.category.name} | Tutar:{tutar_gosterim} TL | Tarih: {islem.transaction_date}")

                    print("="*20)
                    print(f"GÜNCEL KASA BAKİYESİ {bakiye} TL")

                db.close()


            case "3":
                print("\n----- İŞLEM SİL -----")
                print(" ----- KASA İŞLEM GEÇMİŞİ ----- ")
                db = SessionLocal()
                islemler = db.query(Transaction).all()

                if not islemler:
                    print("Kasada henüz kayıtlı işlem yok.")
                    time.sleep(1)
                    db.close
                    continue

                for islem in islemler:
                    tutar_gosterim = f"+{islem.amount}" if islem.type == "gelir" else f"-{islem.amount}"

                    print(f"ID: {islem.id} | Tür:{islem.type.upper()} | Tutar: {tutar_gosterim} TL | Tarih: {islem.transaction_date}")
                
                islem_id = int(input("\nSilmek istediğiniz işlem ID (İptal için -1): "))

                if islem_id == -1:
                    print("İptal edildi!")
                    db.close()
                    continue


                islem = db.query(Transaction).filter(Transaction.id == islem_id).first()
                if not islem:
                    print("İşlem Bulunamadı!")
                else:
                    eminlik = input(f"{islem.amount} TL tutarındaki işlem silinecek. Emin misin? (e/h):")
                    if eminlik.lower() == "e":
                        db.delete(islem)
                        db.commit()
                        print("İşlem başarıyla silindi.")
                    else:
                        print("İptal edildi.")
                db.close()
                time.sleep(1)

            case _:
                print("Geçersiz!")
                time.sleep(1)


def ot_takibi():
    print(" yakında eklenecek...")

def rapor_takibi():
    print(" yakında eklenecek...")


def musteri_listele(db):
    musteriler = db.query(Customer).all()
    if not musteriler:
        print("Henüz müşteriniz yok.")
        time.sleep(2)
        return False
    for musteri in musteriler:
        print(f"ID: {musteri.id} | Firma: {musteri.company_name} | Tel: {musteri.phone} | Şehir: {musteri.city} | E-Posta: {musteri.email}")
    return True


def kategori_listele(db):
    kategoriler = db.query(Category).all()
    if not kategoriler:
        print("Henüz kategori yok.")
        return False
    for k in kategoriler:
        print(f"ID: {k.id} | {k.name} | Tür: {k.type} | Notlar: {k.note} | Aktiflik: {k.is_active}")
    return True

def fatura_listele(db):
    faturalar = db.query(Invoice).all()
    if not faturalar:
        print("Henüz fatura kesmediniz.")
        return False
    for f in faturalar:
        print(f"ID: {f.id} | Müşteri: {f.customer.company_name} | Fatura No: {f.invoice_number} | Tarih: {f.invoice_date} | Toplam. {f.total_amount} | Durum: {f.status}")
    return True


def main():
    while True:
        print("\n"+ "="*30)
        print("    ======= MuhApp ======= ")
        print("="*30)
        print("Müşteri yönetimi için (1)")
        print("Kategori yönetimi için (2)")
        print("Fatura yönetimi için (3)")
        print("Gelir/Gider takibi için (4)")
        print("Ödeme/Tahsilat takibi için (5)")
        print("Raporlar takibi (6)")
        print("Çıkış (0)")

        secim = input("Seçiminiz: ")

        match secim:
            case "0":
                print("İyi günler...")
                time.sleep(1)
                break
            case "1":
                musteri_yonetimi()
            case "2":
                kategori_yonetimi()
            case "3":
                fatura_yonetimi()
            case "4":
                gg_takibi()
            case "5":
                ot_takibi()
            case "6":
                rapor_takibi()
            case _:
                print("Geçersiz işlem!")


if __name__ == "__main__":
    main()