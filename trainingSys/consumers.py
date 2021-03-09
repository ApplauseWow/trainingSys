#  异步使用数据库操作必须使用sync_to_asyn(op_func)
#  consumer处理message命名方式是将message中的'.'替换为'_'，即处理该“事件”的函数名为message的.替换为_
#  如果集成的异步consumer所有处理方法必须加上asyn def，同步consumer则同步方法def
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class CameraConsumer(WebsocketConsumer):
    """
    相机管理，同步
    """

    def connect(self):
        self.accept()