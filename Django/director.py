import json

from django.http import JsonResponse
from django.core.cache import cache
from django.shortcuts import render

from base.models import UserRelation, SchoolUser, TClass, ClassUser
from base.utils import String


# 提取所有参数（包括GET和POST）
from variables import SCHOOL_ROLE_TEACHER


def all_params(has_none=False, filter_list=[]):
    def all_params_handler(func):
        def _do(self, request, *args, **kwargs):
            request_params = request.GET
            if request_params:
                request_params.update(request.POST)
            else:
                request_params = request.POST
            params = {}
            if request_params:
                request_params = dict(request_params)
                filters = ['page', 'nums', 'csrfmiddlewaretoken'] + filter_list  # 过滤掉分页参数
                for key in filters:
                    if key in request_params:
                        request_params.pop(key)

                # 过滤空字符串
                if not has_none:
                    for index, item in request_params.items():
                        if len(item) == 1:
                            if not String.isblank(item[0]):
                                params[index] = item[0]
                        else:
                            params[index] = item
                # params = params if params else request_params
            return func(self, request, *args, **kwargs, params=params)
        return _do
    return all_params_handler


def all_params_func(has_none=False, filter_list=[]):
    def all_params_handler(func):
        def _do(request, *args, **kwargs):
            request_params = request.GET
            if request_params:
                request_params.update(request.POST)
            else:
                request_params = request.POST
            params = {}
            if request_params:
                request_params = dict(request_params)
                filters = ['page', 'nums', 'csrfmiddlewaretoken'] + filter_list  # 过滤掉分页参数
                for key in filters:
                    if key in request_params:
                        request_params.pop(key)

                # 过滤空字符串
                if not has_none:
                    for index, item in request_params.items():
                        if len(item) == 1:
                            if not String.isblank(item[0]):
                                params[index] = item[0]
                        else:
                            params[index] = item
                # params = params if params else request_params
            return func(request, *args, **kwargs, params=params)
        return _do
    return all_params_handler


# 检查是否登录（token 验证）
def login(func):
    def login_handler(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_TOKEN']
        except Exception as e:
            return JsonResponse({'code': False, 'msg': '未登录', 'data': ''})
        if not String.isblank(token):
            user = cache.get(token)
            if user:
                return func(self, request, *args, **kwargs)
        return JsonResponse({'code': False, 'msg': '未登录', 'data': ''})
    return login_handler


# 检查用户是否登录
def check_login(func):
    def check_login_handle(request, *args, **kw):
        try:
            token = request.META['HTTP_TOKEN']
        except Exception as e:
            print(e)
            return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})
        if token and token != '' and len(token.strip()) > 0:
            user_json = cache.get(token)
            if user_json:
                user = json.loads(user_json)
                return func(request, user, *args, **kw)
        return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})
    return check_login_handle


# 检查用户课程权限
def check_class(func):
    def check_class_handle(request, *args, **kw):
        try:
            token = request.META['HTTP_TOKEN']
        except Exception as e:
            print(e)
            return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})
        if token and token != '' and len(token.strip()) > 0:
            user = cache.get(token)
            if user:
                # 检查用户是否加入课程
                try:
                    class_id = request.GET['class_id']
                    student_id = request.GET.get('student_id')
                    user = json.loads(user)
                    if student_id and student_id != '':
                        UserRelation.objects.get(elder_id=user[0]['pk'], young_id=student_id, deleted=0, elder__deleted=0, young__deleted=0)    # 检查用户关系，抛异常说明用户关系不存在
                        tclass = ClassUser.objects.get(tclass_id=class_id, school_user__user_id=student_id, deleted=0, tclass__deleted=0, school_user__deleted=0)
                    else:
                        tclass = ClassUser.objects.get(tclass_id=class_id, school_user__user_id=user[0]['pk'], tclass__deleted=0, school_user__deleted=0)
                        student_id = user[0]['pk']
                    if not tclass:
                        raise Exception('班级不存在')
                except Exception as e:
                    print(e)
                    return JsonResponse({'code': True, 'msg': '', 'data': ''})
                return func(request, student_id, *args, **kw)
        return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})
    return check_class_handle


# 检查老师
def check_teacher(func):
    def check_teacher_handle(request, *args, **kw):
        try:
            token = request.META['HTTP_TOKEN']
        except Exception as e:
            print(e)
            return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})
        if token and token != '' and len(token.strip()) > 0:
            user = cache.get(token)
            if user:
                try:
                    user = json.loads(user)
                    user_id = user[0]['pk']
                    school_id_list = SchoolUser.objects.values_list('school_id', flat=True).\
                        filter(user_id=user_id, schooluserrole__role__temp=SCHOOL_ROLE_TEACHER, deleted=0,
                               school__deleted=0, user__deleted=0, schooluserrole__role__deleted=0)
                    if school_id_list:
                        school_id_list = list(school_id_list)
                    return func(request, user, school_id_list, *args, **kw)
                except Exception as e:
                    print("检查老师装饰器报错:%s" % e)
                    return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})
            else:
                return JsonResponse({'code': False, 'error_code': 'not_login', 'msg': '未登录'})

    return check_teacher_handle


# from 验证render forms = [from对象, '验证失败跳转url']
def valid_form_render(forms):
    def _valid(func):
        def __valid(self, request, *args, **kwargs):
            if forms[0].is_valid():
                return func(self, request, *args, **kwargs)
            else:
                return render(request, forms[1], {'code': False, 'msg': '表单验证失败', 'forms': forms[0]})
        return __valid
    return _valid


# from 验证ajax forms = form对象
def valid_form_ajax(forms):
    def _valid(func):
        def __valid(self, request, *args, **kwargs):
            if forms.is_valid():
                return func(self, request, *args, **kwargs)
            else:
                return JsonResponse()
        return __valid
    return _valid
