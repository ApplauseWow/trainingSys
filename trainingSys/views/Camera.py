#  相机操作
import pyzed.sl as sl
import time
import cv2
from djangoProject.settings import MEDIA_ROOT
import os


class ZedCamera:
    """
    zed相机
    相机配置参数，通过使用camera_*，包括（resolution, image flip…）；
    SDK配置参数，通过使用sdk_*，包括（verbosity, GPU device used…）；
    深度配置参数，通过使用depth_*，包括（depth mode, minimum distance…）；
    坐标系配置参数，通过使用coordinate_*，包括（coordinate system, coordinate units…）；
    配置SVO视频格式的参数（filename, real-time mode…）。
    参数都利用property将方法作为属性使用可直接赋值/获取/删除
    """

    def __init__(self):
        self.status_mapper = {
            'IS_RUNNING': True,  # 摄像头是否正在运行,
            'IS_RECORDING': False,  # 摄像头是否正在录制
            'IS_TRACKING': True  # 摄像头是否正在获取position（z值）
        }  # 摄像头状态映射，易添加
        self.camera = sl.Camera()  # 相机实例
        self.pose = sl.Pose()  # 摄像头空间状态实例
        self.setting_parameters = {  # 设置参数实例
            'basic': None,
            'runtime': None,
            'recording': None,
            'tracking': None
        }
        self.setting_mapper = {
            'basic': {
                'depth_mode': {
                    'none': sl.DEPTH_MODE.NONE,
                    'performance': sl.DEPTH_MODE.PERFORMANCE,
                    'quality': sl.DEPTH_MODE.QUALITY,
                    'ultra': sl.DEPTH_MODE.ULTRA
                },
                'coordinate_units': {
                    'm': sl.UNIT.METER,
                    'cm': sl.UNIT.CENTIMETER,
                    'mm': sl.UNIT.MILLIMETER
                },
                'resolution': {
                    'vga': sl.RESOLUTION.VGA,
                    '720': sl.RESOLUTION.HD720,
                    '1080': sl.RESOLUTION.HD1080,
                    '2k': sl.RESOLUTION.HD2K
                }
            },
            'runtime': {

            },
            'recording': {
                'compression_mode': {
                    'h264': sl.SVO_COMPRESSION_MODE.H264,
                    'h265': sl.SVO_COMPRESSION_MODE.H265,
                    'lossless': sl.SVO_COMPRESSION_MODE.LOSSLESS
                }
            },
            'tracking': {

            }
        }

    def init_settings(self, setting_type=None, settings_dict=None, check=False):
        """
        初始化摄像头参数
        :param setting_type: 设置类型
        :param settings_dict: 参数字典
        :param check: 是否为仅检查
        :return:
        """

        basic_setting = sl.InitParameters()  # 基本设置
        positional_tracking_setting = sl.PositionalTrackingParameters()  # 摄像头空间数据设置
        runtime_setting = sl.RuntimeParameters()  # 摄像头运行设置
        recording_setting = sl.RecordingParameters()  # 录制设置

        if not setting_type:
            #  default
            # basic
            basic_setting.depth_mode = self.setting_mapper['basic']['depth_mode']['ultra']
            basic_setting.coordinate_units = self.setting_mapper['basic']['coordinate_units']['mm']
            basic_setting.camera_resolution = self.setting_mapper['basic']['resolution']['720']
            basic_setting.depth_minimum_distance = 0.3
            basic_setting.camera_fps = 30
            # runtime and positional tacking

            if check:
                pass
            else:
                self.setting_parameters['basic'] = basic_setting
                self.setting_parameters['runtime'] = runtime_setting
                self.setting_parameters['tracking'] = positional_tracking_setting

            return {
                'basic': basic_setting,
                'runtime': runtime_setting,
                'tracking': positional_tracking_setting
            }
        else:
            if setting_type == 'basic':
                # set initial parameters
                basic_setting.depth_mode = self.setting_mapper['basic']['depth_mode'][settings_dict['depth_mode']]
                basic_setting.coordinate_units = self.setting_mapper['basic']['coordinate_units'][
                    settings_dict['coordinate_units']]
                basic_setting.camera_resolution = self.setting_mapper['basic']['resolution'][
                    settings_dict['resolution']]
                basic_setting.depth_minimum_distance = settings_dict['min_dist']
                basic_setting.camera_fps = settings_dict['fps']

                self.setting_parameters['basic'] = basic_setting
                return basic_setting
            elif setting_type == 'runtime':
                # set runtime parameters

                self.setting_parameters['runtime'] = runtime_setting
                return runtime_setting
            elif setting_type == 'recording':
                # set recording parameters
                recording_setting.compression_mode = self.setting_mapper[settings_dict['compression_mode']]
                recording_setting.video_filename = settings_dict['video_path']

                self.setting_parameters['recording'] = recording_setting
                return recording_setting
            elif setting_type == 'tracking':
                # set positional tracking parameters

                self.setting_parameters['tracking'] = positional_tracking_setting
                return positional_tracking_setting

    def update_settings(self, setting_dict):
        """
        更新摄像头参数
        :param setting_dict: 参数字典
        :return:
        """

        pass

    def get_camera_information(self):
        """
        获取摄像头参数
        前提为摄像头open
        z值只能在while true: grab()时获取
        :return:
        """

        pass

    def check(self) -> bool:
        """
        检查相机情况
        """

        parameters = self.init_settings(check=True)
        self.camera.open(parameters['basic'])
        if self.camera.is_opened():
            self.camera.close()
            return True
        else:
            return False

    def open_camera(self, parameters):
        """
        开启摄像头
        :param parameters: 参数设置实例 eg: InitParameters()
        """

        msg = ""  # 错误信息
        self.camera.open(parameters['basic'])
        if self.camera.is_opened():
            if self.camera.enable_positional_tracking(parameters['tracking']) != sl.ERROR_CODE.SUCCESS:
                # 已开启摄像头，但无法获取z值
                "".join([msg, 'can not get oz value'])
                self.status_mapper['IS_TRACKING'] = False
                return {True: msg}
            else:  # 已正常开启，尚未开始录制
                self.status_mapper['IS_RUNNING'] = True
                self.status_mapper['IS_TRACKING'] = True
                "".join([msg, 'continue'])
                return {True: msg}
        else:
            # 摄像头故障
            "".join([msg, 'camera was broken'])
            self.status_mapper['IS_RUNNING'] = False
            return {False: msg}

    def get_current_img(self):
        """
        摄像头开始输入
        """

        left_img = sl.Mat()  # 左目
        right_img = sl.Mat()  # 右目
        while self.status_mapper['IS_RUNNING']:
            if self.camera.grab(self.setting_parameters['runtime']) == sl.ERROR_CODE.SUCCESS:
                # 成功运行摄像头并成功获取图像
                # start = time.time()

                self.camera.retrieve_image(left_img, view=sl.VIEW.LEFT)  # 获取左目,共前端使用
                # self.camera.retrieve_image(right_img, view=sl.VIEW.RIGHT)  # 获取右目
                # 之后是否左右合成为center的图像

                # 25 fps
                # time.sleep(max(1. / 25 - (time.time() - start), 0))

                frame = left_img.get_data()  # ndarray.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
            else:
                frame = cv2.imread(os.path.join(MEDIA_ROOT, 'no_frame.jpg'))
                return (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

    def get_current_z_value(self):
        """
        获取当前z值
        """

        pass

    def recording(self, start_finish='finish', settings=None):
        """
        开始/结束录制
        :param start_finish: str:'start'/'finish'
        :param settings: dict:{filepath, compression_mode}
        """

        pass
