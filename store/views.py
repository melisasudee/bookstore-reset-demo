from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Book, Sale
from .services import DataValidator, JunkDataGenerator, DemoResetService


def dashboard(request):
    issues = DataValidator().validate()

    revenue_expr = ExpressionWrapper(
        F("quantity") * F("unit_price"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )

    total_revenue = Sale.objects.aggregate(total=Sum(revenue_expr))["total"] or Decimal("0.00")

    books = list(Book.objects.all())
    chart_labels = [book.title or "Boş Kitap" for book in books]
    chart_stocks = [book.stock or 0 for book in books]
    chart_prices = [float(book.price or 0) for book in books]

    total_book_revenue = sum((book.stock or 0) * float(book.price or 0) for book in books)
    revenue_distribution = []
    for book in books:
        amount = (book.stock or 0) * float(book.price or 0)
        percentage = (amount / total_book_revenue * 100) if total_book_revenue else 0
        revenue_distribution.append(round(percentage, 1))

    return render(request, "store/dashboard.html", {
        "books": books,
        "issue_count": len(issues),
        "issues": issues,
        "total_books": len(books),
        "total_sales": Sale.objects.count(),
        "total_revenue": total_revenue,
        "chart_labels": chart_labels,
        "chart_stocks": chart_stocks,
        "chart_prices": chart_prices,
        "revenue_distribution": revenue_distribution,
        "total_book_revenue": total_book_revenue,
    })


@staff_member_required
@require_POST
def generate_junk_data(request):
    JunkDataGenerator().generate(12)
    messages.warning(request, "12 adet bozuk veri üretildi.")
    return redirect("dashboard")


@staff_member_required
def reset_demo(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != settings.DEMO_RESET_PASSWORD:
            messages.error(request, "Reset şifresi yanlış.")
            return redirect("reset_demo")

        if confirm != "yes":
            messages.error(request, "İkinci onay verilmedi.")
            return redirect("reset_demo")

        DemoResetService().reset()
        messages.success(request, "Sistem golden veri setine döndürüldü.")
        return redirect("dashboard")

    return render(request, "store/reset.html", {
        "messages": [str(m) for m in messages.get_messages(request)]
    })