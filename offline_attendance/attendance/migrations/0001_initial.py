# Generated by Django 3.2.7 on 2022-11-15 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentData',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=100)),
                ('branch', models.CharField(blank=True, max_length=30, null=True)),
                ('semester', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], default='1', max_length=20)),
                ('contact_number', models.CharField(blank=True, max_length=10, null=True)),
                ('email_id', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=10, null=True)),
                ('email_id', models.EmailField(max_length=100)),
                ('username', models.ForeignKey(db_column='staff', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]