# Generated by Django 3.2.3 on 2021-10-31 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]