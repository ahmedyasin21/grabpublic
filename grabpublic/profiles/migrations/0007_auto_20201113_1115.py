# Generated by Django 3.0.3 on 2020-11-13 19:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20201112_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='create_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='create_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
