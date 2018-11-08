"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from users.views import IndexView
import xadmin


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    path('org/', include('organization.urls')),
    path('course/', include('courses.urls')),
    path('users/', include('users.urls')),
    # re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]

handler403 = 'users.views.csrf_error'
handler404 = 'users.views.page_not_fond'
handler500 = 'users.views.page_error'

