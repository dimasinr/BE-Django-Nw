# Generated by Django 3.2.16 on 2023-01-09 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pengajuanEmp', '0008_auto_20230109_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='petitions',
            name='conditional_reasons',
            field=models.TextField(blank=True, null=True),
        ),
    ]