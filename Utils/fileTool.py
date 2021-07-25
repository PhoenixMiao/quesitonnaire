import xlrd
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

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
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return "Success"
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

#处理.xls文件
def handle_uploaded_file(f):
    xls_file = xlrd.open_workbook("file.name")# 读文件
    xls_sheet = xls_file.sheets()[0] # 打开工作簿
    row_value = xls_sheet.row_values(0) # 读取整行信息，num为第几行
    xh_list = xls_sheet.col_values(row_value.indexof("学号"))# 获取某列的值，col为第几列
    return xh_list


