# Generated by Django 3.1.4 on 2021-01-03 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vtu', '0012_mastersyllabuscopy'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersyllabuscopy',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='syllabus_branch', to='vtu.masterbranches'),
        ),
    ]
