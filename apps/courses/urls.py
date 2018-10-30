from django.urls import path, include
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView
__author__ = 'xhe'
__date__ = '18-10-26 上午9:36'


app_name = 'courses'
urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    path('course/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('course_info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
    path('comments/<int:course_id>/', CommentsView.as_view(), name='course_comments'),
    path('add_comment/', AddCommentsView.as_view(), name='add_comment'),
    path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),
]