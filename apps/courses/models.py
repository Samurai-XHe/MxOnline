from django.db import models
from organization.models import CourseOrg, Teacher


# 课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),)
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    # TextField允许我们不输入长度。可以输入到无限大
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name='难度')
    # 使用分钟做后台记录(存储最小单位)前台转换
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    # 保存学习人数:点击开始学习才算
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(
        upload_to='courses/%Y/%m',
        verbose_name='封面图',
        max_length=100)
    # 保存点击量，点进页面就算
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构', null=True, blank=True)
    category = models.CharField(max_length=20, default='', verbose_name='课程类别')
    tag = models.CharField(max_length=15, default='' ,verbose_name='课程标签')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师', null=True, blank=True)
    you_need_know = models.CharField(max_length=300, default='一颗勤学的心是本课程必要前提', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default='按时交作业,不然叫家长', verbose_name='老实告诉你')
    is_banner = models.BooleanField(default=False, verbose_name='轮播图')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        nums = self.lesson_set.all().count()
        return nums

    def get_learn_users(self):
        students = self.usercourse_set.all()[:5]
        return students

    def __str__(self):
        return self.name


# 章节表
class Lesson(models.Model):
    # 因为一个课程对应很多章节。所以在章节表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个章节对应那个课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的{1}'.format(self.course, self.name)


# 每章视频表
class Video(models.Model):
    # 因为一个章节对应很多视频。所以在视频表中将章节设置为外键。
    # 作为一个字段来存储让我们可以知道这个视频对应哪个章节.
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    url = models.CharField(max_length=200, default='http://blog.mtianyan.cn', verbose_name='访问地址')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}的视频：{1}'.format(self.lesson, self.name)


# 课程资源表
class CourseResource(models.Model):
    # 因为一个课程对应很多资源。所以在课程资源表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个资源对应那个课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    # 这里定义成文件类型的field，后台管理系统中会直接有上传的按钮。
    # FileField也是一个字符串类型，要指定最大长度。
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name='资源文件',
        max_length=100)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的资源：{1}'.format(self.course, self.name)
