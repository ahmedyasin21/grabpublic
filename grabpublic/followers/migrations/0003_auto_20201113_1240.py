# Generated by Django 3.0.3 on 2020-11-13 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20201113_1115'),
        ('followers', '0002_auto_20201113_1239'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Freefollowers',
            new_name='Freefollower',
        ),
    ]
