from django.db import models
from djangoProject.settings import MEDIA_ROOT
import os


class Trainee(models.Model):
    """
    受训队员信息表
    """

    name = models.CharField(max_length=24, default='Unfilled')  # [字符<=12个汉字]受训者姓名
    team = models.ForeignKey(to='Team', on_delete=models.CASCADE, null=True)  # 所属队列
    trainee_num = models.CharField(max_length=20, default='0000')  # [字符<=20位]受训者编号
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # [小数]受训者身高(总共五位数，其中小数占两位)
    weight = models.DecimalField(max_digits=4, decimal_places=2, default=0)  # [小数]受训者体重(总共四位数，其中小数占两位)
    feet_size = models.CharField(max_length=4, default='99')  # [字符<=4位]受训者鞋码(可能有不同的尺码标准eg:260或42.5)
    face_image_path = models.FilePathField(default=os.path.join(MEDIA_ROOT, 'default.jpg'))  # [字符]人像图片存储路径
    # 两个字段都关联一个外键需要设置related_name避免重名
    lfeet_insole = models.ForeignKey(to='Insole', on_delete=models.CASCADE, null=True, related_name='linsole')  #  左脚设备
    rfeet_insole = models.ForeignKey(to='Insole', on_delete=models.CASCADE, null=True, related_name='rinsole')  # 右脚设备


