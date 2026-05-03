from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField("Kitap Adı", max_length=200, blank=True)
    author = models.CharField("Yazar", max_length=150, blank=True)
    price = models.DecimalField(
        "Fiyat",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    stock = models.IntegerField("Stok", null=True, blank=True)
    image_url = models.CharField("Görsel URL", max_length=500, blank=True)

    def __str__(self):
        return self.title or "Boş Kitap"


class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField("Adet", default=1)
    unit_price = models.DecimalField("Birim Fiyat", max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.book} x {self.quantity}"
