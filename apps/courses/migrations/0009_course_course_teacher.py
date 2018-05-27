# Generated by Django 2.0.1 on 2018-05-26 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_teacher_image'),
        ('courses', '0008_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='课程教师'),
        ),
    ]
