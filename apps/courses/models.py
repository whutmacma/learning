# _*_ encoding:utf-8 _*_
from datetime import datetime


from django.db import models


from organization.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    course_organization = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"课程机构", null=True, blank=True)
    course_teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name=u"课程教师", null=True, blank=True )
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj",u"初级"),("zj",u"中级"),("gj",u"高级")), max_length=2)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加次数")
    category = models.CharField(default=u"Web后端", max_length=20, verbose_name=u"课程类别")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    prior_knowledge = models.CharField(default="", verbose_name=u"课程须知",max_length=20)
    course_knowledge = models.CharField(default="", verbose_name=u"你可以学到的技能",max_length=20)

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    def get_lesson_nums(self):
        return self.lesson_set.all().count()
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]
    def get_lesson(self):
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    def get_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course =  models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m",max_length=100, verbose_name=u"资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
