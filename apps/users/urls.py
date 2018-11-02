from django.urls import path
from .views import UserInfoView, UploadImageView, UpdatePwdView, UpdateEmailView, SendEmailCodeView, UploadUserProfileView


app_name = 'users'
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('update_img/', UploadImageView.as_view(), name='update_image'),
    path('update_pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    path('update_profile/', UploadUserProfileView.as_view(), name='update_profile'),
    path('send_email_code/', SendEmailCodeView.as_view(), name='send_email_code'),
]

