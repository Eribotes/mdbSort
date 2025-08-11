#!/usr/bin/env python
#######################
# EXTERNAL MODULES
#######################
from datetime import datetime, timedelta
import random
#######################
# Globals
#######################
BRIGHTEST= (256 * 6) - 1
#######################
# Class definition
#######################
class MdbSortEngine:
  def __init__(self, data, numDimensions, offsets, maxDimensions, keyLength, scheme, stable, sortOrder):
    self.data= data
    self.numDimensions= numDimensions
    self.maxDimensions= maxDimensions
    self.activeDimensions= self.maxDimensions
    self.iteration= 0
    self.offsets= offsets
    self.sortOrder= sortOrder
    self.keyLength= keyLength
    self.scheme= scheme
    self.stable= 0
    self.window= -1
    self.stableKeys= []
    self.numElements= 0
    self.indexList= []
    self.iterStatistics= [0]
    self.cumuStatistics= [0]
    self.initialise()
#--------------------------------------------------------------
  def initialise(self):
    self.numElements= len(self.data)
    self.indexList= range(self.numElements)

    # Nax dimension checks
    if self.maxDimensions == -1:
      self.maxDimensions= self.numDimensions
      self.activeDimensions= self.numDimensions
    elif self.maxDimensions > self.numDimensions:
      self.maxDimensions= self.numDimensions
      self.activeDimensions=self.numDimensions

    self.iterStatistics= [0] * (self.maxDimensions + 4)
    self.cumuStatistics= [0] * (self.maxDimensions + 3)

    self.iterStatistics[3]= -1

    if self.stable:
      for i in range(self.numElements):
        self.stableKeys.append(str(i).zfill(8))
    else:
      self.stableKeys= [str(0).zfill(8)] * self.numElements

    if self.window == -1:
      self.window= self.numDimensions
#--------------------------------------------------------------
  def resetStatistics(self):
    self.iteration= 0
    self.activeDimensions= self.maxDimensions
    self.iterStatistics= [0] * (self.numDimensions + 4)
    self.iterStatistics[3]= -1
    self.cumuStatistics= [0] * (self.numDimensions + 3)
#--------------------------------------------------------------
  def iterate(self):
    for i in range(len(self.iterStatistics)):
      self.iterStatistics[i]= 0

    self.iterStatistics[0]= self.iteration
    self.cumuStatistics[0]= self.iteration

    w= self.activeDimensions - self.window
    if w < 1:
      w= 1

    if self.scheme == 'basic':
      if self.stable:
        self.sortPassBasicStable(w)
      else:
        self.sortPassBasicUnstable(w)
    elif self.scheme == 'bug':
      if self.stable:
        self.sortPassBugStable(w)
      else:
        self.sortPassBugUnstable(w)
    elif self.scheme == 'modified':
      if self.stable:
        self.sortPassModifiedStable(w)
      else:
        self.sortPassModifiedUnstable(w)

    self.iteration+= 1

    for i in range(1, len(self.cumuStatistics)):
      self.cumuStatistics[i]+= self.iterStatistics[i + 1]

    # Reduce the activeDimensions as they become inactive
    l= 1
    while l:
      if self.iterStatistics[self.activeDimensions + 3] == 0:
        self.activeDimensions-= 1
      else:
        l= 0

    self.iterStatistics[1]= self.activeDimensions
#--------------------------------------------------------------
  def sortPassBasicUnstable(self, w):
    for i in self.indexList:
      d= self.activeDimensions
      loop= 1
      swap= 0
      while loop:
        t= i + self.offsets[d - 1]
        # Check that we're still within bounds
        if t < self.numElements:
          self.iterStatistics[2]+= 1 # Increment num of tests
          # Compare...
          if self.sortOrder == 'ASCENDING':
            if self.data[i][:self.keyLength] > self.data[t][:self.keyLength]:
              swap= 1
          elif self.sortOrder == 'DESCENDING':
            if self.data[i][:self.keyLength] < self.data[t][:self.keyLength]:
              swap= 1

          if swap:
            # Yes, so swap...
            sbuff= self.data[t]
            self.data[t]= self.data[i]
            self.data[i]= sbuff
            self.iterStatistics[d + 3]+= 1 # Increment sswaps for dimension
            self.iterStatistics[3]+= 1 # Increments tot swaps
            swap= 0
            loop= 0

          # No, so check we can drop down a dimension
          elif d > w:
            # Yes, so try the next dimesion
            d-= 1
          # No, so exit
          else:
            loop= 0
        # No, we've exceeded bounds so try to drop down a dimension...
        elif d > w:
          d-= 1
        # No, so exit...
        else:
          loop= 0
#--------------------------------------------------------------
  def sortPassBasicStable(self, w):
    for i in self.indexList:
      d= self.activeDimensions
      loop= 1
      swap= 0
      while loop:
        t= i + self.offsets[d - 1]
        # Check that we're still within bounds
        if t < self.numElements:
          self.iterStatistics[2]+= 1 # Increment num of tests
          # Compare...
          if self.sortOrder == 'ASCENDING':
            if (self.data[i][:self.keyLength] > self.data[t][:self.keyLength]) and (self.stableKeys[i] > self.stableKeys[t]):
              swap= 1
          elif self.sortOrder == 'DESCENDING':
            if (self.data[i][:self.keyLength] < self.data[t][:self.keyLength]) and (self.stableKeys[i] < self.stableKeys[t]):
              swap= 1

          if swap:
            # Yes, so swap...
            sbuff= self.data[t]
            self.data[t]= self.data[i]
            self.data[i]= sbuff
            self.iterStatistics[d + 3]+= 1
            self.iterStatistics[3]+= 1
            swap= 0
            loop= 0

          # No, so check we can drop down a dimension
          elif d > w:
            # Yes, so try the next dimesion
            d-= 1
          # No, so exit
          else:
            loop= 0
        # No, we've exceeded bounds so try to drop down a dimension...
        elif d > w:
          d-= 1
        # No, so exit...
        else:
          loop= 0
#--------------------------------------------------------------
  def sortPassBugUnstable(self, w):
    for i in self.indexList:
      d= self.activeDimensions
      loop= 1
      swap= 0
      while loop:
        t= i + self.offsets[d - 1]
        # Check that we're still within bounds
        if t < self.numElements:
          self.iterStatistics[2]+= 1 # Increment num of tests
          # Compare...
          if self.sortOrder == 'ASCENDING':
            if self.data[i][:self.keyLength] > self.data[t][:self.keyLength]:
              swap= 1
          elif self.sortOrder == 'DESCENDING':
            if self.data[i][:self.keyLength] < self.data[t][:self.keyLength]:
              swap= 1

          if swap:
            # Yes, so swap...
            sbuff= self.data[t]
            self.data[t]= self.data[i]
            self.data[i]= sbuff
            self.iterStatistics[d + 3]+= 1
            self.iterStatistics[3]+= 1
            swap= 0

          # No, so check we can drop down a dimension
          elif d > w:
            # Yes, so try the next dimesion
            d-= 1
          # No, so exit
          else:
            loop= 0
        # No, we've exceeded bounds so try to drop down a dimension...
        elif d > w:
          d-= 1
        # No, so exit...
        else:
          loop= 0
#--------------------------------------------------------------
  def sortPassBugStable(self, w):
    for i in self.indexList:
      d= self.activeDimensions
      loop= 1
      swap= 0
      while loop:
        t= i + self.offsets[d - 1]
        # Check that we're still within bounds
        if t < self.numElements:
          self.iterStatistics[2]+= 1 # Increment num of tests
          # Compare...
          if self.sortOrder == 'ASCENDING':
            if (self.data[i][:self.keyLength] > self.data[t][:self.keyLength]) and (self.stableKeys[i] > self.stableKeys[t]):
              swap= 1
          elif self.sortOrder == 'DESCENDING':
            if (self.data[i][:self.keyLength] < self.data[t][:self.keyLength]) and (self.stableKeys[i] < self.stableKeys[t]):
              swap= 1

          if swap:
            # Yes, so swap...
            sbuff= self.data[t]
            skbuf= self.stableKeys[t]

            self.data[t]= self.data[i]
            self.stableKeys[t]= self.stableKeys[i]

            self.data[i]= sbuff
            self.stableKeys[i]= skbuf

            self.iterStatistics[d + 3]+= 1
            self.iterStatistics[3]+= 1
            swap= 0

          # No, so check we can drop down a dimension
          elif d > w:
            # Yes, so try the next dimesion
            d-= 1
          # No, so exit
          else:
            loop= 0
        # No, we've exceeded bounds so try to drop down a dimension...
        elif d > w:
          d-= 1
        # No, so exit...
        else:
          loop= 0
#--------------------------------------------------------------
  def sortPassModifiedUnstable(self, w):
    for i in self.indexList:
      p= i
      d= self.activeDimensions
      loop= 1
      swap= 0
      while loop:
        t= p + self.offsets[d - 1]
        # Check that we're still within bounds
        if t < self.numElements:
          self.iterStatistics[2]+= 1 # Increment num of tests
          # Compare...
          if self.sortOrder == 'ASCENDING':
            if self.data[p][:self.keyLength] > self.data[t][:self.keyLength]:
              swap= 1
          elif self.sortOrder == 'DESCENDING':
            if self.data[p][:self.keyLength] < self.data[t][:self.keyLength]:
              swap= 1

          if swap:
            # Yes, so swap...
            sbuff= self.data[t]
            self.data[t]= self.data[p]
            self.data[p]= sbuff
            self.iterStatistics[d + 3]+= 1
            self.iterStatistics[3]+= 1
            p= t
            swap= 0

          # No, so check we can drop down a dimension
          elif d > w:
            # Yes, so try the next dimesion
            d-= 1
          # No, so exit
          else:
            loop= 0
        # No, we've exceeded bounds so try to drop down a dimension...
        elif d > w:
          d-= 1
        # No, so exit...
        else:
          loop= 0
#--------------------------------------------------------------
  def sortPassModifiedStable(self, w):
    for i in self.indexList:
      p= i
      d= self.activeDimensions
      loop= 1
      swap= 0
      while loop:
        t= i + self.offsets[d - 1]
        # Check that we're still within bounds
        if t < self.numElements:
          self.iterStatistics[2]+= 1 # Increment num of tests
          # Compare...
          if self.sortOrder == 'ASCENDING':
            if (self.data[i][:self.keyLength] > self.data[t][:self.keyLength]) and (self.stableKeys[i] > self.stableKeys[t]):
              swap= 1
          elif self.sortOrder == 'DESCENDING':
            if (self.data[i][:self.keyLength] < self.data[t][:self.keyLength]) and (self.stableKeys[i] < self.stableKeys[t]):
              swap= 1

          if swap:
            # Yes, so swap...
            sbuff= self.data[t]
            self.data[t]= self.data[p]
            self.data[p]= sbuff
            self.iterStatistics[d + 3]+= 1
            self.iterStatistics[3]+= 1
            p= t
            swap= 0

          # No, so check we can drop down a dimension
          elif d > w:
            # Yes, so try the next dimesion
            d-= 1
          # No, so exit
          else:
            loop= 0
        # No, we've exceeded bounds so try to drop down a dimension...
        elif d > w:
          d-= 1
        # No, so exit...
        else:
          loop= 0
#--------------------------------------------------------------
