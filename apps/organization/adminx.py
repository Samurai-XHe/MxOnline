import xadmin
from .models import CityDict, CourseOrg, Teacher

__author__ = 'xhe'
__date__ = '18-9-30 上午10:23'


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'category']  # 搜索字段
    list_filter = [
        'name', 'desc', 'click_nums', 'category', 'fav_nums', 'city__name', 'address', 'add_time']  # 过滤器
    ordering = ['-click_nums']  # 按字段排序
    readonly_fields = ['click_nums', 'fav_nums']  # 只读字段
    exclude = []  # 详情页面中不显示的字段
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = [
        'org__name', 'name', 'work_years', 'work_company', 'click_nums', 'fav_nums', 'add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
