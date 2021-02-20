from microbit import *

WUKONG_ADDR = 0x10


class WUKONG(object):
    """基本描述

    悟空多功能主控板

    """

    def __init__(self):
        i2c.init()

    def set_motors(self, motor, speed):
        """基本描述

        选择电机并且设置速度

        Args:
            motor (number): 选择第几个电机 1,2
            speed (number): 设置电机速度 -100~100
        """
        if speed > 100 or speed < -100:
            raise ValueError('speed error,-100~100')
        if motor > 2 or motor < 1:
            raise ValueError('select motor error,1,2,3,4')
        if speed < 0:
            i2c.write(WUKONG_ADDR, bytearray([motor, 0x02, speed * -1, 0]))
        else:
            i2c.write(WUKONG_ADDR, bytearray([motor, 0x01, speed, 0]))

    def set_servo(self, servo, angle):
        """基本描述

        选择伺服电机并且设置角度/速度

        Args:
            servo (number): 选择第几个舵机（伺服电机）0,1,2,3,4,5,6,7
            angle (number): 设置舵机角度 0~180
        """
        if servo > 7 or servo < 0:
            raise ValueError('select servo error')
        if angle > 180 or angle < 0:
            raise ValueError('angle error,0~180')
        if servo == 7:
            i2c.write(WUKONG_ADDR, bytearray([0x10, angle, 0, 0]))
        else:
            i2c.write(WUKONG_ADDR, bytearray([servo + 3, angle, 0, 0]))

    def set_light(self, light):
        """基本描述

        设置氛围灯亮度

        Args:
            light (number): 氛围灯亮度
        """
        i2c.write(WUKONG_ADDR, bytearray([0x12, light, 0, 0]))
        sleep(100)
        i2c.write(WUKONG_ADDR, bytearray([0x11, 160, 0, 0]))

    def set_light_breath(self, br: bool):
        """基本描述

        设置氛围灯呼吸模式

        Args:
            br (bool): 氛围灯呼吸模式开关
        """
        if br:
            i2c.write(WUKONG_ADDR, bytearray([0x11, 0, 0, 0]))
            sleep(100)
            i2c.write(WUKONG_ADDR, bytearray([0x12, 150, 0, 0]))
        else:
            i2c.write(WUKONG_ADDR, bytearray([0x12, 0, 0, 0]))
            sleep(100)
            i2c.write(WUKONG_ADDR, bytearray([0x11, 160, 0, 0]))


if __name__ == '__main__':
    wk = WUKONG()

    wk.set_motors(1, 100)
    wk.set_servo(1, 90)
    if button_a.is_pressed():
        wk.set_light_breath(False)
    else:
        wk.set_light_breath(True)
