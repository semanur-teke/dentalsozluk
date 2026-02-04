from django.contrib import admin
from .models import DentalTerm


@admin.register(DentalTerm)
class DentalTermAdmin(admin.ModelAdmin):
    list_display = ('title', 'english_equivalent', 'latin_equivalent', 'slug')
    search_fields = ('title', 'english_equivalent', 'latin_equivalent', 'search_aliases')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description')
        }),
        ('Karşılıklar', {
            'fields': ('english_equivalent', 'latin_equivalent')
        }),
        ('Arama', {
            'fields': ('search_aliases',),
            'description': 'Sık yapılan yazım hatalarını veya alternatif yazılışları buraya ekleyin.'
        }),
    )

from .models import ErrorReport

@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ('term', 'created')
    list_filter = ('created',)
