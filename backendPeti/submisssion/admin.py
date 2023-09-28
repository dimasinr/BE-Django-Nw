from django.contrib import admin
from .models import Submission, CalendarCutiSubmission
from import_export.admin import ImportExportModelAdmin

@admin.register(Submission, site=admin.site)
class SubmissionAdmin(ImportExportModelAdmin):
    list_display = ['employee', 'permission_type', 'reason', 'start_date', 'end_date', 'jumlah_hari', 'permission_pil']
    search_fields = ('employee', 'permission_type')
    ordering = ('id', )
  
@admin.register(CalendarCutiSubmission, site=admin.site)
class CalendarCutiSubmissionAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'permission_type')
    search_fields = ('employee',)
    ordering = ('id', )