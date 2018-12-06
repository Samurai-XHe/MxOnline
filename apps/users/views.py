import logging
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)
# 自定义用户验证引擎，在settings中用AUTHENTICATION_BACKENDS指定该类
class CustomBackend(ModelBackend):
    # 使用户能够通过用户名或者邮箱地址登录
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 检查密码是否正确
            if user.check_password(password):
                return user
        except Exception:
            return None


# 首页View
class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')[:5]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banner':all_banner,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data['email']
            if UserProfile.objects.filter(email=user_name).exists():
                return render(request, 'register.html', {'msg': '该邮箱已被使用'})
            pass_word = register_form.cleaned_data['password']
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            # 发送欢迎信息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册!'
            user_message.save()
            # 发送邮件
            send_register_email(user_name, 'register')
            return render(request, 'login.html', {'msg': '邮箱激活链接已发送至您的邮箱，请先激活账号'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 用户登录
class LoginView(View):
    def get(self, request):
        next_url = request.GET.get('next', '')
        return render(request, 'login.html', {'next': next_url})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', '')
                    if next_url:
                        return redirect(next_url)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 用户退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code).first()
        if record:
            email = record.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            return render(request, 'login.html', {'msg': '您的账号已激活，请登录'})
        else:
            return render(request, 'register.html', {'msg': '您的激活链接无效'})


# 忘记密码处理
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            if not UserProfile.objects.filter(email=email).exists():
                return render(request, 'forgetpwd.html', {'msg': '邮箱不存在'})
            send_register_email(email, 'forget')
            return render(request , 'login.html', {'msg': '重置密码邮件已发送，请注意查收'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码请求
class ResetView(View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code).first()
        if record:
            email = record.email
            return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'forgetpwd.html', {'msg': '您的重置密码链接无效，请重新请求'})


# 重置密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html', {'msg': '密码修改成功，请登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


# 用户中心
class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'usercenter-info.html', {})


# 更新头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})


class UpdatePwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return JsonResponse({'status': 'fail', 'msg': '密码不一致'})

            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '请检查填写错误'})


class SendEmailCodeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        email = request.GET.get('email', '')
        # 检查email是否已存在
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email': '邮箱已存在'})
        else:
            send_register_email(email, 'update_email')
            return JsonResponse({'status': 'success'})


class UpdateEmailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email').exists()
        if existed:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '验证码无效'})


class UploadUserProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        user_profile_form = UserInfoForm(request.POST, instance=request.user)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '请正确填写数据'})


class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(pk=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            org = Teacher.objects.get(pk=teacher_id)
            teacher_list.append(org)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(pk=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for message in all_unread_message:
            message.has_read = True
            message.save()
        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })


# 配置全局403页面
def csrf_error(request, **kwargs):
    return render(request, '403.html', status=403)


# 配置全局404页面
def page_not_fond(request, **kwargs):
    return render(request, '404.html', status=404)


# 配置全局500页面
def page_error(request, **kwargs):
    return render(request, '500.html', status=503)



