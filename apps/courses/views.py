from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-students')[:3]
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords) |
                Q(detail__icontains=search_keywords)
            )
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_course': hot_course,
            'search_keywords': search_keywords,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        tag = course.tag
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course.students += 1
        course.save()
        # 添加用户课程
        if not UserCourse.objects.filter(course=course, user=request.user):
            user_course = UserCourse()
            user_course.course = course
            user_course.user = request.user
            user_course.save()

        course_resources = CourseResource.objects.filter(course_id=course_id)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(pk__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
        })


class CommentsView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course).order_by('-add_time')
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(pk__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
        })


class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(pk=course_id)
            course_comments.course = course
            course_comments.user = request.user
            course_comments.comments = comments
            course_comments.save()
            return JsonResponse({'status': 'success', 'msg': '评论成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '评论失败'})


class VideoPlayView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        course = video.lesson.course
        all_resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(pk__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'video': video,
            'course_resources': all_resources,
            'relate_courses': relate_courses,
        })
