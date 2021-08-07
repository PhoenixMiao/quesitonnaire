from poll.models import Questionnaire, Whitelist, Blacklist,Record
from django.http import JsonResponse
from http import HTTPStatus
from django.forms.models import model_to_dict
from Utils.wrappers import permitted_methods
from Utils.tools import request_body_serialize,request_body_serialize_init
from django.core.paginator import Paginator,EmptyPage
from student.models import Student
from Utils.tools import paginator2dict
from Utils.fileTool import upload_file


@permitted_methods(["GET"])
def polls(request, type):
    if type == '' or type is None:
        # 获取未归档的问卷列表
        questionnaires = Questionnaire.objects.exclude(status=-1)
        questionnaires_dict = [model_to_dict(ele, fields=["id", "title", "creatorId", "oneoff", "status",
                                                          "createTime", "updateTime"]) for ele in questionnaires]
        return JsonResponse(data={'message': 'ok', 'data': questionnaires_dict}, json_dumps_params={'ensure_ascii': False})
    elif type == 'archive':
        # 获取已归档的问卷列表：
        questionnaires = Questionnaire.objects.filter(status=-1)
        questionnaires_dict = [model_to_dict(ele,fields=["id","title","creatorId","oneoff","status","createTime","updateTime"]) for ele in questionnaires]
        return JsonResponse(data={"message":"ok", "data":questionnaires_dict}, json_dumps_params={'ensure_ascii':False})
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
    fields = ["status", "oneoff", "title", "scope", "creatorId", "createTime"]
    for i in range(1, 21):
        if getattr(questionnaire, "k" + str(i)) is not None:
            fields.append("k" + str(i))
    mod = model_to_dict(questionnaire, fields=fields)
    ret = {'message': 'ok',
           'data': mod}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def whitelist(request, pollId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 15)
    relations = Whitelist.objects.filter(questionnaireId=pollId)
    xhs = [ele.xh for ele in relations]
    student = Student.objects.filter(xh__in=xhs).order_by('xh')
    paginator = Paginator(student,length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT,data = {"error":"没有该页面"},json_dumps_params={'ensure_ascii':False})
    ret = {'message': 'ok',
           'data':paginator2dict(paginator_page,["xh","xm","glyx"])}
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
    # TODO 可以参考https://docs.djangoproject.com/zh-hans/3.0/topics/http/file-uploads/
    xhs = upload_file(request)
    if xhs[0] == False :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': xhs[1]},
                            json_dumps_params={'ensure_ascii': False})
    else:
        xhs.remove("学号")
        for xh in xhs:
            whitelist = Whitelist.objects.filter(questionnaireId=pollId,xh=xh)
            if len(whitelist) == 0 :
                Whitelist.objects.create(questionnaireId=pollId,xh=xh)
        return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["GET"])
def blacklist(request, pollId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 15)
    relations = Blacklist.objects.filter(questionnaireId=pollId)
    xhs = [ele.xh for ele in relations]
    student = Student.objects.filter(xh__in=xhs).order_by('xh')
    paginator = Paginator(student,length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT,data = {"error":"没有该页面"},json_dumps_params={'ensure_ascii':False})
    ret = {'message': 'ok',
           'data':paginator2dict(paginator_page,["xh","xm","glyx"])}
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
    xhs = upload_file(request)
    if xhs[0] == False :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': xhs[1]},
                            json_dumps_params={'ensure_ascii': False})
    else:
        xhs.remove("学号")
        for xh in xhs:
            blacklist = Blacklist.objects.filter(questionnaireId=pollId,xh=xh)
            if len(blacklist) == 0 :
                Blacklist.objects.create(questionnaireId=pollId,xh=xh)
        return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


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
    Questionnaire.objects.create(status=status,oneoff=oneoff,title=title,scope=scope,creatorId=creatorId,
                                 k1=sub_body_list[0],k2=sub_body_list[1],k3=sub_body_list[2],k4=sub_body_list[3],
                                 k5=sub_body_list[4],k6=sub_body_list[5],k7=sub_body_list[6],k8=sub_body_list[7],
                                 k9=sub_body_list[8],k10=sub_body_list[9],k11=sub_body_list[10],k12=sub_body_list[11],
                                 k13=sub_body_list[12],k14=sub_body_list[13],k15=sub_body_list[14],k16=sub_body_list[15],
                                 k17=sub_body_list[16],k18=sub_body_list[17],k19=sub_body_list[18],k20=sub_body_list[19])
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
def poll_activate(request,pollId):
    questionnaires = Questionnaire.objects.filter(id=pollId)
    if len(questionnaires) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该问卷'},
                            json_dumps_params={'ensure_ascii': False})
    else:
        questionnaire = questionnaires[0];
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
        questionnaire = questionnaires[0];
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



@permitted_methods(["GET"])
def meta(request,recordId):
    records = Record.objects.filter(id=recordId)
    if len(records) == 0 :
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该记录（未填写问卷）'},
                            json_dumps_params={'ensure_ascii': False})
    rec = records[0]
    fields = ["id","xh","questionnaireId","createTime","updateTime"]
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
def records(request,questionnaireId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 5)
    rec = Record.objects.filter(questionnaireId=questionnaireId)
    body_list = request_body_serialize_init(request)
    for item in body_list.keys():
        if item == 'xh' :
            rec = Record.objects.filter(questionnaireId=questionnaireId,xh=body_list.get('xh'))
        elif item == 'name':
            for ele in rec:
                student = Student.objects.filter(xh=ele.xh)
                if student.get('name') != body_list.get('name'):
                    rec.remove(ele)
    paginator = Paginator(rec, length)
    try:
        paginator_page = paginator.page(page_num)
    except EmptyPage:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '没有该页面'}, json_dumps_params={'ensure_ascii': False})
    ret = {'message': 'ok',
           'data': paginator2dict(paginator_page, ["id", "xh", "questionnaireId", "createTime", "updateTime"])}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})
