from django.contrib import admin
from .models import NotesApp
from import_export.admin import ImportExportModelAdmin

@admin.register(NotesApp, site=admin.site)
class NotesAppAdmin(ImportExportModelAdmin):
    list_display = ('id', 'employee', 'date_note', 'notes', 'type_notes', 'created_at' )
    search_fields = ('employee', 'notes', 'type_notes' )
    ordering = ('id', )