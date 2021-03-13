from django.urls import path
from .views import view_normal, view_camera_operation


urlpatterns = [
    path('test/', view_normal.test, name='test'),
    path('camera/check', view_camera_operation.check_camera, name='check'),
    path('camera/open', view_camera_operation.open_camera, name='open'),
    path('camera/z_value', view_camera_operation.get_z_value, name='z'),
    path('camera/close', view_camera_operation.close_camera, name='close'),
    path('camera/start_training', view_camera_operation.start_recording, name='start_training'),
    path('camera/finish_training', view_camera_operation.stop_recording, name='finish_training')
]