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
    path('student/', student_views.student),

    url(r'^polls/(.*)$', poll_views.polls),
    url(r'^poll/(.+)$', poll_views.meta),
    url(r'^whitelist/(.+)$', poll_views.whitelist),
    url(r'^whitelist_delete/(.+)$', poll_views.whitelist_delete),
    url(r'^whitelist_import/(.+)$', poll_views.whitelist_import),

]
