# Generated by Django 3.0.2 on 2020-02-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200208_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='current_announcement',
            field=models.CharField(choices=[('True', 'displayed'), ('False', 'not displayed')], default='False', max_length=5),
        ),
    ]
