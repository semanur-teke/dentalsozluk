from django.contrib.sitemaps import Sitemap
from .models import DentalTerm

class TermSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return DentalTerm.objects.all()

    def location(self, obj):
        return f"/terim/{obj.slug}/"
