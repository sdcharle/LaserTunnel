#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pygame import *
font.init()

class Credit:
    def __init__(self,text,font,text_color,bg_color, surface_origin, surface_size):
        self.done = False
        self.font = font 
        self.surface_origin = surface_origin
        try: text = text.decode('utf-8')
        except: pass
        
        try: self.text_color = Color(text_color)
        except: self.text_color = Color(*text_color)
        
        try: self.bg_color = Color(bg_color)
        except: self.bg_color = Color(*bg_color) 

        self.scr = Surface((surface_size))
        #display.get_surface()
        self.scrrect = self.scr.get_rect()
        self.bg = self.scr.copy() # ???

        w,h = self.font.size(' ')
        Rright = self.scrrect.centerx + w*3
        Rleft = self.scrrect.centerx - w*3

        self.text_array = []
        for i,l in enumerate(text.splitlines()):
            a,b,c = l.partition('\\')
            u = False
            if a:
                if a.startswith('_') and a.endswith('_'):
                    u = True
                    a = a.strip('_')
                rect = Rect((0,0),self.font.size(a))
                if b: rect.topright = Rleft,self.scrrect.bottom+h*i
                else: rect.midtop = self.scrrect.centerx,self.scrrect.bottom+h*i
                self.text_array.append([a,rect,u])
            u = False
            if c:
                if c.startswith('_') and c.endswith('_'):
                    u = True
                    c = c.strip('_')
                rect = Rect((0,0),self.font.size(c))
                rect.topleft = Rright,self.scrrect.bottom+h*i
                self.text_array.append([c,rect,u])

        self.y = 0
        self.text_copy = [x for x in self.text_array]

    def reset(self):
		self.text_array = [x for x in self.text_copy]

    def advance_credit(self):
        self.scr.fill(self.bg_color)
        self.y -= 2
        for p in self.text_array[:]:
            r = p[1].move(0,self.y)
            if r.bottom < 0:
                self.text_array.pop(0)
                if not self.text_array:
                  self.done = True
                  self.text_array = [x for x in self.text_copy]
                  self.y = 0
                continue
            if not isinstance(p[0],Surface):
                if p[2]: self.font.set_underline(1)
                p[0] = self.font.render(p[0],1,self.text_color)
                self.font.set_underline(0)
            self.scr.blit(p[0],r)
            if r.top >= self.scrrect.bottom:
                break
 #       self.clk.tick(70)
 #       display.flip()
 #       self.scr.fill(self.bg_color)
#        self.scr.blit(self.bg,(0,0))

