# Generated by Django 3.2.16 on 2023-03-01 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0015_auto_20230216_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='noteshrd',
            name='name_day',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
