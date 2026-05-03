import random
from decimal import Decimal
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.conf import settings

from .models import Book, Sale


class DataValidator:
    def validate(self):
        issues = []
        seen_titles = set()

        for book in Book.objects.all():
            if not book.title:
                issues.append(f"Book #{book.id}: Kitap adı boş")

            if not book.author:
                issues.append(f"Book #{book.id}: Yazar boş")

            if book.price is None:
                issues.append(f"Book #{book.id}: Fiyat boş")
            elif book.price < 0:
                issues.append(f"Book #{book.id}: Negatif fiyat")
            elif book.price > Decimal("1000"):
                issues.append(f"Book #{book.id}: Mantıksız yüksek fiyat")

            if book.stock is None:
                issues.append(f"Book #{book.id}: Stok boş")
            elif book.stock < 0:
                issues.append(f"Book #{book.id}: Negatif stok")

            if book.image_url and not self.valid_url(book.image_url):
                issues.append(f"Book #{book.id}: Geçersiz görsel URL")

            key = book.title.strip().lower() if book.title else ""
            if key:
                if key in seen_titles:
                    issues.append(f"Book #{book.id}: Kopya kitap kaydı")
                seen_titles.add(key)

        for sale in Sale.objects.all():
            if sale.book is None:
                issues.append(f"Sale #{sale.id}: Kitap bağlantısı yok")
            if sale.quantity <= 0:
                issues.append(f"Sale #{sale.id}: Geçersiz satış adedi")
            if sale.unit_price < 0:
                issues.append(f"Sale #{sale.id}: Negatif satış fiyatı")

        return issues

    def valid_url(self, value):
        parsed = urlparse(value)
        return parsed.scheme in ["http", "https"] and bool(parsed.netloc)


class JunkDataGenerator:
    def generate(self, count=12):
        # garantili hatalar - benzersiz title'lar ile
        self.base_book(title="Eksik Kitap Adı", author="", price=Decimal("120.00"), stock=20, image_url="https://example.com/book.jpg")  # missing_author
        self.base_book(title="Negatif Fiyatlı Kitap", author="Demo Yazar", price=Decimal("-50.00"), stock=20, image_url="https://example.com/book.jpg")  # negative_price
        self.base_book(title="Geçersiz URL'li Kitap", author="Demo Yazar", price=Decimal("120.00"), stock=20, image_url="invalid-url")  # invalid_url

        # duplicate için önce normal kitap oluştur, sonra kopyala
        self.base_book(title="Kopyalanacak Kitap", author="Demo Yazar", price=Decimal("120.00"), stock=20, image_url="https://example.com/book.jpg")
        self.duplicate_book()  # şimdi kopyalayabilir

        # kalanları rastgele doldur
        methods = [
            self.missing_title,
            self.missing_author,
            self.negative_stock,
            self.huge_price,
        ]

        for _ in range(count - 5):  # 4 garantili + 1 duplicate için = 5
            random.choice(methods)()

    def base_book(self, **kwargs):
        data = {
            "title": f"Demo Kitap {random.randint(1000, 9999)}",
            "author": "Demo Yazar",
            "price": Decimal("120.00"),
            "stock": 20,
            "image_url": "https://example.com/book.jpg",
        }
        data.update(kwargs)
        Book.objects.create(**data)

    def missing_title(self):
        self.base_book(title="")

    def missing_author(self):
        self.base_book(author="")

    def negative_price(self):
        self.base_book(price=Decimal("-50.00"))

    def negative_stock(self):
        self.base_book(stock=-10)

    def huge_price(self):
        self.base_book(price=Decimal("999.99"))

    def invalid_url(self):
        self.base_book(image_url="invalid-url")

    def duplicate_book(self):
        first = Book.objects.first()
        if first:
            Book.objects.create(
                title=first.title,
                author=first.author,
                price=first.price,
                stock=first.stock,
                image_url=first.image_url,
            )
        else:
            self.base_book(title="Kopya Kitap")


class DemoDataGenerator:
    def generate(self, count=5):
        authors = [
            "Orhan Pamuk",
            "Elif Şafak",
            "Ahmet Ümit",
            "Nazım Hikmet",
            "Halide Edip Adıvar",
        ]
        urls = [
            "https://covers.openlibrary.org/b/id/8231996-L.jpg",
            "https://covers.openlibrary.org/b/id/7222246-L.jpg",
            "https://covers.openlibrary.org/b/id/6979861-L.jpg",
            "https://covers.openlibrary.org/b/id/8226191-L.jpg",
            "https://covers.openlibrary.org/b/id/8224171-L.jpg",
        ]

        for _ in range(count):
            self.base_book(
                title=f"Demo Veri Kitap {random.randint(100, 999)}",
                author=random.choice(authors),
                price=Decimal(random.choice(["89.90", "99.90", "109.90", "119.90", "129.90"])),
                stock=random.randint(5, 16),
                image_url=random.choice(urls),
            )

        recent_books = Book.objects.order_by("-id")[:min(3, count)]
        for book in recent_books:
            Sale.objects.create(
                book=book,
                quantity=random.randint(1, 4),
                unit_price=book.price or Decimal("49.90"),
            )

    def base_book(self, **kwargs):
        data = {
            "title": f"Demo Kitap {random.randint(1000, 9999)}",
            "author": "Demo Yazar",
            "price": Decimal("120.00"),
            "stock": 20,
            "image_url": "https://example.com/book.jpg",
        }
        data.update(kwargs)
        Book.objects.create(**data)


class DemoResetService:
    def reset(self):
        call_command("dumpdata", "store", output="backup.json")
        call_command("flush", interactive=False)
        call_command("loaddata", "./golden_data.json")
        self.ensure_admin()

    def ensure_admin(self):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123",
            )
