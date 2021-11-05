import xlrd
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from Utils.tools import request_body_serialize_file
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
        vars = request_body_serialize_file(request)
        form = UploadFileForm(request.POST, vars)
        ret = handle_uploaded_file(form.file)
        if ret == None :
            return list[False,"文件不存在"]
        else:
            return ret
    else:
        return list[False,"方法不正确"]

def upload_file2(request):
    if request.method == 'POST':
        vars = request_body_serialze_file(request)
        form = UploadFileForm(request.POST, vars)
        ret = handle_uploaded_file2(form.file)
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

def handle_upload_file2(f):
    try:
        xls_file = xlrd.open_workbook(f)# 读文件
        xls_sheet = xls_file.sheets()[0] # 打开工作簿
        row_value = xls_sheet.row_values(0) # 读取整行信息，num为第几行
        xh_list = xls_sheet.col_values(row_value.index("学号"))
        xm_list = xls_sheet.col_values(row_value.index("姓名"))
        sfzx_list = xls_sheet.col_values(row_value.index("是否在校"))
        sfzj_list = xls_sheet.col_values(row_value.index("学号"))
        xq_list = xls_sheet.col_values(row_value.index("校区"))
        cc_list = xls_sheet.col_values(row_value.index("学历层次"))
        glyx_list = xls_sheet.col_values(row_value.index("管理院系"))
        glyxm_list = xls_sheet.col_values(row_value.index("管理院系码"))
        instructor_num_list = xls_sheet.col_values(row_value.index("辅导员职工号"))
        instructor_name_list = xls_sheet.col_values(row_value.index("辅导员姓名"))
        ret = []
        size = len(xh_list)
        for i in range(size):
            tmp = {}
            tmp["xh"] = xh_list[i]
            tmp["xm"] = xm_list[i]
            tmp["sfzx"] = sfzx_list[i]
            tmp["sfzj"] = sfzj_list[i]
            tmp["xq"] = xq_list[i]
            tmp["cc"] = cc_list[i]
            tmp["glyx"] = glyx_list[i]
            tmp["glyxm"] = glyxm_list[i]
            tmp["instructor_num"] = instructor_num_list[i]
            tmp["instructor_name"] = instructor_name_list[i]
            ret.append(tmp)
        return ret
    except OSError:
        return None



