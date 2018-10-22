from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from .models import CourseOrg, CityDict
from .forms import UserAskForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):
    def get(self, request):
        # 查找到所有的课程机构
        all_orgs = CourseOrg.objects.all()
        # 取出排名前三的热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 取出所有的城市
        all_citys = CityDict.objects.all()
        # 按城市筛选
        try:
            city_id = int(request.GET.get('city', ''))
        except ValueError:
            city_id = ''
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        # 按机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')


        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        # 总共有多少家机构使用count进行统计
        org_numbers = all_orgs.count()
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_numbers': org_numbers,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '{0}'.format(userask_form.errors)})


