from django import forms
from captcha.fields import CaptchaField

__author__ = 'xhe'
__date__ = '18-10-10 上午9:30'


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        error_messages={
            'required': '请填写用户名'
        })
    password = forms.CharField(
        required=True,
        min_length=5,
        error_messages={
            'required': '请填写密码',
            'min_length': '密码至少五位'
        })


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '请填写一个有效的EMAIL地址'
        })
    password = forms.CharField(
        required=True,
        min_length=5,
        error_messages={
            'required': '请填写密码',
            'min_length': '密码至少五位'
        })
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '请填写一个有效的EMAIL地址'
        })
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        min_length=5,
        error_messages={
            'required': '请填写密码',
            'min_length': '密码至少五位'
        })
    password2 = forms.CharField(
        required=True,
        min_length=5,
        error_messages={
            'required': '请再一次密码',
            'min_length': '密码至少五位'
        })

