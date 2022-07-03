from machine import Pin, PWM
import time
import utime

outpin = Pin(22)
pwm = PWM(Pin(16))
pwm.freq(200)
pwm_duty = 3000
pwm.duty_u16(pwm_duty)
servo = PWM(Pin(15))
servo.freq(50)
servo2 = PWM(Pin(18))
servo2.freq(50)

outpin.value(1)

MID = 1500000
MIN = 1000000
MAX = 1900000

input_pin = Pin(5, Pin.IN)
led = Pin(25, Pin.OUT)

def measureFunc(position):
    while input_pin.value() == 0:
        pass
    start = time.ticks_us()
    while input_pin.value() == 1:
        pass
    end = time.ticks_us()
    duty = end - start
    return duty

def moveFunc(position):
    if position == MIN:
        while position != MAX:
            position += 2000
            utime.sleep(0.01)
            servo.duty_ns(position)
            print("Moving")
        position = MAX
    elif position == MAX:
        while position != MIN:
            position -= 2000
            utime.sleep(0.01)
            servo.duty_ns(position)
        position = MIN
    return position
    
def movetoMax():
    position1 = MIN
    position2 = MIN - 100000
    while position2 < MAX:
        time.sleep(0.01)
        if position1 < MAX:
            position1 += 2000
            servo.duty_ns(position1)
        if position2 < MAX:
            position2 += 2000
            if position2 >= MIN:
                servo2.duty_ns(position2)
    return position2

def movetoMin():
    position1 = MAX
    position2 = MAX + 100000
    actualPosition1 = False
    actualPosition2 = False
    while position2 > MIN:
        time.sleep(0.01)
        if position1 > MIN:
            position1 -= 2000
            servo.duty_ns(position1)
        if position2 > MIN:
            position2 -= 2000
            if position2 <= MAX:
                servo2.duty_ns(position2)
        #print(position1, position2)
    return position2
    
CurrPos = MIN
minDuty = 0
while True:
    minDuty = measureFunc(CurrPos)
    print(minDuty)
    """
    print(minDuty)
    if minDuty < 1100:
        led.value(0)
        CurrPos = movetoMax()
        print("Moving")
    if minDuty > 2000:
        led.value(1)
        CurrPos = movetoMin()
        print("Moving")
    """

"""
while True:
    dtime = measureFunc(CurrPos)
    print(dtime)
    if dtime < 1100:
        if CurrPos == MIN:
            led.value(0)
            CurrPos = movetoMax()
            print("Moving Up!")
    elif (dtime > 1100) and (dtime <= 2000):
        print("Yay")
    else:
        if CurrPos == MAX:
            led.value(1)
            CurrPos = movetoMin()
            print("Moving Down!")
"""