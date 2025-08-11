#!/usr/bin/env python
#######################
# EXTERNAL MODULES
#######################
import random
#######################
# Globals
#######################
HIGHVAL= (256 * 6) - 1
#######################
# Class definition
#######################
class MdbSortData:
  def __init__(self, mode, inputFile, numElements, initialOrder):
    self.data= []
    self.mode= mode
    self.inputFile= inputFile
    self.numElements= numElements
    self.initialOrder= initialOrder
    self.numDimensions= 0
    self.offsets= []
    self.status= 0
    self.errors= []
    self.initialise()
#--------------------------------------------------------------
  def initialise(self):
    # Generate the demo data
    if self.mode == 'FILE':
      self.getFileData()
    elif self.mode == 'DEMO1':
      self.generateDemo1Data()
    elif self.mode == 'DEMO2':
      self.generateDemo2Data()

    self.numDimensions, self.offsets= self.calcDimsOffsets(self.numElements)
#--------------------------------------------------------------
  def getFileData(self):
    try:
      ipf= open(self.inputFile, 'r')
      ipfRec= "initialised"
      self.numElements= 0
      while ipfRec != "":
        ipfRec= ipf.readline()
        if ipfRec != "":
          self.data.append(ipfRec)
          self.numElements+= 1

      ipf.close()
    except:
      self.status= 1
      self.errors.append('Unable to open input file')
#--------------------------------------------------------------
  def generateDemo1Data(self):
    # Generate reverse order data
    for i in range(self.numElements - 1, -1, -1):
      self.data.append(str(i).zfill(8))

    # If random order is required then ramdomise the reverse ordered data
    if self.initialOrder == 'random':
      # Create a temp list for the rendomisation process
      t= []
      for i in range(self.numElements):
        j= int(random.random() * (self.numElements - i))
        t.append(self.data[j])
        vnull= self.data.pop(j)

      # Copy the data back from the temp list
      for i in range(self.numElements):
        self.data.append(t[i])

      # Delete the temp list
      del t
#--------------------------------------------------------------
  def generateDemo2Data(self):
    if self.initialOrder == 'random':
      print('initialOrder == random:', self.initialOrder)
      # Set all to random values
      for i in range(self.numElements):
        self.data.append(str(int((random.random() * HIGHVAL) - 1)).zfill(8))

    else:
      print('initialOrder == reverse:', self.initialOrder)
      v= HIGHVAL
      for i in range(self.numElements):
        self.data.append(str(int(v)).zfill(8))
        v-= 1
        if v < 0:
          v= HIGHVAL

      self.data= sorted(self.data, reverse= 1)
#--------------------------------------------------------------
  def calcDimsOffsets(self, n):
    nd= 1
    t= 1
    os= [1]
    while t < n / 2:
      t*= 2
      os.append(t)
      nd+= 1

    return nd, os
#--------------------------------------------------------------
