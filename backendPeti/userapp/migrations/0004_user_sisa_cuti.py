# Generated by Django 3.2.16 on 2023-01-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_alter_user_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sisa_cuti',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
