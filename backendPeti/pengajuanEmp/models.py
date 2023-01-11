from django.db import models

class Petitions(models.Model):
    employee_id = models.CharField(max_length=40, null=True)
    employee_name = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=120, null=True)
    permission_type = models.CharField(max_length=24,  null=True)
    reason = models.TextField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    jumlah_hari = models.CharField(max_length=24,  null=True)
    return_date = models.DateField(null=True)
    permission_pil = models.CharField( null=True, max_length=24,  blank=True)
    reason_rejected = models.TextField( null=True, blank=True)
    conditional_reasons = models.TextField( null=True, blank=True)
    suspended_start = models.DateField( null=True, blank=True)
    suspended_end = models.DateField( null=True, blank=True)

    def __str__(self):
        return self.employee_name

class PetitionsCalendar(models.Model):
    title = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=120, null=True)
    permission_type = models.CharField(max_length=24,  null=True)
    reason = models.TextField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return self.title