from microbit import *


class IOT(object):

    def __init__(self, TX_pin=pin8, RX_pin=pin12):
        uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=TX_pin, rx=RX_pin)
        self.__sendAT("AT+RESTORE", 1000)
        self.__sendAT("AT+CWMODE=1", 500)
        self.__userToken = ""
        self.__topic = ""
        while uart.any():
            uart.read()

    def __sendAT(self, command: str, wait: int = 0):
        uart.write(command + "\u000D\u000A")
        sleep(wait)

    def __waitResponse(self):
        uart_str = ""
        timeOut = running_time()
        while True:
            if uart.any():
                uart_str = str(uart.read(), 'UTF-8') + uart_str
                if "WIFI GOT IP" in uart_str:
                    return True
                elif "OK" in uart_str:
                    return True
                elif "FAIL" in uart_str:
                    return False
                elif len(uart_str) > 60:
                    uart_str = " "
            elif running_time() - timeOut > 8000:
                return False

    def connectWIFI(self, ssid: str, pw: str):
        """
        连接Wi-Fi，只支持2.4G无线网络
        :param ssid:Wi-Fi无线网络名
        :param pw: Wi-Fi无线网络密码
        :return: 是否连接成功
        """
        self.__sendAT("AT+CWJAP=\"" + ssid + "\",\"" + pw + "\"", 500)
        return self.__waitResponse()

    def connectThingSpeak(self):
        """
        连接Wi-Fi，只支持2.4G无线网络
        :param ssid:Wi-Fi 无线网络名
        :param pw: Wi-Fi 无线网络密码
        :return: 是否连接成功
        """
        text = "AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",80"
        self.__sendAT(text, 500)
        return self.__waitResponse()

    def uploadThingSpeak(self, write_api_key: str, n1: int = 0, n2: int = 0, n3: int = 0, n4: int = 0, n5: int = 0, n6: int = 0, n7: int = 0, n8: int = 0):
        """
        设置要发送到 ThingSpeak 的数据并且发送上去
        :param write_api_key: ThingSpeak 的写入API
        :param n1-n8: 8组要写入的数据
        :return: 是否发送成功
        """
        toSendStr = "GET /update?api_key=" + write_api_key + "&field1=" + str(n1) + "&field2=" + str(n2) + "&field3=" + str(
            n3) + "&field4=" + str(n4) + "&field5=" + str(n5) + "&field6=" + str(n6) + "&field7=" + str(n7) + "&field8=" + str(n8)
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)
        return self.__waitResponse()
    
    def connectKidsiot(self, userToken:str, topic:str):
        self.__userToken = userToken
        self.__topic = topic
        self.__sendAT("AT+CIPSTART=\"TCP\",\"139.159.161.57\",5555", 5000)
        toSendStr = "{\"topic\":\"" + self.__topic + "\",\"userToken\":\"" + self.__userToken + "\",\"op\":\"init\"}"
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)

    def uploadKidsiot(self,data:int):
        toSendStr = "{\"topic\":\"" + self.__topic + "\",\"userToken\":\"" + self.__userToken + "\",\"op\":\"up\",\"data\":\"" + data + "\"}"
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)

    def disconnectKidsiot(self):
        toSendStr = "{\"topic\":\"" + self.__topic + "\",\"userToken\":\"" + self.__userToken + "\",\"op\":\"close\"}"
        self.__sendAT("AT+CIPSEND="+str(len(toSendStr)+2), 500)
        self.__sendAT(toSendStr, 100)

if __name__ == '__main__':
    iot = IOT()
    if iot.connectWIFI("iPhone","99551212"):
        display.show(Image.YES)
    else:
        display.show(Image.NO)
    if iot.connectThingSpeak():
        display.show("1")
        if iot.uploadThingSpeak("MR1OD64WC5KH1AJE",666):
            display.show("2")
        