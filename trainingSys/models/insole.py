from django.db import models


class Insole(models.Model):
    """
    鞋垫信息表
    """

    class Status(models.IntegerChoices):
        USED = 0
        UNUSED = 1

    class LeftOrRight(models.IntegerChoices):
        LEFT = 18
        RIGHT = 81
        UNKNOWN = 11

    device_num = models.CharField(max_length=12, default='U0000')  # [字符<=12]设备编号
    device_battery_left = models.DecimalField(max_digits=5, decimal_places=2, default=100)  # [小数]设备剩余电量(共五位，两位小数)
    device_status = models.IntegerField(choices=Status.choices, default=Status.UNUSED)  # [整数]设备状态(0分配，1未分配)
    left_right = models.IntegerField(choices=LeftOrRight.choices, default=LeftOrRight.UNKNOWN)  # [整数]左脚右脚(18左，81右，11未知)
    setting = models.JSONField(null=True)  # [json]设备配置