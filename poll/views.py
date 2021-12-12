from poll.models import Questionnaire, Whitelist, Blacklist,Record,HistoryRecord,Condition
from django.http import JsonResponse
from http import HTTPStatus
from django.forms.models import model_to_dict
from Utils.wrappers import permitted_methods
from Utils.tools import request_body_serialize,request_body_serialize_init
from django.core.paginator import Paginator,EmptyPage
from student.models import Student
from Utils.tools import paginator2dict,paginator3dict,paginator4dict,paginator5dict,paginator6dict
from Utils.fileTool import upload_file
import xlwt
import io, csv, codecs
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl import load_workbook

import pandas as pd


@permitted_methods(["GET"])
def polls(request, type):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 15)
    if type == '' or type is None:
        # 获取未归档的问卷列表
        questionnaires = Questionnaire.objects.exclude(status=-1)
        paginator = Paginator(questionnaires, length)
        try:
            paginator_page = paginator.page(page_num)
        except EmptyPage:
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "没有该页面"},
                                json_dumps_params={'ensure_ascii': False})
        ret = {'message': 'ok',
               'data': paginator4dict(paginator_page, ["id", "title", "creatorId", "oneoff", "status",'createTime','updateTime'])}
        return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})
    elif type == 'archive':
        # 获取已归档的问卷列表：
        questionnaires = Questionnaire.objects.filter(status=-1)
        paginator = Paginator(questionnaires, length)
        try:
            paginator_page = paginator.page(page_num)
        except EmptyPage:
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "没有该页面"},
                                json_dumps_params={'ensure_ascii': False})
        ret = {'message': 'ok',
               'data': paginator5dict(paginator_page,["id", "title", "creatorId", "oneoff", "status", 'createTime', 'updateTime'])}
        return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '参数错误'},
                            json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def meta(request, pollId):
    questionnaires = Questionnaire.objects.filter(id=pollId)
    if len(questionnaires) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该问卷'},
                            json_dumps_params={'ensure_ascii': False})
    questionnaire = questionnaires[0]
    fields = ["status", "oneoff", "title", "scope", "creatorId"]
    for i in range(1, 21):
        if getattr(questionnaire, "k" + str(i)) is not None:
            fields.append("k" + str(i))
    mod = model_to_dict(questionnaire, fields=fields)
    mod['createTime'] = questionnaire.createTime.strftime("%Y-%m-%d %H:%M")
    mod['updateTime'] = questionnaire.updateTime.strftime("%Y-%m-%d %H:%M")
    ret = {'message': 'ok',
           'data': mod}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def whitelist_search(request,pollId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 15)
    vars = request_body_serialize(request)
    whiteList = Whitelist.objects.filter(xh__icontains=vars['xh'],questionnaireId=pollId)
    if(len(whiteList)==0):
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "该学生并不在白名单内"},
                            json_dumps_params={'ensure_ascii': False})
    paginator = Paginator(whiteList,length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "没有该页面"},
                            json_dumps_params={'ensure_ascii': False})
    ret = {'message': 'ok',
           'data': paginator6dict(paginator_page,['questionnaireId','xh'])}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["DELETE"])
def whitelist_delete(request, pollId):
    vars = request_body_serialize(request)
    if "xh" not in vars.keys():
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '缺少参数'},
                            json_dumps_params={'ensure_ascii': False})
    whitelist = Whitelist.objects.filter(questionnaireId=pollId, xh=vars['xh'])
    if len(whitelist) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '白名单或名单中学号不存在'},
                            json_dumps_params={'ensure_ascii': False})
    whitelist.delete()
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def whitelist_import(request, pollId):
    tmpFile = request.FILES.get('whitelist')
    workbook_ = load_workbook(tmpFile)
    sheetnames = workbook_.get_sheet_names()
    sheet = workbook_.get_sheet_by_name(sheetnames[0])
    j=2
    tmp = sheet.cell(row=2,column=1).value
    while tmp:
        student = Student.objects.filter(xh=tmp)
        if (len(student) == 0):
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "没有该学生"},
                                json_dumps_params={'ensure_ascii': False})
        blacklist = Blacklist.objects.filter(xh=tmp)
        if (len(blacklist) != 0):
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "该学生已经在黑名单里了"},
                                json_dumps_params={'ensure_ascii': False})
        Whitelist.objects.create(questionnaireId=pollId, xh=tmp)
        j = j+1
        tmp = sheet.cell(row=j,column=1).value
    return JsonResponse(data={'message':'ok'}, json_dumps_params={'ensure_ascii': False})



@permitted_methods(["POST"])
def blacklist_search(request,pollId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 15)
    vars = request_body_serialize(request)
    blackList = Blacklist.objects.filter(xh__icontains=vars['xh'],questionnaireId=pollId)
    if(len(blackList)==0):
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "该学生并不在黑名单内"},
                            json_dumps_params={'ensure_ascii': False})
    paginator = Paginator(blackList,length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "没有该页面"},
                            json_dumps_params={'ensure_ascii': False})
    ret = {'message': 'ok',
           'data': paginator6dict(paginator_page,['questionnaireId','xh'])}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["DELETE"])
def blacklist_delete(request, pollId):
    vars = request_body_serialize(request)
    if "xh" not in vars.keys():
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '缺少参数'},
                            json_dumps_params={'ensure_ascii': False})
    blacklist = Blacklist.objects.filter(questionnaireId=pollId, xh=vars['xh'])
    if len(blacklist) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '白名单或名单中学号不存在'},
                            json_dumps_params={'ensure_ascii': False})
    blacklist.delete()
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def blacklist_import(request, pollId):
    # reader = csv.reader(request)
    tmpFile = request.FILES.get('blacklist')
    workbook_ = load_workbook(tmpFile)
    sheetnames = workbook_.get_sheet_names()
    sheet = workbook_.get_sheet_by_name(sheetnames[0])
    j=2
    tmp = sheet.cell(row=2,column=1).value
    while tmp:
        student = Student.objects.filter(xh=tmp)
        if (len(student) == 0):
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "没有该学生"},
                                json_dumps_params={'ensure_ascii': False})
        whitelist = Whitelist.objects.filter(xh=tmp)
        if (len(whitelist) != 0):
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={"error": "该学生已经在白名单里了"},
                                json_dumps_params={'ensure_ascii': False})
        Blacklist.objects.create(questionnaireId=pollId, xh=tmp)
        j = j+1
        tmp = sheet.cell(row=j,column=1).value
    return JsonResponse(data={'message':'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def poll_create(request):
    body_list = request_body_serialize_init(request)
    status = int(body_list.get("status"))
    oneoff = int(body_list.get("oneoff"))
    title = body_list.get("title")
    scope = int(body_list.get("scope"))
    creatorId = '20130053'
    sub_body_list = list(body_list.values())[list(body_list.keys()).index("1"):]
    size = len(sub_body_list)
    for i in range(size+1,21):
        sub_body_list.append(None)
    Questionnaire.objects.create(status=status, oneoff=oneoff,title=title, scope=scope, creatorId=creatorId,
                                 k1=sub_body_list[0], k2=sub_body_list[1], k3=sub_body_list[2], k4=sub_body_list[3],
                                 k5=sub_body_list[4], k6=sub_body_list[5], k7=sub_body_list[6], k8=sub_body_list[7],
                                 k9=sub_body_list[8], k10=sub_body_list[9], k11=sub_body_list[10], k12=sub_body_list[11],
                                 k13=sub_body_list[12], k14=sub_body_list[13], k15=sub_body_list[14], k16=sub_body_list[15],
                                 k17=sub_body_list[16], k18=sub_body_list[17], k19=sub_body_list[18], k20=sub_body_list[19])
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def poll_activate(request,pollId):
    questionnaires = Questionnaire.objects.filter(id=pollId)
    if len(questionnaires) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该问卷'},
                            json_dumps_params={'ensure_ascii': False})
    else:
        questionnaire = questionnaires[0]
        if questionnaire.status == 0 or questionnaire.status == 2:
           questionnaires[0].status = 1
        elif questionnaire.status == 1:
            return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷已经在发布状态'},
                            json_dumps_params={'ensure_ascii': False})
        elif questionnaire.status == -1:
            return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷已归档'},
                            json_dumps_params={'ensure_ascii': False})
        questionnaires[0].save()
        return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def poll_pause(request,pollId):
    questionnaires = Questionnaire.objects.filter(id=pollId)
    if len(questionnaires) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该问卷'},
                            json_dumps_params={'ensure_ascii': False})
    else:
        questionnaire = questionnaires[0]
        if questionnaire.status == 1:
           questionnaires[0].status = 2
        elif questionnaire.status == 2:
            return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷已经暂停发布'},
                            json_dumps_params={'ensure_ascii': False})
        elif questionnaire.status == 0:
            return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷仍在草稿状态'},
                            json_dumps_params={'ensure_ascii': False})
        elif questionnaire.status == -1:
            return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷已归档'},
                            json_dumps_params={'ensure_ascii': False})
        questionnaires[0].save()
        return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def record_add_judge(request):
    body_list = request_body_serialize_init(request)
    xh = body_list.get('xh')
    questionnaire_id = body_list.get('questionnaireId')
    questionnaires = Questionnaire.objects.filter(id=questionnaire_id)
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    if len(questionnaires) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该问卷'},
                            json_dumps_params={'ensure_ascii': False})
    stu = Student.objects.filter(xh=xh)
    if len(stu)==0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该学生'},
                            json_dumps_params={'ensure_ascii': False})
    whitelist = Whitelist.objects.filter(questionnaireId=questionnaire_id,xh=xh)
    blacklist = Blacklist.objects.filter(questionnaireId=questionnaire_id,xh=xh)
    if len(whitelist)==0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生并不在白名单内'},
                            json_dumps_params={'ensure_ascii': False})
    if len(blacklist)!=0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '该学生并在黑名单内'},
                            json_dumps_params={'ensure_ascii': False})
    questionnaire_dic = model_to_dict(questionnaire)
    if questionnaire_dic.get("status") != 1:
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷并不在发布状态'},
                            json_dumps_params={'ensure_ascii': False})
    recorded = Record.objects.filter(questionnaireId=questionnaire_id,xh=xh)
    if len(recorded) != 0:
        if questionnaire_dic.get("oneoff") == 0:
            return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷一人一份，只能修改单人记录'},
                                json_dumps_params={'ensure_ascii': False})
    return JsonResponse(data={'message': '该学生可以填写问卷'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def record_add(request):
    body_list = request_body_serialize_init(request)
    xh = body_list.get('xh')
    questionnaire_id = body_list.get('questionnaireId')
    sub_body_list = list(body_list.values())[list(body_list.keys()).index("v1"):]
    size = len(sub_body_list)
    for i in range(size+1,21):
        sub_body_list.append(None)
    Record.objects.create(xh=xh, questionnaireId=questionnaire_id,
                                 v1=sub_body_list[0], v2=sub_body_list[1], v3=sub_body_list[2], v4=sub_body_list[3],
                                 v5=sub_body_list[4], v6=sub_body_list[5], v7=sub_body_list[6], v8=sub_body_list[7],
                                 v9=sub_body_list[8], v10=sub_body_list[9], v11=sub_body_list[10],
                                 v12=sub_body_list[11],
                                 v13=sub_body_list[12], v14=sub_body_list[13], v15=sub_body_list[14],
                                 v16=sub_body_list[15],
                                 v17=sub_body_list[16], v18=sub_body_list[17], v19=sub_body_list[18],
                                 v20=sub_body_list[19])
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def record_change(request):
    body_list = request_body_serialize_init(request)
    xh = body_list.get('xh')
    questionnaire_id = body_list.get('questionnaireId')
    recs = Record.objects.filter(xh=xh,questionnaireId=questionnaire_id)
    record = Record.objects.get(xh=xh,questionnaireId=questionnaire_id)
    if len(recs) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该记录（未填写问卷）'},
                            json_dumps_params={'ensure_ascii': False})
    questionnaire_dic = model_to_dict(Questionnaire.objects.get(id=questionnaire_id))
    if questionnaire_dic.get("oneoff") == 1:
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷是一次性问卷，不能修改记录'},
                            json_dumps_params={'ensure_ascii': False})
    for item in body_list.keys():
        if item == "v1":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v1"))
        if item == "v2":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v2"))
        if item == "v3":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v3"))
        if item == "v4":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v4"))
        if item == "v5":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v5"))
        if item == "v6":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v6"))
        if item == "v7":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v7"))
        if item == "v8":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v8"))
        if item == "v9":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v9"))
        if item == "v10":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v10"))
        if item == "v11":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v11"))
        if item == "v12":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v12"))
        if item == "v13":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v13"))
        if item == "v14":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v14"))
        if item == "v15":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v15"))
        if item == "v16":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v16"))
        if item == "v17":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v17"))
        if item == "v18":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v18"))
        if item == "v19":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v19"))
        if item == "v20":
            Record.objects.filter(xh=xh, questionnaireId=questionnaire_id).update(v1=body_list.get("v20"))
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})



@permitted_methods(["GET"])
def record_meta(request,recordId):
    record = Record.objects.filter(id=recordId)
    if len(record) == 0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该记录（未填写问卷）'},
                            json_dumps_params={'ensure_ascii': False})
    rec = record[0]
    rec_use = model_to_dict(rec)
    que = model_to_dict(Questionnaire.objects.get(id=rec_use.get("questionnaireId")))
    fields = ["id","xh","questionnaireId"]
    keys = ["id","xh","questionnaireId"]
    for i in range(1, 21):
        tmp = str(i)
        if getattr(rec, "v" + tmp) is not None:
            keys.append(que.get("k" + tmp))
            fields.append("v" + tmp)
    tmp = model_to_dict(rec,fields=fields).values()
    mod = dict(zip(keys,tmp))
    ret = {'message': 'ok','data': mod}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def records(request,questionnaireId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 5)
    rec = Record.objects.filter(questionnaireId=questionnaireId)
    body_list = request_body_serialize_init(request)
    for item in body_list.keys():
        if item == 'xh' :
            rec = Record.objects.filter(questionnaireId=questionnaireId,xh__icontains=body_list.get('xh'))
        # elif item == 'name':
        #     for ele in rec:
        #         student = Student.objects.filter(xh=ele.xh)
        #         if student.get('name') != body_list.get('name'):
        #             rec.remove(ele)
    paginator = Paginator(rec, length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该页面'}, json_dumps_params={'ensure_ascii': False})
    ret = {'message': 'ok',
           'data': paginator2dict(paginator_page, ["id", "xh", "questionnaireId","v1","v2","v3"])}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def history_meta(request,recordId):
    record = HistoryRecord.objects.filter(id=recordId)
    if len(record) == 0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该归档记录'},
                            json_dumps_params={'ensure_ascii': False})
    rec = record[0]
    rec_use = model_to_dict(rec)
    que = model_to_dict(Questionnaire.objects.get(id=rec_use.get("questionnaireId")))
    fields = ["id","xh","questionnaireId"]
    keys = ["id","xh","questionnaireId"]
    for i in range(1, 21):
        tmp = str(i)
        if getattr(rec, "v" + tmp) is not None:
            keys.append(que.get("k" + tmp))
            fields.append("v" + tmp)
    tmp = model_to_dict(rec,fields=fields).values()
    mod = dict(zip(keys,tmp))
    ret = {'message': 'ok','data': mod}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def history_records(request,questionnaireId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 5)
    rec = HistoryRecord.objects.filter(questionnaireId=questionnaireId)
    body_list = request_body_serialize_init(request)
    for item in body_list.keys():
        if item == 'xh' :
            rec = HistoryRecord.objects.filter(questionnaireId=questionnaireId,xh__icontains=body_list.get('xh'))
        # elif item == 'name':
        #     for ele in rec:
        #         student = Student.objects.filter(xh=ele.xh)
        #         if student.get('name') != body_list.get('name'):
        #             rec.remove(ele)
    paginator = Paginator(rec, length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该页面'}, json_dumps_params={'ensure_ascii': False})
    ret = {'message': 'ok',
           'data': paginator2dict(paginator_page, ["id", "xh", "questionnaireId","v1","v2","v3"])}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def dynamic_filtering(request,questionnaireId):
    relations = Whitelist.objects.filter(questionnaireId=questionnaireId)
    xhs = [ele.xh for ele in relations]
    students = Student.objects.filter(xh__in=xhs).order_by('xh')
    # res = model_to_dict(students,fields=['xh','xm','glyx','cc'])
    conditions = Condition.objects.filter(questionnaireId=questionnaireId)
    tmp = []
    contants = " student "
    for ele in conditions:
        tmp.append(model_to_dict(ele,fields=['key','values']))
    for ele in tmp:
        value = '"'+ele['values']+'"'
        l ="SELECT * FROM" + contants + "WHERE "+ele['key']+" = "+value
        students = students.raw(l)
        if len(students)==0:
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有符合条件的学生'}, json_dumps_params={'ensure_ascii': False})
    res = []
    for ele in students:
        res.append(model_to_dict(ele,fields=['xh','xm','xq','glyx']))
    ret = {'message': 'ok', 'data': res}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})

@permitted_methods(["GET"])
def dynamic_fileDown(request,questionnaireId):
    relations = Whitelist.objects.filter(questionnaireId=questionnaireId)
    xhs = [ele.xh for ele in relations]
    students = Student.objects.filter(xh__in=xhs).order_by('xh')
    # res = model_to_dict(students,fields=['xh','xm','glyx','cc'])
    conditions = Condition.objects.filter(questionnaireId=questionnaireId)
    tmp = []
    contants = " student "
    for ele in conditions:
        tmp.append(model_to_dict(ele,fields=['key','values']))
    for ele in tmp:
        value = '"'+ele['values']+'"'
        l ="SELECT * FROM" + contants + "WHERE "+ele['key']+" = "+value
        students = students.raw(l)
        if len(students)==0:
            return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有符合条件的学生'}, json_dumps_params={'ensure_ascii': False})
    res = []
    for ele in students:
        res.append(model_to_dict(ele,fields=['xh','xm','xq','glyx']))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=dynamic.csv'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(["学号","姓名","校区","管理院系"])
    for ele in res:
        writer.writerow([ele.get('xh'),ele.get('xm'),ele.get('xq'),ele.get('glyx')])
    return response


@permitted_methods(["POST"])
def file(request,questionnaireId):
    questionnaires = Questionnaire.objects.filter(id=questionnaireId)
    questionnaire = questionnaires[0]
    if questionnaire.status == 1 or questionnaire.status == 2:
        Questionnaire.objects.filter(id=questionnaireId).update(status=-1)
    elif questionnaire.status == 0:
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷仍在草稿状态'},
                            json_dumps_params={'ensure_ascii': False})
    elif questionnaire.status == -1:
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '该问卷已归档'},
                            json_dumps_params={'ensure_ascii': False})
    recs = Record.objects.filter(questionnaireId=questionnaireId)
    HistoryRecord.objects.bulk_create(recs)
    Record.objects.filter(questionnaireId=questionnaireId).delete()
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def templateFiles(request, type):
    if type == "whitelist":
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment;filename=whitelist.xlsx'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(["学号"])
        writer.writerow(["10204xxxxx"])
        return response
    elif type == "blacklist":
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment;filename=blacklist.xlsx'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(["学号"])
        writer.writerow(["10204xxxxx"])
        return response
    elif type == "student":
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment;filename=student.xlsx'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(["学号",'姓名','校区','是否在校','是否在籍','学历层次','管理院系','管理院系码','辅导员姓名','辅导员职工号'])
        writer.writerow(["10204xxxxx",'张三','中北校区','是','是','本科生','软件工程','10010','李四','100300'])
        return response
    else:
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '参数错误'},
                            json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def fileDown(request,questionnaireId):
    questionnaire = Questionnaire.objects.get(id=questionnaireId)
    if questionnaire:
        mes = model_to_dict(questionnaire,fields=['id','status','oneoff','title','scope','creatorId','createTime','updateTime','k1','k2','k3','k4','k5','k6','k7','k8','k9','k10','k11','k12','k13','k14','k15','k16','k17','k18','k19','k20'])
        if mes.get('status') != -1 :
            records = Record.objects.filter(id=questionnaireId)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename=record.csv'
            response.write(codecs.BOM_UTF8)
            writer = csv.writer(response)
            writer.writerow(["序号","学号", "创建时间", "更新时间", mes.get('k1'), mes.get('k2'), mes.get('k3'), mes.get('k4'), mes.get('k4'), mes.get('k5'), mes.get('k6'), mes.get('k7'), mes.get('k8'), mes.get('k9'), mes.get('k10'),
                   mes.get('k11'),mes.get('k12'),mes.get('k13'),mes.get('k14'),mes.get('k15'),mes.get('k16'),mes.get('k17'),mes.get('k18'),mes.get('k19'),mes.get('k20')])
            j = 1
            for record in records:
                tmp = model_to_dict(record,fields=['xh','createTime','updateTime','v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19','v20'])
                tmp['createTime'] = record.createTime.strftime("%Y-%m-%d %H:%M")
                tmp['updateTime'] = record.updateTime.strftime("%Y-%m-%d %H:%M")
                writer.writerow([j,tmp.get('xh'),tmp.get('createTime'),tmp.get('updateTime'),tmp.get('v1'),tmp.get('v2'),tmp.get('v3'),tmp.get('v4'),tmp.get('v5'),tmp.get('v6'),tmp.get('v7'),tmp.get('v8'),tmp.get('v8'),tmp.get('v9'),tmp.get('v9'),tmp.get('v10'),tmp.get('v11'),tmp.get('v12'),tmp.get('v13'),tmp.get('v14'),tmp.get('v15'),tmp.get('v16'),tmp.get('v17'),tmp.get('v18'),tmp.get('v19'),tmp.get('v20')])
                j = j+1
        else:
            history_records = HistoryRecord.objects.filter(questionnaireId=questionnaireId)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename=history_record.csv'
            response.write(codecs.BOM_UTF8)
            writer = csv.writer(response)
            writer.writerow(
                ["序号", "学号", "创建时间", "更新时间",mes.get('k1'), mes.get('k2'), mes.get('k3'), mes.get('k4'), mes.get('k4'),
                 mes.get('k5'), mes.get('k6'), mes.get('k7'), mes.get('k8'), mes.get('k9'), mes.get('k10'),
                 mes.get('k11'), mes.get('k12'), mes.get('k13'), mes.get('k14'), mes.get('k15'), mes.get('k16'),
                 mes.get('k17'), mes.get('k18'), mes.get('k19'), mes.get('k20')])
            j = 1
            for history_record in history_records:
                tmp = model_to_dict(history_record,
                                    fields=['xh', 'createTime', 'updateTime', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7',
                                            'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18',
                                            'v19', 'v20'])
                tmp['createTime'] = history_record.createTime.strftime("%Y-%m-%d %H:%M")
                tmp['updateTime'] = history_record.updateTime.strftime("%Y-%m-%d %H:%M")
                writer.writerow(
                    [j, tmp.get('xh'), tmp.get('createTime'), tmp.get('updateTime'), tmp.get('v1'), tmp.get('v2'),
                     tmp.get('v3'), tmp.get('v4'), tmp.get('v5'), tmp.get('v6'), tmp.get('v7'), tmp.get('v8'),
                     tmp.get('v8'), tmp.get('v9'), tmp.get('v9'), tmp.get('v10'), tmp.get('v11'), tmp.get('v12'),
                     tmp.get('v13'), tmp.get('v14'), tmp.get('v15'), tmp.get('v16'), tmp.get('v17'), tmp.get('v18'),
                     tmp.get('v19'), tmp.get('v20')])
                j = j + 1
    return response
