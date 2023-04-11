import threading

from lec_pyserial_class import MySerial
running_thread = True

def parser(ser):
    global running_thread

    try:
        while running_thread:
            readed = ser.read(size=10, timeout=1)
            if len(readed) != 0:
                with open('log.txt', 'a') as f:
                    f.write(readed.decode())
                    f.write('\n')
    except Exception as e:
        print(e)
    finally:
        ser.close()

if __name__ == '__main__':
    ser = MySerial('com2')

    thread = threading.Thread(target=parser, args=[ser])
    thread.start()

    print('Thread is started')
    print('Type q to stop : ', end='')
    if input() == 'q':
        running_thread = False
        print('Thread is dead')

