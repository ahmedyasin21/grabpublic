# Generated by Django 3.0.3 on 2020-11-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, max_length=250, verbose_name='Description'),
        ),
    ]
