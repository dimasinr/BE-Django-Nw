# Generated by Django 3.2.16 on 2023-02-08 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0013_auto_20230208_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noteshrd',
            name='employee_id',
        ),
    ]