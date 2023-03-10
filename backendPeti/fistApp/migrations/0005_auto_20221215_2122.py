# Generated by Django 3.2.16 on 2022-12-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fistApp', '0004_auto_20221215_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengajuans',
            name='suspended_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pengajuans',
            name='suspended_start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pengajuans',
            name='permission_pil',
            field=models.CharField(blank=True, max_length=24),
        ),
        migrations.AlterField(
            model_name='pengajuans',
            name='reason_rejected',
            field=models.TextField(blank=True, null=True),
        ),
    ]
