from django.forms.models import model_to_dict
from django.http.request import QueryDict
from poll.models import Questionnaire, Whitelist, Blacklist,Record,HistoryRecord,Condition
from student.models import Student
import json

# 将Paginator对象转换为dict
# fields参数用于model_to_dict函数的fields参数
def paginator2dict(page, fields=[]):
    result = {
        'list': [],
        'count': page.paginator.count,
        'page_num': page.paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_num': page.previous_page_number() if page.has_previous() else 1,
        'next_page_num': page.next_page_number() if page.has_next() else page.paginator.num_pages
    }
    eles = []
    for obj in page.object_list:
        eles.append(model_to_dict(obj, fields=fields))
    result['list'] = eles
    return result

def paginator3dict(page,fields=[]):
    result = {
        'list': [],
        'count': page.paginator.count,
        'page_num': page.paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_num': page.previous_page_number() if page.has_previous() else 1,
        'next_page_num': page.next_page_number() if page.has_next() else page.paginator.num_pages
    }
    eles = []
    for ele in page:
        my_ele = model_to_dict(ele,fields=["xh", "xm", 'cc', 'glyx', 'glyxm', 'sftb', 'sfdr', 'sfzj', 'sfzx', 'xq'])
        if my_ele['sftb'] == True:
            my_ele['sftb'] = '是'
        if my_ele['sftb'] == False:
            my_ele['sftb'] = '否'
        if my_ele['sfdr'] == True:
            my_ele['sfdr'] = '是'
        if my_ele['sfdr'] == False:
            my_ele['sfdr'] = '否'
        dict = {'xh':my_ele['xh'],'xm':my_ele['xm'],'glyx':my_ele['glyx'],'sfdr':my_ele['sfdr'],'sftb':my_ele['sftb']}
        eles.append(dict)
    result['list'] = eles
    return result

def paginator4dict(page, fields=[]):
    result = {
        'list': [],
        'count': page.paginator.count,
        'page_num': page.paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_num': page.previous_page_number() if page.has_previous() else 1,
        'next_page_num': page.next_page_number() if page.has_next() else page.paginator.num_pages
    }
    questionnaires_dict = []
    for ele in page.object_list:
        my_ele = model_to_dict(ele, fields=["id", "title", "creatorId", "oneoff", "status"])
        my_ele['createTime'] = ele.createTime.strftime("%Y-%m-%d %H:%M")
        my_ele['updateTime'] = ele.updateTime.strftime("%Y-%m-%d %H:%M")
        questionnaires_dict.append(my_ele)
    result['list'] = questionnaires_dict
    return result

def paginator5dict(page, fields=[]):
    result = {
        'list': [],
        'count': page.paginator.count,
        'page_num': page.paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_num': page.previous_page_number() if page.has_previous() else 1,
        'next_page_num': page.next_page_number() if page.has_next() else page.paginator.num_pages
    }
    questionnaires_dict = []
    for ele in page.object_list:
        my_ele = model_to_dict(ele, fields=["id", "title", "creatorId", "oneoff", "status"])
        my_ele['createTime'] = ele.createTime.strftime("%Y-%m-%d %H:%M")
        my_ele['updateTime'] = ele.updateTime.strftime("%Y-%m-%d %H:%M")
        rec = HistoryRecord.objects.filter(questionnaireId=my_ele['id'])
        my_ele['times'] = len(rec)
        questionnaires_dict.append(my_ele)
    result['list'] = questionnaires_dict
    return result

def paginator6dict(page, fields=[]):
    result = {
        'list': [],
        'count': page.paginator.count,
        'page_num': page.paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_num': page.previous_page_number() if page.has_previous() else 1,
        'next_page_num': page.next_page_number() if page.has_next() else page.paginator.num_pages
    }
    eles = []
    for obj in page.object_list:
        tmp = model_to_dict(obj,fields=fields)
        student = model_to_dict(Student.objects.get(xh=tmp['xh']))
        tmp['xm']=student['xm']
        eles.append(tmp)
    result['list'] = eles
    return result


def request_body_serialize(request):
    querydict = json.loads(request.body.decode("utf-8"))
    return querydict

def request_body_serialize_file(request):
    tmp = json.loads(request.body)
    return tmp.get("file")

def request_body_serialize_init(request):
    return json.loads(request.body)

