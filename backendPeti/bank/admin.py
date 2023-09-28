from django.contrib import admin
from .models import Bank
from import_export.admin import ImportExportModelAdmin

@admin.register(Bank, site=admin.site)
class BankAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)
    ordering = ('id', )