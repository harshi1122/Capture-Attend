# Generated by Django 3.2.4 on 2021-07-17 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_take_attendance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='take_attendance',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]