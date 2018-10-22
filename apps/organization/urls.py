from django.urls import path
from .views import OrgView, AddUserAskView
__author__ = 'xhe'
__date__ = '18-10-22 上午9:30'

app_name = 'organization'
urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask')
]