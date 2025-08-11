#!/usr/bin/env python
#######################
# EXTERNAL MODULES
#######################
from datetime import datetime, timedelta
#######################
# Class definition
#######################
class MdbSortTimer:
  def __init__(self):
    self.start= datetime.now()
    self.stop= datetime.now()
    self.elapsed= self.stop - self.start
#--------------------------------------------------------------
  def startTimer(self):
    self.start= datetime.now()
#--------------------------------------------------------------
  def stopTimer(self):
    self.stop= datetime.now()
    self.elapsed= self.stop - self.start
#--------------------------------------------------------------
