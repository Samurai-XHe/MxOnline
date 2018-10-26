from django.db import models
from users.models import UserProfile
from courses.models import Course


# 用户我要学习表单
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户咨询：%s' % self.name


# 用户对于课程评论
class CourseComments(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    comments = models.CharField(max_length=250, verbose_name='评论')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s ：%s' % (self.user.username, self.comments)


# 用户对于课程，机构，讲师的收藏
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据ID')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '讲师')), default=0, verbose_name='收藏类型')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s收藏的%s' % (self.user.username, self.fav_type)


# 用户消息表
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 用户课程表
class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name
