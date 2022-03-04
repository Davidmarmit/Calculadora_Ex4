from datetime import time

from RPi import GPIO


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    # print_hi('PyCharm')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
    # main loop
    while True:
        GPIO.output(8, GPIO.HIGH)
        time.sleep(1)
        # off
        GPIO.output(8, GPIO.LOW)
        time.sleep(1)
