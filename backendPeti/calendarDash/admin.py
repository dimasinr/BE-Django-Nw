from django.contrib import admin
from .models import CalendarDashHRD, DashboardHRD
from import_export.admin import ImportExportModelAdmin

@admin.register(DashboardHRD, site=admin.site)
class DashboardHRDAdmin(ImportExportModelAdmin):
    list_display = ('id', 'total_employee', 'total_days', 'hour_perday', 'total_hour')
    search_fields = ('total_days', 'total_employee')
    ordering = ('id', )

@admin.register(CalendarDashHRD, site=admin.site)
class CalendarDashHRDAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title_day', 'type_day', 'date', 'day_names')
    search_fields = ('title_day', 'type_day')
    ordering = ('id', )
