# Generated by Django 3.0.3 on 2020-11-13 05:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20201112_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]