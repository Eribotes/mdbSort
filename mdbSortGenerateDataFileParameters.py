#######################
# EXTERNAL MODULES
#######################
from optparse import OptionParser
#######################
# Class definition
#######################
class MdbSortGenerateDataFileParameters:
  def __init__(self, parameterList):
    self.parameterList= parameterList
    self.numElements= 1000000
    self.initialOrder= 'random'
    self.outputFile= ''
    self.status= 0
    self.errors= []
    self.parseParameters()
#--------------------------------------------------------------
  def parseParameters(self):
    hlp= 'Usage: %prog [options]'
    parser= OptionParser(usage= hlp)
    parser.add_option('-i', '--initialOrder', dest= 'initialOrder', metavar= 'str', help= 'Initial Order of data (random/reverse) [random]')
    parser.add_option('-n', '--numElements', dest= 'numElements', metavar= 'n', help= 'Number of elements to sort [1000000]')
    parser.add_option('-o', '--outputFile', dest= 'outputFile', metavar= 'str', help= 'Output File (MUST NOT EXIST)')
    options, arguments= parser.parse_args()

    if options.initialOrder:
      if options.initialOrder == 'random':
        self.initialOrder= 'random'
      elif options.initialOrder == 'reverse':
        self.initialOrder= 'reverse'
      else:
        self.errors.append('initailOrder not random/reverse')
        self.status= 1

    if options.numElements:
      self.numElements= int(options.numElements)

    if options.outputFile:
      self.outputFile= options.outputFile
    else:
      self.errors.append('No outputFile name specified')
      self.status= 1
#--------------------------------------------------------------
