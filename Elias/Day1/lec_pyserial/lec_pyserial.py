# Document : https://pyserial.readthedocs.io/en/latest/index.html

import serial
import time

###################################################################################################
# Open Serial
###################################################################################################
def openSerial(port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscst=False,
               dsrdtr=False):

    # 시리얼 포트객체 생성
    ser = serial.Serial()

    # 시리얼 포트설정
    ser.port = port             # 포트명 COM2, COM3...
    ser.baudrate = baudrate     # Baudrate 속도
    ser.bytesize = bytesize     # 데이터비트
    ser.parity = parity         # 패러티 체크
    ser.stopbits = stopbits     # 스톱비트
    ser.timeout = timeout       # None: 무한대기, 0: 논블럭킹모드, x: x초 대기
    ser.xonxoff = xonxoff       # SW 플로우 컨트롤
    ser.rtscts = rtscst         # RTS/CTS 플로우 컨트롤
    ser.dsrdtr = dsrdtr         # DSR/DTR 플로우 컨트롤, 둘중 하나만 설정가능 (rtsctsr or dsrdtr)

    # 시리얼 포트열기
    ser.open()

    # ser = serial.Serial(port, baudrate, ...)
    # ser.open() 을 호출할 필요가 없습니다!!
    return ser

###################################################################################################
# Write Port
###################################################################################################
def writePort(ser, data):
    ser.write(data)

def writePortUnicode(ser, data):
    ser.write(data.encode())

###################################################################################################
# Read Port
###################################################################################################
def read(ser, size=1, timeout=None):
    ser.timeout = timeout
    readed = ser.read(size)
    return readed

# Putty에서의 EOF : Ctrl + J
def readEOF(ser):
    readed = ser.readline()
    # return readed
    return readed[:-1]

# Ctrl + C 가 들어올때까지 Read
def readuntilExitCode(ser, code=b'\x03'):
    readed = b''
    while True:
        data = ser.read()
        # print(data)
        readed += data
        # print(readed)
        if data == code:
            return readed[:-1]

if __name__ == '__main__':
    # 시리얼 포트 객체생성
    ser = openSerial('COM2', 9600)

    # time.sleep(10)

    # 포트 쓰기
    # writePort(ser, "HelloWorld") # Unicode --> Error!!
    # writePort(ser, 'HelloWorld'.encode())
    # writePortUnicode(ser, 'HelloWorld')
    # writePortUnicode(ser, '안녕세상아~')

    # Read 1byte : 1byte만 읽고 return
    # print(read(ser))

    # Read 10 bytes : 10bytes 읽고 return
    # print(read(ser, 10))
    # print(read(ser, size=10))

    # Read with timeout 5 sec: 5초 대기한 후에 데이터가 없으면 return
    # print(read(ser, 1, 5))
    # print(read(ser, size=1, timeout=5))

    # Read Until EOF
    print(readEOF(ser))

    # Read Until Exit Code
    # print(readuntilExitCode(ser))

# 01. 전원 (Command: k a)
# ▶ 세트의 전원 켜짐/ 꺼짐을 제어합니다.

# Transmission(명령값)
# [k][a][ ][Set ID][ ][Data][Cr]
# Data	00: 꺼짐
#       01: 켜짐
#       ff(FF): 상태값
# ex) ka 01 01, ka 01 00, ka 01 ff

# Acknowledgement(응답값)
# [a][ ][Set ID][ ][OK/NG][Data][x]
# ex) a 01 OK01x, a 01 OK00x, a 01 NG11x
#     a 01 OK01x (켜져있는경우)
#     a 01 OK00x (꺼져있는경우)
# NG인 경우는: 명령어가 잘못된경우, 값이 잘못된경우.
# 처음 시작상태는 poweroff인 상태로 시작
# * 디스플레이의 전원이 완전히 켜진 이후에 정상적인 Acknowledgement 신호가 돌아옵니다.
#
# ** Transmission/ Acknowledgement 신호 사이에는 일정시간 지연이 발생할 수 있습니다.