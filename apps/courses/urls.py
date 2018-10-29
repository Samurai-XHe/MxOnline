from django.urls import path, include
from .views import CourseListView, CourseDetailView, CourseInfoView
__author__ = 'xhe'
__date__ = '18-10-26 上午9:36'


app_name = 'courses'
urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    path('course/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('course_info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
]