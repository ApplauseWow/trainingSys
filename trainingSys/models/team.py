from django.db import models


class Team(models.Model):
    """
    受训队列信息表
    """

    team_name = models.CharField(max_length=20, default='未命名')  # [字符<=20]队列名称
