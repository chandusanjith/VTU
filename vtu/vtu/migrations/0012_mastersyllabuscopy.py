# Generated by Django 3.1.4 on 2021-01-03 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vtu', '0011_appforceupdaterequired_appversion_deviceauth'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterSyllabusCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('updated_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]