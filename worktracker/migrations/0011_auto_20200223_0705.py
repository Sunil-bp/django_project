# Generated by Django 3.0.2 on 2020-02-23 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0010_userstat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstat',
            name='current_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='worktracker.Task'),
        ),
    ]