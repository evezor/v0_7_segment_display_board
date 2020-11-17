#7-segment Display v1.0p test code

from machine import Pin
from pyb import CAN, ADC
import utime


print(" 7-Segment Display board test")
print("v1.0")
print("initializing")
can = CAN(1, CAN.NORMAL)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))


#Setup Pins
hbt_led = Pin("D13", Pin.OUT)
func_butt = Pin("D5", Pin.IN, Pin.PULL_UP) 
can_wakeup = Pin("D6", Pin.OUT)
can_wakeup.value(0)

DIGITS_1 = ["A0", "A1", "A2", "A3"]
DIGITS_2 = ["E13", "E14", "E15", "E17"]

SEGMENTS_1 = ["E4", "E3", "D0", "D1", "E2", "E1", "A5", "A4"]
SEGMENTS_2 = ["E11", "E10", "SD_DETECT", "E8", "E7", "E6", "E5", "E12"]

for i in range(len(DIGITS_1)):
    DIGITS_1[i] = Pin(DIGITS_1[i], Pin.OUT)
    DIGITS_1[i].value(1)    #Be sure to write these pins HIGH during initilization
    
for i in range(len(DIGITS_2)):
    DIGITS_2[i] = Pin(DIGITS_2[i], Pin.OUT)
    DIGITS_2[i].value(1)    #Be sure to write these pins HIGH during initilization

for i in range(len(SEGMENTS_1)):
    SEGMENTS_1[i] = Pin(SEGMENTS_1[i], Pin.OUT)
    SEGMENTS_1[i].value(0)

for i in range(len(SEGMENTS_2)):
    SEGMENTS_2[i] = Pin(SEGMENTS_2[i], Pin.OUT)
    SEGMENTS_2[i].value(0)

    
    
#Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
hbt_led.value(hbt_state)


print("starting")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            hbt_led.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            hbt_led.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

def chk_buttons():
    global next_button_chk
    now = utime_ms()
    if utime.ticks_diff(next_button_chk, now) <= 0:
        pass
        

def send():
    can.send('EVZRTST', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
    segments_chase()
        
def segments_chase():
    print("Display 1 chase sequence")
    for i in range(len(DIGITS_1)):
        DIGITS_1[i].value(0)
        for j in range(len(SEGMENTS_1)):
            SEGMENTS_1[j].value(1)
            utime.sleep_ms(50)
            SEGMENTS_1[j].value(0)
        DIGITS_1[i].value(1)
    print("Display 2 chase sequence")
    for i in range(len(DIGITS_2)):
        DIGITS_2[i].value(0)
        for j in range(len(SEGMENTS_2)):
            SEGMENTS_2[j].value(1)
            utime.sleep_ms(50)
            SEGMENTS_2[j].value(0)
        DIGITS_2[i].value(1)
      
while True:
    chk_hbt()
    if not (func_butt.value()):
        print("function button")
        send()
        segments_chase()
        utime.sleep_ms(200)
    
    if(can.any(0)):
        get()
        