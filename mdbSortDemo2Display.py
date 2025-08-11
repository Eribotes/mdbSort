#######################
# EXTERNAL MODULES
#######################
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as PYG
from pygame.locals import *
from time import sleep
#######################
# GLOBALS
#######################
BRIGHTEST= (256 * 6) - 1
#######################
# Class definition
#######################
class MdbSortDemo2Display:
  def __init__(self, s, t):
    self.display= ""
    self.size= s
    self.title= t
    self.surface= PYG.Surface((self.size, self.size), 0, 24)
    self.window= PYG.display.set_mode((self.size, self.size),0,24)
    self.initialise()
#######################
# Functions
#######################
  def initialise(self):
    # open pygame PYG_window
    PYG.init()
    self.surface= PYG.Surface((self.size, self.size), 0, 24)
    self.window= PYG.display.set_mode((self.size, self.size),0,24)
    PYG.display.set_caption(self.title)
#--------------------------------------------------------------
  def update(self, data, interval):

    x= 0
    y= 0

    for item in data:
      c= int(item)
      d= int(c / 256)
      if d == 0:
        cr= c
        cg= 0
        cb= 0
      elif d == 1:
        cr= 255
        c= c - (d * 256)
        cg= c
        cb= 0
      elif d == 2:
        cg= 255
        c= c - (d * 256)
        cr= 255 - c
        cb= 0
      elif d == 3:
        cg= 255
        c= c - (d * 256)
        cb= c
        cr= 0
      elif d == 4:
        cb= 255
        c= c - (d * 256)
        cg= 255 - c
        cr= 0
      elif d == 5:
        cb= 255
        c= c - (d * 256)
        cr= c
        cg= c

      self.surface.set_at((x, y), (cr, cg, cb))

      x= x + 1
      if x >= self.size:
        x= 0
        y= y + 1
        if y >= self.size:
          y= 0

    # Update the screen.
    self.window.blit(self.surface,(0,0))
    PYG.display.flip()

    sleep(interval)
#--------------------------------------------------------------
