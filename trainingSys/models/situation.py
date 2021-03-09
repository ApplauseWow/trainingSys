from django.db import models


class Situation(models.Model):
    """
    训练场景
    """

    situation_name = models.CharField(max_length=16, default="未命名场景")  # [字符<=16]训练场景名称
    situation_settings = models.JSONField(null=True)  # [json]视频画面校准线设置