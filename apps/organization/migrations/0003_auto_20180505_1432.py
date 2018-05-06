# Generated by Django 2.0.1 on 2018-05-05 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_remove_courseorg_click_nums'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='catgory',
            field=models.CharField(choices=[('training angency', '培训机构'), ('personal', '个人'), ('university', '高校')], default='traning angency', max_length=20, verbose_name='机构类别'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='click_nums',
            field=models.IntegerField(default=0, verbose_name='点击数'),
        ),
    ]