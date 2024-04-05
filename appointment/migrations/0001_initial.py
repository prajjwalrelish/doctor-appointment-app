# Generated by Django 3.2.6 on 2021-08-27 10:51

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_profile', models.UUIDField()),
                ('doctor', models.UUIDField(default=False)),
                ('appointment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('appointment_time', models.TimeField(blank=True)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=7)),
                ('transaction', models.UUIDField()),
                ('booking_status', models.DateField(default=django.utils.timezone.now)),
                ('prescription', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoctorNotification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('acceptance', models.CharField(choices=[('confirmed', 'Confirmed'), ('not_confirmed', 'Not_Confirmed')], default='not_confirmed', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
