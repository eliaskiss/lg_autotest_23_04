# Document : https://pyserial.readthedocs.io/en/latest/index.html

import serial
import time


class MySerial:
    def __init__(self, port=None):
        self.ser = None

        if port is not None:
            self.openSerial(port)

    def __str__(self):
        return f'Port: {self.ser.port}'


    ###################################################################################################
    # Open Serial
    ###################################################################################################
    def openSerial(self, port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscst=False,
                   dsrdtr=False):
        # 시리얼 포트객체 생성
        self.ser = serial.Serial()

        # 시리얼 포트설정
        self.ser.port = port  # 포트명 COM2, COM3...
        self.ser.baudrate = baudrate  # Baudrate 속도
        self.ser.bytesize = bytesize  # 데이터비트
        self.ser.parity = parity  # 패러티 체크
        self.ser.stopbits = stopbits  # 스톱비트
        self.ser.timeout = timeout  # None: 무한대기, 0: 논블럭킹모드, x: x초 대기
        self.ser.xonxoff = xonxoff  # SW 플로우 컨트롤
        self.ser.rtscts = rtscst  # RTS/CTS 플로우 컨트롤
        self.ser.dsrdtr = dsrdtr  # DSR/DTR 플로우 컨트롤, 둘중 하나만 설정가능 (rtsctsr or dsrdtr)

        # 시리얼 포트열기
        self.ser.open()

    def set_baudrate(self, baudrate):
        self.ser.baudrate = baudrate

    def get_options(self):
        options = {}
        options['port'] = self.ser.port
        options['baudrate'] = self.ser.baudrate
        # ...

        return options

    ###################################################################################################
    # Write Port
    ###################################################################################################
    def writePort(self, data):
        self.ser.write(data)

    def writePortUnicode(self, data):
        self.ser.write(data.encode())

    ###################################################################################################
    # Read Port
    ###################################################################################################
    def read(self, size=1, timeout=None):
        self.ser.timeout = timeout
        readed = self.ser.read(size)
        return readed

    # Putty에서의 EOF : Ctrl + J
    def readEOF(self):
        readed = self.ser.readline()
        # return readed
        return readed[:-1]

    # Ctrl + C 가 들어올때까지 Read
    def readuntilExitCode(self, code=b'\x03'):
        readed = b''
        while True:
            data = self.ser.read()
            # print(data)
            readed += data
            # print(readed)
            if data == code:
                return readed[:-1]

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    # 시리얼 포트 객체생성
    ser = MySerial('COM2')
    print(ser)

    options = ser.get_options()
    print(options)

    # time.sleep(10)

    # 포트 쓰기
    # writePort("HelloWorld") # Unicode --> Error!!
    # ser.writePort('HelloWorld'.encode())
    # ser.writePortUnicode('HelloWorld')
    # ser.writePortUnicode('안녕세상아~')

    # Read 1byte : 1byte만 읽고 return
    # print(ser.read())

    # Read 10 bytes : 10bytes 읽고 return
    # print(ser.read(10))
    # print(ser.read(size=10))

    # Read with timeout 5 sec: 5초 대기한 후에 데이터가 없으면 return
    # print(ser.read(1, 5))
    # print(ser.read(size=1, timeout=5))

    # Read Until EOF
    # print(ser.readEOF())

    # Read Until Exit Code
    # print(ser.readuntilExitCode())