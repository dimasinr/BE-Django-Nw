# Generated by Django 3.2.16 on 2023-01-20 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pengajuanEmp', '0010_auto_20230120_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petitions',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
