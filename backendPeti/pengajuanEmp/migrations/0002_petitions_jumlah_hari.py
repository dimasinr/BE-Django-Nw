# Generated by Django 3.2.16 on 2023-01-03 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pengajuanEmp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='petitions',
            name='jumlah_hari',
            field=models.CharField(max_length=24, null=True),
        ),
    ]
