# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:49:03 2019

@author: Cmdr Raghul
Sources:
http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
https://pythonprogramming.net/direct-input-game-python-plays-gta-v/
https://www.raspberrypi.org/forums/viewtopic.php?t=19969
"""

import pygame
import sys
import time
import ctypes

SendInput = ctypes.windll.user32.SendInput

Z = 0x2C
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
X = 0x2D

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
def FlightAssistOff():
    PressKey(X)
    time.sleep(0.1) 
    ReleaseKey(X)

    PressKey(Z)
    time.sleep(0.1) 
    ReleaseKey(Z)

def FlightAssistOn():
    PressKey(Z)
    time.sleep(0.1) 
    ReleaseKey(Z)
    PressKey(D)
    time.sleep(0.1) 
    ReleaseKey(D)

total = 1000
actual = 0
toggle = 0
lasttoggle = 0

pygame.joystick.init()
pygame.init()

print (pygame.joystick.get_count())

_joystick = pygame.joystick.Joystick(0)
_joystick.init()
print (_joystick.get_init())
print (_joystick.get_id())
print (_joystick.get_name())
print (_joystick.get_numaxes())
print (_joystick.get_numballs())
print (_joystick.get_numbuttons())
print (_joystick.get_numhats())

pressbit = 0

try:
    while True:

        if pressbit == 1:
            
            pressbit = 0
        pygame.event.get()
        actual = ((_joystick.get_axis(1))+(actual*(total-1)))/total
        
        if ((actual >= 0.95) or (actual <= -0.95)):
            
            lasttoggle = toggle
            toggle = 1
        else:
            lasttoggle = toggle      
            toggle = 0

        if (lasttoggle != toggle):
            if toggle == 1:
                print ("Flight assist off")
                FlightAssistOff()
                pressbit = 1
                
            else:
                print("Flight assist on")
                FlightAssistOn()
                pressbit = 1
            lasttoggle = toggle
            


except KeyboardInterrupt:
    quit()
