# Generated by Django 3.2.3 on 2021-10-31 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0004_alter_user_photo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]