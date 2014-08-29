#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Code for the display for the Bloominglabs/Wonderlab Laser Tunnel

SDC 8/21/2014

TODO:

"""

import pygame
from pygame import *
import pygame.mixer

from credits import Credit
import sys
import time
import serial

text = """CREDITS
_                                                 _

_Construction Team_\\Jay Sissom
\\Stephen Charlesworth
\\Naomi Charlesworth
\\Kristy Kallback-Rose
\\David Rose
\\Tomoko Oishi

_Arduino and Raspberry Pi Programming_\\Jay Sissom
\\Stephen Charlesworth

_                                                 _

©Copyright 2014 by Bloominglabs
http://bloominglabs.org

For Wonderlab"""

#~ utiliser '\\' pour aligner les lignes de texte

# key constants
DISPLAY_WIDTH = 990
DISPLAY_HEIGHT = 500    
DISPLAY_SURF = display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
FPS = 30
NUM_SENSORS = 6
SENSOR_STATE = [0] * NUM_SENSORS


#serial stuff. for debugging purposes also allows keyboard input
SERIAL_MODE = False
SERIAL_PORT = "/dev/ttyACM0" #"/dev/tty.usbmodem1421" # change as appropriate

# Fonts
small_font = font.Font("./fonts/Roboto-MediumItalic.ttf",20)
medium_font = font.Font("./fonts/Roboto-MediumItalic.ttf",32)
big_font = font.Font("./fonts/Roboto-MediumItalic.ttf",64)
huge_font = font.Font("./fonts/Roboto-MediumItalic.ttf",80)
big_computer_font = font.Font("./fonts/Computer.ttf",100)
medium_computer_font = font.Font("./fonts/Computer.ttf",35)
big_LCD_font = font.Font("./fonts/LCD2 Bold.ttf",80)

# Images
wonderlab_img = pygame.image.load("./pix/wonderlab400x128.png")
blabs_img = pygame.image.load("./pix/blabsweirdfont990x180.png")

#sounds - pre init solved laggy sounds (mostly)
pygame.mixer.pre_init(44100,-16,2 ,256)
pygame.init()
pygame.mixer.music.set_volume(1)

click = pygame.mixer.Sound("./sounds/goodClick.ogg")
motion_detected = pygame.mixer.Sound("./sounds/motionDetected.ogg")
activating_alarm = pygame.mixer.Sound("./sounds/activatingAlarm.ogg")
intruder_alert = pygame.mixer.Sound("./sounds/IntruderAlert.ogg")

def draw_splash(display_surf):
    display_surf.fill((255,255,255))
    display_surf.blit(blabs_img,(0,0))
    display_surf.blit(wonderlab_img,(display_surf.get_size()[0]/2 - 
        wonderlab_img.get_size()[0]/2,240))
        
    time_surface_obj = big_font.render('and',True,(0,0,0),(255,255,255))
    text_rect_obj = time_surface_obj.get_rect()
    text_rect_obj.center = (
        display_surf.get_size()[0]/2 ,200)    
    display_surf.blit(time_surface_obj,text_rect_obj)
    
    time_surface_obj = big_font.render('present...',True,(0,0,0),(255,255,255))
    text_rect_obj = time_surface_obj.get_rect()
    text_rect_obj.center = (
        display_surf.get_size()[0]/2 ,
        display_surf.get_size()[1] - text_rect_obj.h)    
    display_surf.blit(time_surface_obj,text_rect_obj)
    
    pygame.display.update()
    time.sleep(2)

    display_surf.fill((0,0,0))    

    time_surface_obj = big_computer_font.render('Laser',True,(0,255,0),(0,0,0))
    text_rect_obj = time_surface_obj.get_rect()
    text_rect_obj.center = (
        display_surf.get_size()[0]/2 ,
        display_surf.get_size()[1]/3)    
    display_surf.blit(time_surface_obj,text_rect_obj)

    time_surface_obj = big_computer_font.render('Tunnel',True,(0,255,0),(0,0,0))
    text_rect_obj = time_surface_obj.get_rect()
    text_rect_obj.center = (
        display_surf.get_size()[0]/2 ,
        display_surf.get_size()[1]*2/3)    
    display_surf.blit(time_surface_obj,text_rect_obj)    
    pygame.display.update()
    time.sleep(2)

def get_serial_command(serial_port,stuff):
    line = ""
    ed = serial_port.read(10)
    while ed: 
        print "serial read: [%s]" % ed
        stuff = stuff + ed
        idx = stuff.find("\n")
        if idx > -1:
            line = stuff[:idx]
            print "got a line: [%s]" % line
            print "line has len [%s]" % len(line)
            if len(line):
                print "first char: [%s]" % line[0]
                line = line[0]
            stuff = stuff[idx+1:]
            break
        ed = serial_port.read(10) 
    return (stuff, line) 


FPS_CLOCK = pygame.time.Clock()
cred = Credit(text,small_font,(255,255,255),(0,0,0))
pygame.display.set_caption('Laser Tunnel')
DISPLAY_SURF.fill((255,255,255))
#draw_splash(DISPLAY_SURF)
GAME_STATE = "ATTRACT"
# also ARMED DISARMED ALERT
GAME_TIME = 0

try:
    serial_port = serial.Serial(SERIAL_PORT, 9600, timeout = 0)
    SERIAL_MODE = True
    print "Serial be live"
    # clean shit out
    while serial_port.read(10):
		pass
    
    
except:
    pass

serial_stuff = ""

"""
commands
A 'arm' (red button)
D 'disarm' (green button)
1 - 8 (indicates a line was touched)
X - quit
"""
armed = False
alert = False
time_increment = 0 

while True: # main game loop
    current_key = ""
    current_serial = "" 
    serial_command = ""
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:    
            current_key = str(unichr(event.key))
            # play the key sound
            print "%s pressed" % current_key

    if SERIAL_MODE == True:
        (serial_stuff, serial_command) = get_serial_command(serial_port,serial_stuff)
        if serial_command:
            print "Serial: [%s] %s" % (serial_command,len(serial_command))
            current_key = serial_command
               
    time_increment = FPS_CLOCK.tick(FPS)
    pygame.display.update()
