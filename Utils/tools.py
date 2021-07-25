from django.forms.models import model_to_dict
from django.http.request import QueryDict
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


def request_body_serialze(request):
    querydict = json.loads(request.body.decode("utf-8"))
    return querydict

