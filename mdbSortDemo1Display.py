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
BGCOLOUR = (255,255,255)
#######################
# Class definition
#######################
class MdbSortDemo1Display:
  def __init__(self, s, t):
    self.display= ""
    self.size= s
    self.title= t
    self.surface= PYG.Surface((self.size, self.size), 0, 24)
    self.window= PYG.display.set_mode((self.size, self.size),0,24)
#######################
# Functions
#######################
#--------------------------------------------------------------
  def update(self, data, interval):
    PYG.display.set_caption(self.title)
    # Blank the screen and display the Vplot background
    PYG.draw.rect(self.surface, BGCOLOUR, self.window.get_rect())

    for i in range(len(data)):
      self.surface.set_at((int(data[i]), self.size - int(i)), (0, 0, 255))

    # Update the screen.
    self.window.blit(self.surface,(0,0))
    PYG.display.flip()

    sleep(interval)
#--------------------------------------------------------------
