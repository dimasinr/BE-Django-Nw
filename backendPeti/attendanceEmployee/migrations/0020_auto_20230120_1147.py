# Generated by Django 3.2.16 on 2023-01-20 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceEmployee', '0019_alter_attendanceemployee_lembur_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceemployee',
            name='lembur_hour_detail',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendanceemployee',
            name='working_hour_detail',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
