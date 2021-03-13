from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .Camera import ZedCamera

from .constant import SysConstant

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
        return StreamingHttpResponse(camera.get_current_img(),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
    elif False in result.keys():  # 无法启动摄像头
        return JsonResponse({
            'success': False,
            'data': {},
            'message': 'no frame: can not open the camera'
        })


def get_z_value(request):
    """
    获取摄像头z值
    """

    z = camera.get_current_z_value()
    return JsonResponse({
            'success': False if z == SysConstant.NO_Z else True,
            'data': {
                'z': z
            },
            'message': 'can not get z, please check the camera' if z == SysConstant.NO_Z else ''
        })



def close_camera(request):
    """
    关闭摄像头，并且关闭录制和跟踪
    """

    success = camera.close_camera()
    return JsonResponse({
        'success': success,
        'data': {},
        'message': 'fail to close the camera, please try again' if not success else ''
    })

def stop_recording(request):
    return None


def start_recording(request):
    return None