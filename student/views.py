import datetime

from django.shortcuts import render

from Utils.wrappers import permitted_methods
from student.models import Student
from student.models import Instructor_Student
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from Utils.tools import paginator2dict
from Utils.midd import errMsg
from http import HTTPStatus
from Utils.tools import request_body_serialize_init
from .models import DepartAdmin


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


@permitted_methods(["POST"])
def student_import(request):
    stu_mes = request_body_serialize_init(request)
    userId = '20130053'
    userName = 'Tang'
    relations2 = Student.objects.filter(xh=stu_mes.get("xh"))
    if len(relations2) >0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生已存在'},json_dumps_params={'ensure_ascii': False})
    if stu_mes.get("xh")==None or stu_mes.get("name")==None or stu_mes.get("xq")==None or stu_mes.get("sfzx")==None or stu_mes.get("cc")==None or stu_mes.get("glyx")==None or stu_mes.get("instructor_name")==None or stu_mes.get("instructor_num")==None:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '参数不全，字段不齐'},json_dumps_params={'ensure_ascii': False})
    relations3 = DepartAdmin.objects.filter(zgh=stu_mes.get("instructor_num"))
    if (len(relations3) == 0):
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该辅导员不存在'},
                            json_dumps_params={'ensure_ascii': False})
    Student.objects.create(xh=stu_mes.get("xh"),xm=stu_mes.get("name"),xq=stu_mes.get("xq"),sfzx=stu_mes.get("sfzx"),sfzj=True,
                           cc=stu_mes.get("cc"),glyx=stu_mes.get("glyx"),sfdr=True,sftb=False)
    Instructor_Student.objects.create(zgh=stu_mes.get("instructor_num"),xm=stu_mes.get("instructor_name"),xh=stu_mes.get("xh"))
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def student_change(request):
    stu_mes = request_body_serialize_init(request)
    relations = Student.objects.filter(xh=stu_mes.get("xh"))
    if len(relations) == 0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生不存在'}, json_dumps_params={'ensure_ascii': False})
    elif len(relations) >1 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '存在多个相同学号的学生'},json_dumps_params={'ensure_ascii': False})
    for item in stu_mes.keys():
        if item == "name":
            relations[0].xm = stu_mes.get(item)
        elif item == "xq":
            relations[0].xq = stu_mes.get(item)
        elif item == "sfzx":
            relations[0].sfzx = stu_mes.get(item)
        elif item == "cc":
            relations[0].cc = stu_mes.get(item)
        elif item == "glyx":
            relations[0].glyx = stu_mes.get(item)
        elif item == "instructor_name" or "instructor_num":
            relations2 = Instructor_Student.objects.filter(xh = stu_mes.get("xh"))
            if item == "instructor_name":
                if len(relations2)==0:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生不存在'},json_dumps_params={'ensure_ascii': False})
                elif len(relations2)>1:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '存在多个相同学号的学生'},json_dumps_params={'ensure_ascii': False})
                else:
                    relations2[0].xm = stu_mes.get(item)
            elif item == "instructor_num":
                if len(relations2)==0:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生不存在'},json_dumps_params={'ensure_ascii': False})
                elif len(relations2)>1:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '存在多个相同学号的学生'},json_dumps_params={'ensure_ascii': False})
                else:
                    relations2[0].zgh = stu_mes.get(item)
                    relations2[0].save()
    relations[0].save()
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})