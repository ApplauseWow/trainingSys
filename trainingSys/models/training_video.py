from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoProject.settings import MEDIA_ROOT
import os


class TrainingVideo(models.Model):
    """
    视频信息表
    完整视频保存于’队列‘文件下
    若没有得到分析后的视频则指向default.avi
    分析结果出来后存储合成的视频路径和时间片段以及从·设备数据表·中截取的对应足部数据还有姿态节点数据
    """

    class VideoType(models.IntegerChoices):
        TEAM = 0, _("team's")  # 队列完整的
        INDIVIDUAL = 1, _("individual's")  # 个人切分后

    video_path = models.FilePathField(default=os.path.join(MEDIA_ROOT, 'video', 'default.avi'))  # [字符]视频存储路径
    pose_data_path = models.FilePathField(default=os.path.join(MEDIA_ROOT, 'video', 'default.json'))  # [字符]姿态数据存储路径，完整视频没有姿态数据
    pose_video_path = models.FilePathField(default=os.path.join(MEDIA_ROOT, 'video', 'pose_default.avi'))  # [字符]合成的姿态视频存储路径
    foot_data = models.JSONField(null=True)  # [json]分析后对应的足部数据
    trainee = models.ForeignKey(to='Trainee', on_delete=models.CASCADE, null=True)  # 切分后某队员片段，空为队列完整视频
    training = models.ForeignKey(to='Training', on_delete=models.CASCADE, null=True)  # 训练批次，含日期
    video_type = models.IntegerField(choices=VideoType.choices, default=VideoType.TEAM)  # [整数]视频类型(0完整，1切分后)
    video_fragment = models.JSONField(null=True)  # [json]视频的起始时间，队员单次训练可能有循环即产生多个视频片段
