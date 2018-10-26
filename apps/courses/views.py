from django.shortcuts import render
from django.views.generic.base import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-students')[:3]
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
            'hot_course': hot_course
        })


class CourseDetailView(View):
    def get(self, reqeust, course_id):
        course = Course.objects.get(pk=course_id)
        tag = course.tag
        course.click_nums += 1
        course.save()
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []
        return render(reqeust, 'course-detail.html', {'course': course, 'relate_courses': relate_courses})
