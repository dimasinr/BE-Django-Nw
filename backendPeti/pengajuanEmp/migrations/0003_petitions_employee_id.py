# Generated by Django 3.2.16 on 2023-01-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pengajuanEmp', '0002_petitions_jumlah_hari'),
    ]

    operations = [
        migrations.AddField(
            model_name='petitions',
            name='employee_id',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
