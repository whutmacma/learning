# Generated by Django 2.0.1 on 2018-05-05 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='click_nums',
        ),
    ]
