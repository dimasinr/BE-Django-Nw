from django.contrib import admin
from .models import PresenceEmployee
from import_export.admin import ImportExportModelAdmin

@admin.register(PresenceEmployee, site=admin.site)
class PresenceEmployeeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'employee', 'working_date', 'start_from', 'end_from', 'ket')
    search_fields = ('employee', 'ket')
    ordering = ('id', )