# Generated by Django 2.0.1 on 2018-06-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20180611_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('reset_email', '修改邮箱')], max_length=15, verbose_name='验证码类型'),
        ),
    ]
