from microbit import *

Camera_Add = 0x14
Card = 2
Face = 6
Ball = 7
Tracking = 8
Color = 9
Learn = 10
numberCards = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letterCards = ["A", "B", "C", "D", "E"]
otherCards = ["Mouse", "micro:bit", "Ruler", "Cat", "Peer", "Ship", "Apple", "Car", "Pan", "Dog", "Umbrella",
              "Airplane", "Clock", "Grape", "Cup", "Turn left", "Turn right", "Forward", "Stop", "Back"]
colorList = ["Green", "Blue", "Yellow", "Black", "Red", "White"]


class AILENS(object):
    """基本描述

    二郎神AI摄像头(AI-Lens)

    """

    def __init__(self):
        i2c.init()
        sleep(5000)
        try:
            i2c.read(Camera_Add, 1)
        except:
            display.scroll("Init AILens Error!")

    def __get_image(self):
        Databuff = i2c.read(Camera_Add, 9)
        return Databuff

    def switch_function(self, func):
        """基本描述

        选择摄像头功能

        Args:
            :param func: 选择功能号
        """
        i2c.write(Camera_Add, bytearray([0x20, func]))

    def get_ball_color(self):
        """

        :return:
        """
        Databuff = self.__get_image()
        if Databuff[0] == 7:
            if Databuff[1] == 1:
                return "Blue"
            elif Databuff == 2:
                return "Red"
            else:
                return "No Ball"

    def get_ball_data(self):
        """

        :return:
        """
        BallData = []
        Databuff = self.__get_image()
        for i in range(7):
            BallData[i] = Databuff[i + 2]
        return BallData

    def get_face(self):
        """

        :return:
        """
        Databuff = self.__get_image()
        return Databuff[0] == 6

    def get_face_data(self):
        """

        :return:
        """
        FaceData = []
        Databuff = self.__get_image()
        for i in range(7):
            FaceData[i] = Databuff[i + 2]
        return FaceData

    def get_card_content(self):
        Databuff = self.__get_image()
        if Databuff[0] == 2:
            return numberCards[Databuff[1] - 1]
        elif Databuff[0] == 4:
            return letterCards[Databuff[1] - 1]
        elif Databuff[0] == 3:
            return otherCards[Databuff[1] - 1]
        else:
            return "No Card"

    def get_card_data(self):
        CardData = []
        Databuff = self.__get_image()
        for i in range(7):
            CardData[i] = Databuff[i + 2]
        return CardData

    def get_color_type(self):
        Databuff = self.__get_image()
        if Databuff[0] == 9:
            return colorList[Databuff[1] - 1]
        else:
            return "No Color"

    def get_color_data(self):
        ColorData = []
        Databuff = self.__get_image()
        for i in range(7):
            ColorData[i] = Databuff[i + 2]
        return ColorData

    def get_track_data(self):
        TrackData = []
        Databuff = self.__get_image()
        for i in range(3):
            TrackData[i] = Databuff[i + 2]
        return TrackData

    def learn_object(self, learn_id):
        i2c.write(Camera_Add, bytearray([10, learn_id]))

    def get_learn_data(self):
        LearnData = []
        Databuff = self.__get_image()
        LearnData[0] = Databuff[1]
        LearnData[1] = 100 - Databuff[2]
        return LearnData


if __name__ == '__main__':
    ai = AILENS()
    ai.switch_function(Ball)
