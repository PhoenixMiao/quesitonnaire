import xlrd
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from Utils.tools import request_body_serialze2
from http import HTTPStatus

#上传文件过程中用到的工具类
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

    def __init__(self,title,file):
        self.file = file
        self.title = title

#上传文件的过程
def upload_file(request):
    if request.method == 'POST':
        vars = request_body_serialze2(request)
        form = UploadFileForm(request.POST, vars)
        ret = handle_uploaded_file(form.file)
        if ret == None :
            return list[False,"文件不存在"]
        else:
            return ret
    else:
        return list[False,"方法不正确"]


#处理.xls文件
def handle_uploaded_file(f):
    try:
        xls_file = xlrd.open_workbook(f)# 读文件
        xls_sheet = xls_file.sheets()[0] # 打开工作簿
        row_value = xls_sheet.row_values(0) # 读取整行信息，num为第几行
        xh_list = xls_sheet.col_values(row_value.index("学号"))# 获取某列的值，col为第几列
        return xh_list
    except OSError:
        return None



