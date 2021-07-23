from poll.models import Questionnaire, Whilelist
from django.http import JsonResponse
from http import HTTPStatus
from django.forms.models import model_to_dict
from Utils.wrappers import permitted_methods
from Utils.tools import request_body_serialze


@permitted_methods(["GET"])
# TODO
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
        # TODO
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
# TODO
def whitelist(request, pollId):
    page_num = request.GET.get('p', 1)
    length = request.GET.get('l', 15)
    # TODO 可以参照student.views.student
    ret = {'message': 'ok'}
    return JsonResponse(data=ret, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["DELETE"])
def whitelist_delete(request, pollId):
    vars = request_body_serialze(request)
    if "xh" not in vars.keys():
        return JsonResponse(status=HTTPStatus.NOT_ACCEPTABLE, data={'error': '缺少参数'},
                            json_dumps_params={'ensure_ascii': False})
    whitelist = Whilelist.objects.filter(questionnaireId=pollId, xh=vars['xh'])
    if len(whitelist) == 0:
        return JsonResponse(status=HTTPStatus.NO_CONTENT, data={'error': '白名单或名单中学号不存在'},
                            json_dumps_params={'ensure_ascii': False})
    whitelist.delete()
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})


@permitted_methods(["POST"])
# TODO
def whitelist_import(request, pollId):
    # TODO 可以参考https://docs.djangoproject.com/zh-hans/3.0/topics/http/file-uploads/
    return JsonResponse(data={'message': 'ok'}, json_dumps_params={'ensure_ascii': False})
