import time
import random

from lec_pyserial_class import MySerial

ser = MySerial('com3')

try:
    while True:
        rand_data = random.randint(10**(10-1), (10**10)-1) # 1000000000, 9999999999
        print(rand_data)
        ser.writePortUnicode(f'{rand_data}')
        time.sleep(1)
except Exception as e:
    print(e)

finally:
    ser.close()