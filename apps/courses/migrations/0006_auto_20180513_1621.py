# Generated by Django 2.0.1 on 2018-05-13 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20180512_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='learn_times',
            new_name='learn_time',
        ),
    ]
