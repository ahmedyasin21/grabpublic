# Generated by Django 3.0.3 on 2020-11-13 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followers', '0003_auto_20201113_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freefollower',
            name='free_10_followers',
            field=models.BooleanField(default=False),
        ),
    ]
