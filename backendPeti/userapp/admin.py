from django.contrib import admin
from .models import User, UserRoles, UserDivision, Log, UserNotes, UserBank, UserBerkas, UserAdditionalData, UserCertificate, UserContract, Certificate
from import_export.admin import ImportExportModelAdmin

admin.site.register(Log)
admin.site.register(Certificate)

@admin.register(User,  site=admin.site)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'division', 'username', 'email', 'status_employee', 'birth_date', 'alamat')
    search_fields = ('name',)
    ordering = ('id', )

@admin.register(UserRoles, site=admin.site)
class UserRolesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'roles')
    search_fields = ('roles',)
    ordering = ('id', )

@admin.register(UserDivision, site=admin.site)
class UserDivisionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'division')
    search_fields = ('division',)
    ordering = ('id', )

@admin.register(UserNotes, site=admin.site)
class UserNotesAdmin(ImportExportModelAdmin):
    list_display = ['employee', 'notes', 'created_at', 'updated_at']
    search_fields = ('employee', 'notes', )
    ordering = ('id', )

@admin.register(UserBerkas, site=admin.site)
class UserBerkasAdmin(ImportExportModelAdmin):
    list_display = ['id', 'employee', 'nik', 'no_npwp', 'no_bpjs']
    search_fields = ('employee', 'nik', 'no_npwp', 'no_bpjs')
    ordering = ('id', )

@admin.register(UserBank, site=admin.site)
class UserBankAdmin(ImportExportModelAdmin):
    list_display = ['id', 'employee', 'nomor', 'bank']
    search_fields = ('employee', 'nomor', 'bank')
    ordering = ('id', )

@admin.register(UserAdditionalData, site=admin.site)
class UserAdditionalDataAdmin(ImportExportModelAdmin):
    list_display = ['id', 'employee']
    search_fields = ('employee', )
    ordering = ('id', )

@admin.register(UserCertificate, site=admin.site)
class UserCertificateAdmin(ImportExportModelAdmin):
    list_display = ['id', 'employee', 'institute_name', 'study_program', 'certificate_level']
    search_fields = ('employee', 'institute_name', 'study_program', 'certificate_level')
    ordering = ('id', )

@admin.register(UserContract, site=admin.site)
class UserContractAdmin(ImportExportModelAdmin):
    list_display = ['id', 'employee', 'contract_start', 'contract_end', 'contract_time']
    search_fields = ('employee', 'contract_start', 'contract_end', 'contract_time')
    ordering = ('id', )