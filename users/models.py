from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(
        max_length=6, verbose_name='性别', choices=(('male', '男'), ('female', '女')), default='female')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机')
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100, verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(
        max_length=30, verbose_name='验证码类型', choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')))
    send_time = models.DateTimeField(verbose_name='发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(max_length=100, verbose_name='轮播图', upload_to='banner/%Y/%m')
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
