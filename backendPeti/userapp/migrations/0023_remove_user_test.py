# Generated by Django 3.2.16 on 2023-01-22 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0022_auto_20230123_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='test',
        ),
    ]
