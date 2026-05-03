from django.contrib import admin
from .models import Book, Sale

admin.site.site_header = "Kitabevi Yönetim Paneli"
admin.site.site_title = "Kitabevi Admin"
admin.site.index_title = "Yönetim Kontrol Paneli"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "stock", "image_url")
    search_fields = ("title", "author")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("book", "quantity", "unit_price")
