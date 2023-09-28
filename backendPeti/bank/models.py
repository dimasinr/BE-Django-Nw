from django.db import models

from backendPeti.helper.file import RandomFileName

class Bank(models.Model):
    nama = models.CharField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to=RandomFileName('user/bank/'), null=True, blank=True)

    def __str__(self):
        return self.nama