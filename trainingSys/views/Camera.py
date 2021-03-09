#  相机操作
import pyzed.sl as sl


class ZedCamera:
    """
    zed相机
    相机配置参数，通过使用camera_*，包括（resolution, image flip…）；
    SDK配置参数，通过使用sdk_*，包括（verbosity, GPU device used…）；
    深度配置参数，通过使用depth_*，包括（depth mode, minimum distance…）；
    坐标系配置参数，通过使用coordinate_*，包括（coordinate system, coordinate units…）；
    配置SVO视频格式的参数（filename, real-time mode…）。
    """

    def __init__(self):
        self.status_mapper = {}  # 状态映射
        self.status = None  # 摄像头状态
        self.camera = sl.Camera()  # 相机实例
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
            }
        }

    def init_settings(self, setting_type, settings_dict):
        """
        初始化摄像头参数
        :param setting_type: 设置类型
        :param settings_dict: 参数字典
        :return:
        """

        if setting_type == 'basic':
            normal_setting = sl.InitParameters()
            normal_setting.depth_mode = self.setting_mapper[settings_dict['depth_mode']]
            normal_setting.coordinate_units = self.setting_mapper[settings_dict['coordinate_units']]
            normal_setting.camera_resolution = self.setting_mapper[settings_dict['resolution']]
            normal_setting.depth_minimum_distance = settings_dict['min_dist']
            normal_setting.camera_fps = settings_dict['fps']

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
        :return:
        """

        pass

