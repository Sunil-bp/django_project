# Generated by Django 3.0.2 on 2020-02-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0002_testdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login_data',
            name='log_out',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='login_data',
            name='time_spent',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='Testdata',
        ),
    ]