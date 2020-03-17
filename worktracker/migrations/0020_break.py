# Generated by Django 3.0.2 on 2020-03-10 16:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worktracker', '0019_auto_20200310_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('break_in', models.DateTimeField(auto_now_add=True)),
                ('break_out', models.DateTimeField(blank=True, default=None, null=True)),
                ('create_on', models.DateField(default=datetime.date.today)),
                ('break_tittle', models.TextField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
