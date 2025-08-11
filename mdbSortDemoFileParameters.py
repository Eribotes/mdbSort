#######################
# EXTERNAL MODULES
#######################
from optparse import OptionParser
#######################
# Class definition
#######################
class MdbSortDemoFileParameters:
  def __init__(self, parameterList):
    self.parameterList= parameterList
    self.inputFile=''
    self.outputFile= ''
    self.dimensions= 0
    self.keyLength= 10
    self.scheme= 'bug'
    self.order= 'ASCENDING'
    self.maxDimensions= -1
    self.stable= 0
    self.statistics= 0
    self.status= 0
    self.errors= []
    self.parseParameters()
#--------------------------------------------------------------
  def parseParameters(self):
    hlp= 'Usage: %prog [options]'
    parser= OptionParser(usage= hlp)
    parser.add_option('-a', '--ascending', dest= 'ascending', action= 'store_true', default= True, help= 'Sort to ascending order [True]')
    parser.add_option('-d', '--descending', dest= 'descending', action= 'store_true', default= False, help= 'Sort to descending order [False]')
    parser.add_option('-D', '--doubleSort', dest= 'doubleSort', action= 'store_true', default= False, help= 'Sort ascending then descending [False]')
    parser.add_option('-i', '--inputFile', dest= 'inputFile', metavar= 'str', help= 'Input File')
    parser.add_option('-l', '--keyLength', dest= 'keyLength', metavar= 'n', help= 'Key Length [10]')
    parser.add_option('-m', '--maxDimensions', dest= 'maxDimensions', metavar= 'n', help= 'Maximum num of dims when testing')
    parser.add_option('-o', '--outputFile', dest= 'outputFile', metavar= 'str', help= 'Output File (MUST NOT EXIST)')
    parser.add_option('-s', '--scheme', dest= 'scheme', metavar= 'str', help= 'Sort scheme (basic/bug/modified) [basic]')
    parser.add_option('-S', '--stable', dest= 'stable', action= 'store_true', default= False, help= 'Make the sort stable by adding a secondary key [False]')
    parser.add_option('-z', '--statistics', dest= 'statistics', action= 'store_true', default= False, help= 'Print statistics [False]')
    options, arguments= parser.parse_args()

    if options.ascending:
      self.order= 'ASCENDING'

    if options.descending:
      self.order= 'DESCENDING'

    if options.doubleSort:
      self.order= 'DOUBLESORT'

    if options.inputFile:
      self.inputFile= options.inputFile
    else:
      self.errors.append('No input file specified')
      self.status= 1

    if options.keyLength:
      self.keyLength= int(options.keyLength)

    if options.maxDimensions:
      self.maxDimensions= int(options.maxDimensions)

    if options.outputFile:
      self.outputFile= options.outputFile

    if options.scheme:
      if options.scheme == 'basic':
        self.scheme= 'basic'
      elif options.scheme == 'bug':
        self.scheme= 'bug'
      elif options.scheme == 'modified':
        self.scheme= 'modified'
      else:
        self.errors.append('scheme not basic/bug/modified')
        self.status= 1

    if options.stable:
      self.stable= 1

    if options.statistics:
      self.statistics= 1
#--------------------------------------------------------------
