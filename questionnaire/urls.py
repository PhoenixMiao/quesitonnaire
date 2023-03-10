"""questionnaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from student import views as student_views
from poll import views as poll_views
from django.conf.urls import url


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('students/', student_views.student),
    path('student_import/',student_views.student_import),
    path('student_change/',student_views.student_change),
    path('student_select/',student_views.meta),
    url(r'^polls/(.*)$', poll_views.polls),
    url(r'^poll/(.+)$', poll_views.meta),
    url(r'^whitelist_delete/(.+)$', poll_views.whitelist_delete),
    url(r'^whitelist_import/(.+)$', poll_views.whitelist_import),
    url(r'^blacklist_delete/(.+)$', poll_views.blacklist_delete),
    url(r'^blacklist_import/(.+)$', poll_views.blacklist_import),
    url(r'^poll_create/', poll_views.poll_create),
    url(r'^poll_activate/(.+)$',poll_views.poll_activate),
    url(r'^poll_pause/(.+)$',poll_views.poll_pause),
    url(r'^record_add/',poll_views.record_add),
    url(r'^record_add_judge/', poll_views.record_add_judge),
    url(r'^record_change/',poll_views.record_change),
    url(r'^record/(.+)$',poll_views.record_meta),
    url(r'^records/(.+)$',poll_views.records),
    url(r'^history_record/(.+)$',poll_views.history_meta),
    url(r'^history_records/(.+)$',poll_views.history_records),
    url(r'^poll_file/(.+)$',poll_views.file),
    url(r'^poll_template/(.+)$',poll_views.templateFiles),
    url(r'^poll_download/(.+)$',poll_views.fileDown),
    url(r'^dynamic_download/(.+)$',poll_views.dynamic_fileDown),
    url(r'^whitelist_search/(.+)$',poll_views.whitelist_search),
    url(r'^blacklist_search/(.+)$', poll_views.blacklist_search),
    url(r'^dynamic_filtering/(.+)$',poll_views.dynamic_filtering),
    url(r'^answer_poll/(.+)$',poll_views.answer),
    url(r'^create_poll',poll_views.create),
    url(r'^pie_draw',poll_views.pieChartDraw),
]
