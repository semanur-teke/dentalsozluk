# dentalsozluk/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from terms import views as term_views  # ← EKLE

def ads_txt(request):
    content = "google.com, pub-1097665456567426, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path("spiderman-semapai/", admin.site.urls),
    path("ads.txt", ads_txt, name="ads_txt"),  # ← AdSense ads.txt
    path("", term_views.home, name="home"),  # ← KÖKTEN 'home' alias
    path("", include(("terms.urls", "terms"), namespace="terms")),  # ← NAMESPACE'li include
]

