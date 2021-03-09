from django.db import models


class Training(models.Model):
    """
    训练信息表
    """

    team = models.ForeignKey(to='Team', on_delete=models.CASCADE, null=True)  # 所属队列
    situation = models.ForeignKey(to='Situation', on_delete=models.CASCADE, null=True)  # 训练场景
    training_order = models.JSONField(null=True)  # [json]队列顺序，默认第一次查询顺序，调整后进行修改并保存
    training_date_start = models.DateTimeField(null=True)  # [时间]训练开始时间
    training_date_end = models.DateTimeField(null=True)  # [时间]训练结束时间
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # [小数]队列此次平均成绩

