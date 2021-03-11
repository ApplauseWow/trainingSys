from django.urls import path
from .views import view_normal, view_camera_operation


urlpatterns = [
    path('test/', view_normal.test, name='test'),
    path('camera/check', view_camera_operation.check_camera, name='check'),
    path('camera/open', view_camera_operation.open_camera, name='open')
]