from django.urls import path
from .views import UserInfoView


app_name = 'users'
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
]

