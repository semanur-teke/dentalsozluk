# dentalsozluk/urls.py
from django.contrib import admin
from django.urls import path, include
from terms import views as term_views  # ← EKLE

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", term_views.home, name="home"),  # ← KÖKTEN 'home' alias
    path("", include(("terms.urls", "terms"), namespace="terms")),  # ← NAMESPACE'li include
]

