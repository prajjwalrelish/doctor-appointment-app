# Generated by Django 3.2.6 on 2021-12-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='order_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='transactions',
            name='signature',
            field=models.CharField(default='', max_length=100),
        ),
    ]