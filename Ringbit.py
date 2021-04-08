from microbit import *
from time import sleep_us
from machine import time_pulse_us


class RINGBIT(object):
    """基本描述

    Ring:bit（瑞比特）主控板

    """

    def __init__(self, left_wheel_pin=pin1, right_wheel_pin=pin2):
        """
        初始化ring:bit小车
        :param left_wheel_pin: 小车左轮舵机连接口
        :param right_wheel_pin: 小车右轮舵机连接口
        """
        i2c.init()
        self.__left_wheel_pin = left_wheel_pin
        self.__right_wheel_pin = right_wheel_pin
        self.__right_wheel_pin.set_analog_period(10)
        self.__left_wheel_pin.set_analog_period(10)
        self.__module_pin = pin0
        if self.__left_wheel_pin != pin1 and self.__right_wheel_pin != pin1:
            self.__module_pin = pin1
        if self.__left_wheel_pin != pin2 and self.__right_wheel_pin != pin2:
            self.__module_pin = pin2

    def set_motors_speed(self, left_wheel_speed: int, right_wheel_speed: int):
        """
        设置左右轮电机速度
        :param left_wheel_speed:左轮速度-100～100
        :param right_wheel_speed: 右轮速度-100～100
        :return: none
        """
        if left_wheel_speed > 100 or left_wheel_speed < -100:
            raise ValueError('speed error,-100~100')
        if right_wheel_speed > 100 or right_wheel_speed < -100:
            raise ValueError('select motor error,1,2,3,4')
        if left_wheel_speed > 0:
            left_wheel_speed = ((left_wheel_speed - 0) *
                                (256 - 153.6)) / (100 - 0) + 153.6
            self.__left_wheel_pin.write_analog(left_wheel_speed)
        elif left_wheel_speed < 0:
            left_wheel_speed = ((left_wheel_speed - 0) *
                                (51.2 - 153.6)) / (-100 - 0) + 153.6
            self.__left_wheel_pin.write_analog(left_wheel_speed)
        else:
            self.__left_wheel_pin.write_analog(153.6)

        right_wheel_speed = right_wheel_speed * -1
        if right_wheel_speed > 0:
            right_wheel_speed = ((right_wheel_speed - 0)
                                 * (256 - 153.6)) / (100 - 0) + 153.6
            self.__right_wheel_pin.write_analog(right_wheel_speed)
        elif right_wheel_speed < 0:
            right_wheel_speed = ((right_wheel_speed - 0)
                                 * (51.2 - 153.6)) / (-100 - 0) + 153.6
            self.__right_wheel_pin.write_analog(right_wheel_speed)
        else:
            self.__right_wheel_pin.write_analog(153.6)

    def get_distance(self, unit: int = 0):
        """
        超声波读取距离
        :param unit:检测距离单位 0 厘米 1 英尺
        :return:距离
        """
        self.__module_pin.read_digital()
        self.__module_pin.write_digital(1)
        sleep_us(10)
        self.__module_pin.write_digital(0)
        ts = time_pulse_us(self.__module_pin, 1, 25000)

        distance = ts * 9 / 6 / 58
        if unit == 0:
            return distance
        elif unit == 1:
            return distance / 254

    def get_tracking(self):
        """
        返回当前巡线头状态
        :return:00 均在白色
                10 左黑右白
                01 左白右黑
                11 均在黑色
        """
        val = self.__module_pin.read_analog()
        if val < 150:
            return 11
        elif 150 <= val < 235:
            return 10
        elif 235 <= val < 300:
            return 1
        elif 300 <= val < 600:
            return 0
        else:
            print("Unknown ERROR")


if __name__ == '__main__':
    rb = RINGBIT(pin1, pin2)

    while True:
        rb.set_motors_speed(50, 50)
        sleep(1000)
        rb.set_motors_speed(0, 0)
        sleep(1000)
