# Generated by Django 3.2.16 on 2023-01-16 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0015_alter_useractive_useractived'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserActive',
        ),
    ]