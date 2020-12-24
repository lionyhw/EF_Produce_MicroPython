from microbit import *
import time
import utime

Camera_Add = 0x14
Card = 2
Face = 6
Ball = 7
Tracking = 8
Color = 9
Learn = 10

class AILENS(object):
    """基本描述

    二郎神AI摄像头(AI-Lens)

    """
    def __init__(self):
        i2c.init()
        sleep(5000)
        try:
            i2c.read(Camera_Add,1)
        except:
            display.scroll("Init AILens Error!")


    def switch_function(self, func):
        """基本描述

        选择摄像头功能

        Args:
            func (number): 选择功能号
        """
        i2c.write(Camera_Add, bytearray([0x20, func]))



if __name__ == '__main__':
    ai = AILENS()
    ai.switch_function(Ball)
