from django.db import models


class Questionnaire(models.Model):
    status = models.SmallIntegerField(default=0, null=True)  # {0:草稿 1:发布中 2:暂停发布 -1:已归档}
    oneoff = models.BooleanField(default=False, null=True)  # {true: 一次性问卷，不能修改，可以多次填写 false: 一人一份的问卷，只能在原内容上修改}
    title = models.CharField(max_length=200, null=True)
    scope = models.SmallIntegerField(default=2, null=True)  #{1:动态筛选，设置条件，有黑名单 2:静态名单，手动导入白名单}
    creatorId = models.CharField(max_length=30, null=True)  # 学工号
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    archiveTime = models.DateTimeField(null=True)
    k1 = models.CharField(max_length=50, null=True)
    k2 = models.CharField(max_length=50, null=True)
    k3 = models.CharField(max_length=50, null=True)
    k4 = models.CharField(max_length=50, null=True)
    k5 = models.CharField(max_length=50, null=True)
    k6 = models.CharField(max_length=50, null=True)
    k7 = models.CharField(max_length=50, null=True)
    k8 = models.CharField(max_length=50, null=True)
    k9 = models.CharField(max_length=50, null=True)
    k10 = models.CharField(max_length=50, null=True)
    k11 = models.CharField(max_length=50, null=True)
    k12 = models.CharField(max_length=50, null=True)
    k13 = models.CharField(max_length=50, null=True)
    k14 = models.CharField(max_length=50, null=True)
    k15 = models.CharField(max_length=50, null=True)
    k16 = models.CharField(max_length=50, null=True)
    k17 = models.CharField(max_length=50, null=True)
    k18 = models.CharField(max_length=50, null=True)
    k19 = models.CharField(max_length=50, null=True)
    k20 = models.CharField(max_length=50, null=True)
    type1 = models.IntegerField(default=2, null=True)
    type2 = models.IntegerField(default=2, null=True)
    type3 = models.IntegerField(default=2, null=True)
    type4 = models.IntegerField(default=2, null=True)
    type5 = models.IntegerField(default=2, null=True)
    type6 = models.IntegerField(default=2, null=True)
    type7 = models.IntegerField(default=2, null=True)
    type8 = models.IntegerField(default=2, null=True)
    type9 = models.IntegerField(default=2, null=True)
    type10 = models.IntegerField(default=2, null=True)
    type11 = models.IntegerField(default=2, null=True)
    type12 = models.IntegerField(default=2, null=True)
    type13 = models.IntegerField(default=2, null=True)
    type14 = models.IntegerField(default=2, null=True)
    type15 = models.IntegerField(default=2, null=True)
    type16 = models.IntegerField(default=2, null=True)
    type17 = models.IntegerField(default=2, null=True)
    type18 = models.IntegerField(default=2, null=True)
    type19 = models.IntegerField(default=2, null=True)
    type20 = models.IntegerField(default=2, null=True)

    class Meta:
        db_table = 'questionaire'


class Record(models.Model):
    xh = models.CharField(max_length=30, default="", null=False)  # 填写者学号
    questionnaireId = models.IntegerField(max_length=50, default="", null=False) #问卷id
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    v1 = models.CharField(max_length=50, null=True)
    v2 = models.CharField(max_length=50, null=True)
    v3 = models.CharField(max_length=50, null=True)
    v4 = models.CharField(max_length=50, null=True)
    v5 = models.CharField(max_length=50, null=True)
    v6 = models.CharField(max_length=50, null=True)
    v7 = models.CharField(max_length=50, null=True)
    v8 = models.CharField(max_length=50, null=True)
    v9 = models.CharField(max_length=50, null=True)
    v10 = models.CharField(max_length=50, null=True)
    v11 = models.CharField(max_length=50, null=True)
    v12 = models.CharField(max_length=50, null=True)
    v13 = models.CharField(max_length=50, null=True)
    v14 = models.CharField(max_length=50, null=True)
    v15 = models.CharField(max_length=50, null=True)
    v16 = models.CharField(max_length=50, null=True)
    v17 = models.CharField(max_length=50, null=True)
    v18 = models.CharField(max_length=50, null=True)
    v19 = models.CharField(max_length=50, null=True)
    v20 = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'record'


class HistoryRecord(models.Model):
    xh = models.CharField(max_length=30, default="", null=False)  # 填写者学号
    questionnaireId = models.CharField(max_length=30, default="", null=False)  # 问卷id
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    v1 = models.CharField(max_length=50, null=True)
    v2 = models.CharField(max_length=50, null=True)
    v3 = models.CharField(max_length=50, null=True)
    v4 = models.CharField(max_length=50, null=True)
    v5 = models.CharField(max_length=50, null=True)
    v6 = models.CharField(max_length=50, null=True)
    v7 = models.CharField(max_length=50, null=True)
    v8 = models.CharField(max_length=50, null=True)
    v9 = models.CharField(max_length=50, null=True)
    v10 = models.CharField(max_length=50, null=True)
    v11 = models.CharField(max_length=50, null=True)
    v12 = models.CharField(max_length=50, null=True)
    v13 = models.CharField(max_length=50, null=True)
    v14 = models.CharField(max_length=50, null=True)
    v15 = models.CharField(max_length=50, null=True)
    v16 = models.CharField(max_length=50, null=True)
    v17 = models.CharField(max_length=50, null=True)
    v18 = models.CharField(max_length=50, null=True)
    v19 = models.CharField(max_length=50, null=True)
    v20 = models.CharField(max_length=50, null=True)


    class Meta:
        db_table = 'history_record'


class Whitelist(models.Model):
    questionnaireId = models.CharField(max_length=30, default="", null=False)  # 问卷id
    xh = models.CharField(max_length=30, default="", null=True)  # 学号
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'whitelist'


class Choice(models.Model):
    questionnaireId = models.CharField(max_length=30, default="", null=False)  # 问卷id
    choiceNumber = models.IntegerField(default=0, null=False) #问题id
    A = models.CharField(max_length=200, default='', null=True)
    B = models.CharField(max_length=200, default='', null=True)
    C = models.CharField(max_length=200, default='', null=True)
    D = models.CharField(max_length=200, default='', null=True)

    class Meta:
        db_table = 'choice'


class Blacklist(models.Model):
    questionnaireId = models.IntegerField(default=0, null=False)  # 问卷id
    xh = models.CharField(max_length=30, default="", null=True)  # 学号
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blacklist'


class Condition(models.Model):
    questionnaireId = models.IntegerField(default=0, null=False)  # 问卷id
    key = models.CharField(max_length=30, null=True)  # 条件的键
    values = models.CharField(max_length=200, null=True)  # 条件的值（如果有多个值是或关系，用逗号隔开）
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'condition'


