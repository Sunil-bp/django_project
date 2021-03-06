# Generated by Django 3.0.2 on 2020-05-09 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense_tracker', '0003_auto_20200509_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financeprofile',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='financeprofile',
            name='add_to_total',
        ),
        migrations.RemoveField(
            model_name='financeprofile',
            name='balance',
        ),
        migrations.AlterField(
            model_name='financeprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
