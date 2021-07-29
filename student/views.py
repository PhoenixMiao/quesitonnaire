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
from Utils.tools import request_body_serialize3
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
    stu_mes = request_body_serialize3(request)
    userId = '20130053'
    userName = 'Tang'
    relations = Instructor_Student.objects.filter(zgh=userId)
    xhs = [ele.xh for ele in relations]
    if xhs.count(stu_mes.get("学号"))>0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生已存在'}, json_dumps_params={'ensure_ascii': False})
    relations2 = Student.objects.filter(xh=stu_mes.get("学号"))
    if len(relations2) >0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生已存在'},json_dumps_params={'ensure_ascii': False})
    Student.objects.create(xh=stu_mes.get("学号"),xm=stu_mes.get("姓名"),xq=stu_mes.get("校区"),sfzx=stu_mes.get("是否在校"),sfzj=True,
                           cc=stu_mes.get("学历层次"),glyx=stu_mes.get("管理院系"),sfdr=True,sftb=False)
    Instructor_Student.objects.create(zgh=stu_mes.get("辅导员职工号"),xm=stu_mes.get("辅导员姓名"),xh=stu_mes.get("学号"))
    relations3 = DepartAdmin.objects.filter(zgh=stu_mes.get("辅导员职工号"))
    if(len(relations3)==0):
        DepartAdmin.objects.create(zgh=stu_mes.get("辅导员职工号"),xm=stu_mes.get("辅导员姓名"),)
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def student_change(request):
    stu_mes = request_body_serialize3(request)
    relations = Student.objects.filter(xh=stu_mes.get("学号"))
    if len(relations) == 0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生不存在'}, json_dumps_params={'ensure_ascii': False})
    elif len(relations) >1 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '存在多个相同学号的学生'},json_dumps_params={'ensure_ascii': False})
    stu = relations[0]
    for item in stu_mes.keys():
        if item == "姓名":
            stu.xm = stu_mes.get(item)
        elif item == "校区":
            stu.xq = stu_mes.get(item)
        elif item == "是否在校":
            stu.sfzx = stu_mes.get(item)
        elif item == "学历":
            stu.cc = stu_mes.get(item)
        elif item == "管理院系":
            stu.glyx = stu_mes.get(item)
        elif item == "辅导员姓名" or "辅导员工号":
            if item == "辅导员姓名":
                relations2 = Instructor_Student.objects.filter(xh = stu_mes.get("学号"))
                if len(relations2)==0:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生不存在'},json_dumps_params={'ensure_ascii': False})
                elif len(relations2)>1:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '存在多个相同学号的学生'},json_dumps_params={'ensure_ascii': False})
                else:
                    stuin = relations2[0]
                    stuin.xm = stu_mes.get(item)
            elif  item == "辅导员工号":
                relations2 = Instructor_Student.objects.filter(xh = stu_mes.get("学号"))
                if len(relations2)==0:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生不存在'},json_dumps_params={'ensure_ascii': False})
                elif len(relations2)>1:
                    return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '存在多个相同学号的学生'},json_dumps_params={'ensure_ascii': False})
                else:
                    stuin = relations2[0]
                    stuin.zgh = stu_mes.get(item)
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})