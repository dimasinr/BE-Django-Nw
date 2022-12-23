from django.db import models
from userapp.models import User

class CutiHr(models.Model):
    sisa_cuti = models.CharField(max_length=24,  null=True)
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField( null=True, blank=True)

    def __str__(self):
        return self.sisa_cuti

class NotesHrd(models.Model):
    employee_name = models.CharField(max_length=50, null=True)
    jatah_cuti = models.CharField(max_length=120, null=True)
    sisa_cuti = models.CharField(max_length=24,  null=True)
    tanggal_cuti = models.DateField(null=True, blank=True)
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField( null=True, blank=True)
    data_cuti = models.ForeignKey(
        CutiHr, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.employee_name

class EmployeeCuti(models.Model):
    employee_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    jatah_cuti = models.CharField(max_length=120, null=True)
    sisa_cuti = models.CharField(max_length=24,  null=True)
    tanggal_cuti = models.DateField(null=True, blank=True)
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField( null=True, blank=True)
    catatan = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.sisa_cuti

