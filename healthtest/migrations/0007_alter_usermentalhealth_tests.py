# Generated by Django 3.2.3 on 2021-10-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthtest', '0006_alter_usermentalhealth_tests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermentalhealth',
            name='tests',
            field=models.JSONField(null=True),
        ),
    ]
