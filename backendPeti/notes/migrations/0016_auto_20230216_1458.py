# Generated by Django 3.2.16 on 2023-02-16 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0015_auto_20230216_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='noteshrd',
            old_name='days',
            new_name='day_notes',
        ),
        migrations.RenameField(
            model_name='noteshrd',
            old_name='months',
            new_name='month_notes',
        ),
        migrations.RenameField(
            model_name='noteshrd',
            old_name='years',
            new_name='year_notes',
        ),
    ]