# Generated by Django 3.2.16 on 2023-04-03 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submisssion', '0005_auto_20230403_1440'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='uuid_id',
            new_name='id',
        ),
    ]
