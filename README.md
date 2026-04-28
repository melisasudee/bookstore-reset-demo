# Kitabevi Demo Sistemi  
## Veri Temizleme ve Güvenli Reset Mekanizması

Bu proje, bozuk verileri tespit edip sistemi güvenli şekilde temiz veri setine döndüren bir demo uygulamasıdır.

---

## İçindekiler

- [Proje Amacı](#proje-amacı)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Mimari Yaklaşım](#mimari-yaklaşım-solid-prensipleri)
- [Dashboard Özellikleri](#dashboard-özellikleri)
- [Test Modu](#test-modu-bozuk-veri-üretimi)
- [Bozuk Veri Tespiti](#bozuk-veri-tespiti)
- [Reset Mekanizması](#reset-mekanizması-güvenlik)
- [Reset İşlemi](#reset-işlemi)
- [Reset Tetikleme](#reset-tetikleme-yöntemleri)
- [Demo Senaryosu](#demo-senaryosu)
- [Kurulum](#kurulum-ve-çalıştırma)
- [Not](#not)
- [Geliştirici](#geliştirici)

---

## Proje Amacı

Bu projenin amacı, bir online kitap satış sistemi üzerinde oluşabilecek bozuk (kirli) verileri tespit etmek, bu verileri analiz edilebilir hale getirmek ve sistemi güvenli bir şekilde temiz (golden) veri setine döndürmektir.

Proje, özellikle şu senaryoyu ele alır:

> Sistem hatalı verilerle bozulduğunda, kontrollü ve güvenli bir mekanizma ile tekrar kullanılabilir hale getirilebilir mi?

---

## Kullanılan Teknolojiler

- Python  
- Django Web Framework  
- SQLite (veritabanı)  
- Django Admin Panel  
- JSON Fixture (golden veri seti)  

---

## Mimari Yaklaşım (SOLID Prensipleri)

Proje, sürdürülebilir ve genişletilebilir bir yapı oluşturmak amacıyla SOLID prensiplerine uygun olarak tasarlanmıştır.

### Katmanlar:

- `data_validation` → Veri doğrulama ve bozuk veri tespiti  
- `junk_data` → Test amacıyla bozuk veri üretimi  
- `backup` → Reset öncesi veri yedekleme  
- `reset` → Sistem sıfırlama ve veri yeniden yükleme  

Her modül tek bir sorumluluğa sahiptir (Single Responsibility Principle).

---

## Dashboard Özellikleri

Dashboard, sistemin hem işlevsel hem de veri sağlığı durumunu gösterir:

- Kitap listesi (isim, fiyat, stok)  
- Toplam satış / gelir bilgisi  
- Bozuk veri sayacı (kritik gösterge)  

### Örnek:

- `Bozuk Veri: 12` → Sistem kirlenmiş  
- `Bozuk Veri: 0` → Sistem sağlıklı  

Bu gösterge, reset işleminin etkisini doğrudan görünür kılar.

---

## Test Modu (Bozuk Veri Üretimi)

Sistem, gerçek hayattaki veri hatalarını simüle etmek amacıyla rastgele bozuk veri üretimi yapabilir.

Üretilen bozuk veri türleri:

- Eksik alanlar (title, author, price)  
- Negatif fiyat ve stok değerleri  
- Aşırı yüksek (anlamsız) fiyatlar  
- Geçersiz görsel URL’leri  
- Kopya kayıtlar  
- Format hataları  

Amaç:

> Sistemin bilinçli olarak bozulması ve reset mekanizmasının test edilmesi

---

## Bozuk Veri Tespiti

Sistem aşağıdaki durumları bozuk veri olarak değerlendirir:

- Zorunlu alanların boş olması  
- Negatif veya mantıksız sayısal değerler  
- Geçersiz veri formatları (örneğin URL)  
- Tutarsız veya eksik veri ilişkileri  

Bu kontroller backend servis katmanında gerçekleştirilir ve sonuçlar dashboard’a yansıtılır.

---

## Reset Mekanizması (Güvenlik)

Reset işlemi, veri kaybı riski taşıdığı için çok katmanlı güvenlik ile korunmaktadır:

1. Sadece admin kullanıcılar erişebilir  
2. Ek reset şifresi gereklidir  
3. Kullanıcıdan ikinci onay alınır ("Emin misin?")  
4. İşlem yalnızca POST isteği ile gerçekleştirilir (CSRF korumalı)  

Amaç, yetkisiz veya hatalı veri silinmesini engellemektir.

---

## Reset İşlemi

Reset mekanizması aşağıdaki adımları uygular:

1. Mevcut veriler `backup.json` dosyasına yedeklenir  
2. Veritabanı tamamen temizlenir (`flush`)  
3. Önceden hazırlanmış golden veri seti yüklenir (`loaddata`)  
4. Sistem tekrar kullanılabilir hale getirilir  

Sonuç:

> Sistem, bozulmuş durumdan temiz ve stabil bir duruma getirilir

---

## Reset Tetikleme Yöntemleri

### Ana yöntem:
- Django Admin Panel üzerinden "Reset Demo" butonu  

### Ek yöntem:
- Şifre korumalı özel endpoint (`/admin/reset-demo/`)  

---

## Demo Senaryosu

1. Sistem başlangıçta temizdir  
   → `Bozuk Veri: 0`  

2. Test modu çalıştırılır  
   → Sistem bozulur  
   → `Bozuk Veri: 12`  

3. Kullanıcı bozuk verileri gözlemler  

4. Admin reset mekanizmasını başlatır  
   - Şifre doğrulaması  
   - Onay süreci  

5. Sistem resetlenir  

6. Dashboard tekrar kontrol edilir  
   → `Bozuk Veri: 0`  

Bu senaryo, sistemin veri bozulmasına karşı dayanıklılığını göstermektedir.

---

## Kurulum ve Çalıştırma

```bash
git clone https://github.com/melisasudee/bookstore-reset-demo.git
cd bookstore-reset-demo
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata golden_data.json
python manage.py createsuperuser
python manage.py runserver
```

---

## Not

Bu proje eğitim amaçlı geliştirilmiştir. Gerçek üretim ortamları için ek güvenlik, performans ve hata yönetimi mekanizmaları gereklidir.

---

## Geliştirici

Ad Soyad: Melisa Sudenaz Arık  
Ders: Yazılım Mühendisliğine Giriş  
Tarih: 28.04.2026
