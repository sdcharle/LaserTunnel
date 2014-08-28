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
SERIAL_PORT = "/dev/tty.usbmodem1421" # change as appropriate

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

"""

show simple panel. Basically just: is alarm armed or not,
and are we safe or was ALERT TRIGGERED

show dots for our sensors also.
Green for not triggered, red for triggered

"""
def draw_panel(display_surf, armed, alert):
    w_margin = 20 # add to args?
    h_margin = 20
    
    rect_width = (DISPLAY_WIDTH - 4*w_margin)/3
    rect_height = (DISPLAY_HEIGHT - 2*h_margin)


    ARMED_COLOR = (255,0,0)
    DISARMED_COLOR = (0,255,0)

    if armed:
        armed_str = "ARMED"
        armed_color = ARMED_COLOR
    else:
        armed_str = "DISARMED"
        armed_color = DISARMED_COLOR
    
    if alert:
        alert_str = "ALERT"
        alert_color = ARMED_COLOR
    else:
        alert_str = "SECURE"
        alert_color = DISARMED_COLOR
       
    display_surf.fill((30,30,30))
    
    big_left_width = (DISPLAY_WIDTH*2/3 - 2*w_margin)
    
    pygame.draw.rect(display_surf, armed_color, 
        (w_margin, h_margin, big_left_width, 
            DISPLAY_HEIGHT/2 - (3*h_margin/2)) ,0)
#    pygame.draw.rect(display_surf, alert_color, (2*w_margin + rect_width, h_margin, rect_width, rect_height) ,0)

    pygame.draw.rect(display_surf, (0,0,0), 
       (3*w_margin + 2*rect_width, h_margin, rect_width, rect_height) ,0)    

    text_surface_obj = medium_computer_font.render(armed_str,True,(0,0,0),armed_color)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (
        w_margin + big_left_width/2 ,
        DISPLAY_HEIGHT/3 - h_margin)    
    display_surf.blit(text_surface_obj,text_rect_obj)

# draw the friendly sensors
    sensor_y = DISPLAY_HEIGHT * 3/4
    sensor_width = big_left_width / (NUM_SENSORS + 1)
    
    for (idx, sens_val) in enumerate(SENSOR_STATE):
        if SENSOR_STATE[idx]:
            color = ARMED_COLOR
        else:
            color = DISARMED_COLOR
        pygame.draw.circle(display_surf, color, (w_margin + (1+idx) * sensor_width,sensor_y),
            big_left_width/(NUM_SENSORS * 4), 0)
    
#    text_surface_obj = medium_computer_font.render(alert_str,True,(0,0,0),alert_color)
#    text_rect_obj = text_surface_obj.get_rect()
#    text_rect_obj.center = (
#        w_margin * 2+ rect_width*3/2 ,
#        DISPLAY_HEIGHT/2)    
#    display_surf.blit(text_surface_obj,text_rect_obj)
      
    time_str = "%02d:%02d" % (GAME_TIME/60000, (GAME_TIME % 60000)/1000)
    time_surface_obj = big_LCD_font.render(time_str,True,(255,0,0),(0,0,0))
    time_rect_obj = time_surface_obj.get_rect()
    time_rect_obj.center = (
        display_surf.get_size()[0]/2 + rect_width,display_surf.get_size()[1]/2)    
    display_surf.blit(time_surface_obj,time_rect_obj)
 
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
        stuff = stuff + ed
        idx = stuff.find("\n")
        if idx > -1:
            line = stuff[:idx]
            stuff = stuff[idx+1:]
            break
        ed = serial_port.read(10) 
    return (stuff, line) 


FPS_CLOCK = pygame.time.Clock()
cred = Credit(text,small_font,(255,255,255),(0,0,0))
pygame.display.set_caption('Laser Tunnel')
DISPLAY_SURF.fill((255,255,255))
draw_splash(DISPLAY_SURF)
GAME_STATE = "ATTRACT"
# also ARMED DISARMED ALERT
GAME_TIME = 0

try:
    serial_port = serial.Serial(SERIAL_PORT, 9600, timeout = 0)
    SERIAL_MODE = True
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
            print "Serial: %s" % serial_command
            current_key = serial_command
            
    if current_key == "a":
        GAME_STATE = "ARMED"
        armed = True
        alert = False #???
        GAME_TIME = 0 # actually depends. allow pause/reset
        click.play()
        activating_alarm.play()
        SENSOR_STATE = [0] * NUM_SENSORS
    elif current_key == "d":
        armed = False
        alert = False #?
        click.play() # ugh. need another sound.
        GAME_STATE = "DISARMED"
        SENSOR_STATE = [0] * NUM_SENSORS
    elif current_key and ((ord(current_key) - ord("1") < NUM_SENSORS and ord(current_key) >= ord("1"))):
        if GAME_STATE == "ARMED":
            SENSOR_STATE[ord(current_key) - ord("1")] = 1
            intruder_alert.play()
            alert = True
            
    elif current_key == "x" or serial_command == "x":
        pygame.quit()
        sys.exit()            
            
    if GAME_STATE == "ATTRACT":
        if not cred.done:
            cred.advance_credit()
        else:
            GAME_STATE = "DISARMED"
            print "end of credits"

# go through state-specific activities

    if GAME_STATE == "ARMED":
        if not alert:
            GAME_TIME = GAME_TIME + time_increment
        draw_panel(DISPLAY_SURF, armed, alert)    
 
    if GAME_STATE == "DISARMED":
        draw_panel(DISPLAY_SURF, armed, alert)
    
    time_increment = FPS_CLOCK.tick(FPS)
    pygame.display.update()
