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
# 'exit'가 입력되면 종료
# 수신된 데이터를 json 포맷으로 저장

from lec_pyserial_class import MySerial
import json
from datetime import datetime

RETURN_CODE = b'\x0d'

ser = MySerial()
is_power_on = False
ser.openSerial('COM2')

print('Program is running...')
while True:
    # Todo: 구현부분
    readed = ser.readuntilExitCode(RETURN_CODE)
    print(readed)

    response = 'a 01 OK01 x'
    ser.writePortUnicode(response)

# 포트닫기
ser.close()