# Generated by Django 2.0.1 on 2018-05-04 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20180504_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='addd_time',
            new_name='add_time',
        ),
    ]
