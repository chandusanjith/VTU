# Generated by Django 3.1.4 on 2021-01-01 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vtu', '0008_mastervideolab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastervideolab',
            name='programid',
            field=models.IntegerField(default=0),
        ),
    ]
