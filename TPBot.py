from microbit import *
from time import sleep_us
from machine import time_pulse_us

TPbot_ADDR = 0x10


class TPBOT(object):
    """基本描述

    TPBot（天蓬）智能车

    """

    def __init__(self):
        i2c.init()
        self.__direction = 0
        self.__pinL = pin13
        self.__pinR = pin14
        self.__pinL.set_pull(self.__pinL.NO_PULL)
        self.__pinR.set_pull(self.__pinR.NO_PULL)
        self.__pin_t = pin16
        self.__pin_e = pin15

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
            raise ValueError('speed error,-100~100')
        self.__direction = 0x00 if left_wheel_speed > 0 else 0x01
        self.__direction = self.__direction if right_wheel_speed > 0 else self.__direction + 2
        left_wheel_speed = left_wheel_speed if left_wheel_speed > 0 else left_wheel_speed * -1
        right_wheel_speed = right_wheel_speed if right_wheel_speed > 0 else right_wheel_speed * -1
        i2c.write(TPbot_ADDR, bytearray(
            [0x01, left_wheel_speed, right_wheel_speed, self.__direction]))

    def set_car_light(self, R: int, G: int, B: int):
        """
        设置车头灯颜色
        :param R:R通道颜色0-255
        :param G:G通道颜色0-255
        :param B:B通道颜色0-255
        :return:none
        """
        if R > 255 or G > 255 or B > 255:
            raise ValueError('RGB is error')
        i2c.write(TPbot_ADDR, bytearray([0x20, R, G, B]))

    def get_distance(self, unit: int = 0):
        """
        车头超声波读取距离
        :param unit:检测距离单位 0 厘米 1 英尺
        :return:距离
        """
        self.__pin_e.read_digital()
        self.__pin_t.write_digital(1)
        sleep_us(10)
        self.__pin_t.write_digital(0)
        ts = time_pulse_us(self.__pin_e, 1, 25000)

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
        if self.__pinL.read_digital() == 1 and self.__pinR.read_digital() == 1:
            return 00
        elif self.__pinL.read_digital() == 0 and self.__pinR.read_digital() == 1:
            return 10
        elif self.__pinL.read_digital() == 1 and self.__pinR.read_digital() == 0:
            return 1
        elif self.__pinL.read_digital() == 0 and self.__pinR.read_digital() == 0:
            return 11
        else:
            print("Unknown ERROR")

    def set_servo(self, servo, angle):
        """基本描述

        选择伺服电机并且设置角度/速度

        Args:
            servo (number): 选择第几个舵机（伺服电机）1,2,3,4
            angle (number): 设置舵机角度 0~180
        """
        if servo > 4 or servo <= 0:
            raise ValueError('select servo error')
        servo = servo - 1
        if angle > 180 or angle < 0:
            raise ValueError('angle error,0~180')
        i2c.write(TPbot_ADDR, bytearray([0x10 + servo, angle, 0, 0]))


if __name__ == '__main__':
    tp = TPBOT()
    tp.set_servo(3, 0)
    while True:
        print(tp.get_distance())
