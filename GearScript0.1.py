from machine import Pin, PWM
import time
import utime

pwm = PWM(Pin(16))
pwm.freq(200)
pwm_duty = 3000
pwm.duty_u16(pwm_duty)
servo = PWM(Pin(15))
servo.freq(50)
servo2 = PWM(Pin(18))
servo2.freq(50)

MID = 1500000
MIN = 1000000
MAX = 2000000

targetTime = 5
incrementTime = 0.01
increment = (((MAX/MIN) * incrementTime) / targetTime)

input_pin1 = Pin(5, Pin.IN)
input_pin2 = Pin(7, Pin.IN)

def measureFunc1():
    while input_pin1.value() == 0:
        pass
    start = time.ticks_us()
    while input_pin1.value() == 1:
        pass
    end = time.ticks_us()
    duty = end - start
    return duty

def measureFunc2():
    while input_pin2.value() == 0:
        pass
    start = time.ticks_us()
    while input_pin2.value() == 1:
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
        time.sleep(incrementTime)
        if position1 < MAX:
            position1 += increment
            servo.duty_ns(position1)
        if position2 < MAX:
            position2 += increment
            if position2 >= MIN:
                servo2.duty_ns(position2)
    return position2

def movetoMin():
    position1 = MAX
    position2 = MAX + 100000
    actualPosition1 = False
    actualPosition2 = False
    while position2 > MIN:
        time.sleep(incrementTime)
        if position1 > MIN:
            position1 -= increment
            servo.duty_ns(position1)
        if position2 > MIN:
            position2 -= increment
            if position2 <= MAX:
                servo2.duty_ns(position2)
        print(position1, position2)
    return position2
    
CurrPos = MIN
duty1 = 0
duty2 = 0
switchPos = None

while True:
    if measureFunc2() - measureFunc1() > 400:
        switchPos = 0
    elif measureFunc2() - measureFunc1() < -400:
        switchPos = 1
        
    if switchPos == 0 and CurrPos == MAX:
        CurrPos = movetoMin()
    elif switchPos == 1 and CurrPos == MIN:
        CurrPos = movetoMax()
 
    print(measureFunc2() - measureFunc1())
