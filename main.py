import RPi.GPIO as GPIO
import sys
import time

from _cffi_backend import string

import I2C_LCD_driver

# define PINs according to cabling
col_list = [21, 20, 16, 12]
# following array matches 5,6,7,8 PINs from 4x4 Keypad Matrix
row_list = [7, 25, 8, 24]

# set row pins to output, to high
GPIO.setmode(GPIO.BCM)
for pin in row_list:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# set columns pins to input.
for pin in col_list:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

key_map = [["/", ".", "0", "="],
           ["*", "9", "8", "7"],
           ["-", "6", "5", "4"],
           ["+", "3", "2", "1"]]

operation = ""


# define Matrix Keypad read function
def Keypad4x4Read(cols, rows):
    for r in rows:
        GPIO.output(r, GPIO.LOW)
        result = [GPIO.input(cols[0]), GPIO.input(cols[1]), GPIO.input(cols[2]), GPIO.input(cols[3])]
        if min(result) == 0:
            key = key_map[int(rows.index(r))][int(result.index(0))]
            GPIO.output(r, GPIO.HIGH)  # manages key keept pressed
            return key
        GPIO.output(r, GPIO.HIGH)


def calculate(operation):
    i = 0
    portion_a = ""
    portion_b = ""
    operator1 = ""
    operator2 = ""
    result = 0
    final_result = 0

    while operation[i] != "=":
        if i != 0:
            portion_a = result
            portion_b = ""
            operator1 = operator2
        if i == 0:
            while operation[i] != "+" and operation[i] != "-" and operation[i] != "*" and operation[i] != "/" \
                    and operation != "=":
                portion_a = portion_a + operation[i]
                i += 1

            operator1 = operation[i]
            i += 1

        while operation[i] != "+" and operation[i] != "-" and operation[i] != "*" and operation[i] != "/" \
                and operation[i] != "=":
            portion_b = portion_b + operation[i]
            i += 1

        if operator1 == "+":
            result = float(portion_a) + float(portion_b)
        if operator1 == "-":
            result = float(portion_a) - float(portion_b)
        if operator1 == "*":
            result = float(portion_a) * float(portion_b)
        try:
            if operator1 == "/":
                result = float(portion_a) / float(portion_b)
        except ZeroDivisionError:
            print()
            print("INOTIME le informa de que no se puede dividir en estos momentos, porfavor, vuelva a intentarlo "
                  "mas tarde.")
            mylcd.lcd_clear()
            mylcd.lcd_display_string("INOTIME dice:", 1, 0)
            mylcd.lcd_display_string("Syntax Error :(",2,0)
            time.sleep(5)
            mylcd.lcd_clear()
            final_result = 0
            break

        operator2 = operation[i]
        final_result = result
        if operator2 != "=":
            i += 1

    return final_result

if __name__ == '__main__':
    mylcd = I2C_LCD_driver.lcd()
    result = 0
    calculated = False
    puntero = 0
    # main program
    while True:

        try:
            key = Keypad4x4Read(col_list, row_list)
            if key is not None:
                operation = operation + key
                if key == "=":
                    result = calculate(operation)
                    calculated = True
                time.sleep(0.3)  # gives user enough time to release without having double inputs
                print(key, end='')
                mylcd.lcd_display_string(key, 1, puntero)
                puntero += 1
                if puntero > 15:
                    puntero = 15
                if calculated:
                    print()
                    print(result)
                    mylcd.lcd_display_string(str(result), 2, 0)
                    print()
                    time.sleep(5)
                    operation = ""
                    calculated = False
                    mylcd.lcd_clear()
                    puntero = 0

        # PINs final cleaning on interrupt
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()
