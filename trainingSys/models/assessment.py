from django.db import models


class Assessment(models.Model):
    """
    训练评估表
    """

    trainee = models.ForeignKey(to='Trainee', on_delete=models.CASCADE, null=True)  # 队员
    training = models.ForeignKey(to='Training', on_delete=models.CASCADE, null=True)  # 训练批次
    score = models.JSONField(null=True)  # [json]包含各个评分细则所对应的各项打分以及建议
    avg_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 平均成绩
    report = models.TextField(default='尚未得出评估报告')  # [字符]综合评估报告
    suggestion = models.TextField(default='尚未给出训练建议')  # [字符]训练建议