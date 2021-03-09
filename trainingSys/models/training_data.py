from django.db import models


class TrainingData(models.Model):
    """
    训练数据表
    training可以得到训练开始时间以校准
    自增id通过排序可以推测数据的先后顺序
    某人某次训练的采样数据，可避免更换设备无法找到数据
    """

    trainee = models.ForeignKey(to='Trainee', on_delete=models.CASCADE, null=True)  # 队员
    training = models.ForeignKey(to='Training', on_delete=models.CASCADE, null=True)  # 产生数据的训练批次
    left_foot_data = models.JSONField(null=True)  # [json]左脚设备采集整个训练过程的冗余数据，包含各种数据key-val对应
    right_foot_data = models.JSONField(null=True)  # # [json]右脚设备采集整个训练过程的冗余数据，包含各种数据key-val对应
