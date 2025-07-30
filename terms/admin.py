from django.contrib import admin
from .models import DentalTerm

admin.site.register(DentalTerm)

from .models import ErrorReport

@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ('term', 'created')
    list_filter = ('created',)
