from django.db import models


class Student(models.Model):
    xh = models.CharField(max_length=30, default="", null=False)  # 学号
    xm = models.CharField(max_length=150, null=True)  # 姓名
    sfzx = models.CharField(max_length=10, null=True)  # 是否在校 研究生的zxzk映射到0和1
    sfzj = models.CharField(max_length=10, null=True)  # 是否在籍/全日制 研究生非全/非国家学籍，映射到0 注意：研究生sfzj不会随着学生的毕业而改变
    xq = models.CharField(max_length=20, null=True)  # 校区
    cc = models.CharField(max_length=20, null=True)  # 学历层次
    glyx = models.CharField(max_length=50, null=True)  # 管理院系
    glyxm = models.CharField(max_length=20, null=True)  # 管理院系码
    sftb = models.BooleanField(default=True)  # 是否自动同步
    sfdr = models.BooleanField(default=True)  # 是否手动导入
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student'


class Instructor_Student(models.Model):
    zgh = models.CharField(primary_key=True, max_length=30, default="", null=False)  # 职工号
    xm = models.CharField(max_length=150, default="", null=True)  # 职工姓名
    xh = models.CharField(max_length=30, default="", null=True)  # 学生学号
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'instructor_student'


class DepartAdmin(models.Model):
    zgh = models.CharField(primary_key=True, max_length=30, default="", null=False)  # 职工号
    xm = models.CharField(max_length=150, default="", null=True)  # 职工姓名
    glyx = models.CharField(max_length=50, null=True)  # 管理院系
    glyxm = models.CharField(max_length=20, null=True)  # 管理院系码
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'depart_admin'


class SystemAdmin(models.Model):
    zgh = models.CharField(primary_key=True, max_length=30, default="", null=False)  # 职工号
    xm = models.CharField(max_length=150, default="", null=True)  # 职工姓名
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'system_admin'
