from http import HTTPStatus
from django.http import HttpResponse


def permitted_methods(methods):
    def dector(fn):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
            return fn(request, *args, *kwargs)
        return wrapper
    return dector