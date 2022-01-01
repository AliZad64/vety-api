# Generated by Django 4.0 on 2022-01-01 14:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=255, null=True, verbose_name='gender')),
                ('birth', models.DateField(blank=True, null=True, verbose_name='birth')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.emailaccount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('facebook', models.URLField(blank=True, max_length=500, null=True, verbose_name='facebook')),
                ('instagram', models.URLField(blank=True, max_length=500, null=True, verbose_name='instagram')),
                ('work_range', models.CharField(blank=True, max_length=255, null=True, verbose_name='work_range')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.emailaccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]