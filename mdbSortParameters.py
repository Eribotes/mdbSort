#######################
# EXTERNAL MODULES
#######################
from optparse import OptionParser
#######################
# Class definition
#######################
class MdbSortParameters:
  def __init__(self, parameterList):
    self.parameterList= parameterList
    self.mode= 'DEMO2'
    self.inputFile= ''
    self.outputFile= ''
    self.statistics= 1
    self.modified= 0
    self.stable= 0
    self.pause= 0
    self.numElements= 160000
    self.initialOrder= 'RANDOM'
    self.status= 'OK'
    self.errors= []
    self.parseParameters()
#--------------------------------------------------------------
  def parseParameters(self):
    hlp= 'Usage: %prog [options]'
    parser= OptionParser(usage= hlp)
    parser.add_option('-i', '--inputFile', dest= 'iFile', metavar= 'FILE', help= 'Input filename')
    parser.add_option('-m', '--mode', dest= 'mode', metavar= 'FILE/DEMO1/DEMO2', help= 'Mode [DEMO2]')
    parser.add_option('-M', '--modified', dest= 'modified', action= 'store_true', default= False, help= 'Modified sort pass [False]')
    parser.add_option('-n', '--numElements', dest= 'numElements', metavar= 'n', help= 'Number of elements to sort [160000] [DEMO1/2 modes only]')
    parser.add_option('-o', '--outputFile', dest= 'oFile', metavar= 'FILE', help= 'Output filename [Must NOT exist]')
    parser.add_option('-p', '--pause', dest= 'pause', action= 'store_true', default= False, help= 'Insert a two second pause between sort passes [False]')
    parser.add_option("-r", "--random", dest= "random", action= "store_true", default= True, help= "Random order initial state [True] [DEMO1 mode only]")
    parser.add_option('-s', '--statistics', dest= 'statistics', action= 'store_true', default= False, help= 'Print statistics [True]')
    parser.add_option('-S', '--stable', dest= 'stable', action= 'store_true', default= False, help= 'Make the sort stable by adding a seconadry key [False]')
    options, arguments= parser.parse_args()

    if options.mode:
      if options.mode == 'FILE':
        self.mode= 'FILE'
      elif options.mode == 'DEMO1':
        self.mode= 'DEMO1'
      elif options.mode == 'DEMO2':
        self.mode= 'DEMO2'
      else:
        self.status= 'NOK'
        self.error.append('** Mode invalid: ' + mode)

    if options.iFile:
      if self.mode != 'FILE':
        self.status= 'NOK'
        self.errors.append('** Input file specified for non-FILE mode')
      else:
        self.inputFile= options.iFile
        try:
          iF= open(self.inputFile, 'r')
          iRec= 'initialised'
          self.numElements= 0
          while iRec != '':
            iRec= iF.readline()
            if iRec != '':
              self.numElements+= 1

          if self.numElements < 2:
            self.status= 'NOK'
            self.errors.append('** Input file has < 2 records')

          iF.close()
        except:
          self.status= 'NOK'
          self.errors.append('** Unable to read input file')

    if options.oFile:
      if self.mode != 'FILE':
        self.status= 'NOK'
        self.errors.append('** Output file specified for non-FILE mode')
      else:
        self.outputFile= options.oFile
        try:
          oF= open(self.outputFile, 'r')
          oF.close()
          self.status= 'NOK'
          self.errors.append('** Output file already exists')
        except:
          try:
            oF= open(self.outputFile, 'w')
            oF.close()
          except:
            self.status= 'NOK'
            self.errors.append('** Unable to create output file')

    if self.mode == 'FILE':
      if self.inputFile == '':
        self.status= 'NOK'
        self.errors.append('** FILE mode specified with no input file')
      if self.outputFile == '':
        self.status= 'NOK'
        self.errors.append('** FILE mode specified with no output file')

    if self.mode == 'DEMO1' or self.mode == 'DEMO2':
      if self.inputFile != '':
        self.status= 'NOK'
        self.errors.append('** Input file specified with DEMO1/2 mode')
      if self.outputFile != '':
        self.status= 'NOK'
        self.errors.append('** Output file specified with DEMO1/2 mode')

    if options.numElements:
      if self.mode == 'FILE':
        self.status= 'NOK'
        self.errors.append('** Number of element specified for FILE mode')
      else:
        self.numElements= int(options.numElements)
#--------------------------------------------------------------
