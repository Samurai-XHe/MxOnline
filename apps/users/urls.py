from django.urls import path
from .views import UserInfoView, UploadImageView, UpdatePwdView, UpdateEmailView, SendEmailCodeView
from .views import UploadUserProfileView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView


app_name = 'users'
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('update_img/', UploadImageView.as_view(), name='update_image'),
    path('update_pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    path('update_profile/', UploadUserProfileView.as_view(), name='update_profile'),
    path('send_email_code/', SendEmailCodeView.as_view(), name='send_email_code'),
    path('my_course/', MyCourseView.as_view(), name='my_course'),
    path('my_fav/org/', MyFavOrgView.as_view(), name='my_fav_org'),
    path('my_fav/teacher/', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    path('my_fav/course/', MyFavCourseView.as_view(), name='my_fav_course'),
    path('my_message/', MyMessageView.as_view(), name='my_message'),
]

