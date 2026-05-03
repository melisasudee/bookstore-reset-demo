from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("generate-junk/", views.generate_junk_data, name="generate_junk_data"),
    path("admin/reset-demo/", views.reset_demo, name="reset_demo"),
    path("admin/", admin.site.urls),
]