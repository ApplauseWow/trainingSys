from django.http import HttpResponse, JsonResponse
from .Camera import ZedCamera

camera = ZedCamera()


def check_camera(request):
    """
    检查摄像头情况
    """

    success = camera.check()
    message = "please check the camera again" if not success else "the camera is ready"
    data = {}
    return JsonResponse({
        'success': success,
        'data': data,
        'message': message
    })


def open_camera(request):
    """
    开始打开摄像头
    """

    parameters = camera.init_settings()
    result = camera.open_camera(parameters)
    if True in result.keys():  # 可以开启摄像头，可能有其他异常，如无法获取z值
        return HttpResponse(camera.get_current_img(), content_type='multipart/x-mixed-replace; boundary=frame')
    elif False in result.keys():  # 无法启动摄像头
        return JsonResponse({
        'success': False,
        'data': {},
        'message': 'no frame: can not open the camera'
    })
