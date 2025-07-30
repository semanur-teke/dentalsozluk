from django.urls import path
from . import views
app_name = 'terms'
from .views import robots_txt
from django.contrib.sitemaps.views import sitemap
from terms.sitemaps import TermSitemap

sitemaps = {
    'terms': TermSitemap,
}


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('terimler/', views.term_list, name='term_list'),
    path('terim/<slug:slug>/', views.term_detail, name='term_detail'),
    path('report_error/', views.report_error, name='report_error'),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # ← Statik sayfalarınızı buraya ekleyin:
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('cerez-politikasi/', views.cerez_politikasi, name='cerez_politikasi'),
    path('gizlilik-ilkesi/', views.gizlilik_ilkesi, name='gizlilik_ilkesi'),
]
