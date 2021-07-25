from django.shortcuts import render
from student.models import Student
from student.models import Instructor_Student
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from Utils.tools import paginator2dict
from Utils.midd import errMsg
from http import HTTPStatus


def student(request):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 5)
    userId = '20130053'
#    permission = '4'
    relations = Instructor_Student.objects.filter(zgh=userId)
    xhs = [ele.xh for ele in relations]
    students = Student.objects.filter(xh__in=xhs).order_by('xh')
    paginator = Paginator(students, length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该页面'}, json_dumps_params={'ensure_ascii': False})
    ret = {'message': 'ok',
           'data': paginator2dict(paginator_page, ["xh", "xm", 'cc', 'glyx', 'glyxm', 'sftb', 'sfdr', 'sfzj', 'sfzx', 'xq', ])}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})

