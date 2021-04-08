from microbit import *


class IOT(object):

    def __init__(self, TX_pin=pin8, RX_pin=pin12):
        #uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=TX_pin, rx=RX_pin)
        self.__sendAT("AT+RESTORE", 1000)
        self.__sendAT("AT+CWMODE=1", 500)

    def __sendAT(self, command: str, wait: int = 0):
        uart.write(command + "\u000D\u000A")
        sleep(wait)

    def connectWIFI(self, ssid: str, pw: str):
        """
        连接Wi-Fi，只支持2.4G无线网络
        :param ssid:Wi-Fi无线网络名
        :param pw: Wi-Fi无线网络密码
        :return: 是否连接成功
        """
        self.__sendAT("AT+CWJAP=\"" + ssid + "\",\"" + pw + "\"", 500)
        while True:
            uart_str = uart.read()
            if "WIFI GOT IP" in str(uart_str):
                return True
            elif "FAIL" in str(uart_str):
                return False

    def connectThingSpeak(self):
        """
        连接Wi-Fi，只支持2.4G无线网络
        :param ssid:Wi-Fi无线网络名
        :param pw: Wi-Fi无线网络密码
        :return: 是否连接成功
        """
        text = "AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",80"
        self.__sendAT(text, 100)

    def uploadData(self, write_api_key: str, n1: int = 0, n2: int = 0, n3: int = 0, n4: int = 0, n5: int = 0, n6: int = 0, n7: int = 0, n8: int = 0):
        """
        设置要发送到 ThingSpeak 的数据并且发送上去
        :param write_api_key: ThingSpeak 的写入API
        :param n1-n8: 8路要写入的数据
        :return: 是否发送成功
        """
        toSendStr = "GET /update?api_key=" + write_api_key + "&field1=" + str(n1) + "&field2=" + str(n2) + "&field3=" + str(
            n3) + "&field4=" + str(n4) + "&field5=" + str(n5) + "&field6=" + str(n6) + "&field7=" + str(n7) + "&field8=" + str(n8)
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 100)
        self.__sendAT(toSendStr, 100)


if __name__ == '__main__':
    iot = IOT()
    iot.uploadData("asdad1d1d21d1",1,2,3,4,5,6,7,8)
    if iot.connectWIFI("iPhone", "995512"):
        display.show(Image.HAPPY)
    display.show(Image.SAD)
