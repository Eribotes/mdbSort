#######################
# EXTERNAL MODULES
#######################
from optparse import OptionParser
#######################
# Class definition
#######################
class MdbSortDemo1Parameters:
  def __init__(self, parameterList):
    self.parameterList= parameterList
    self.dimensions= 0
    self.initialOrder= 'random'
    self.interval= 0
    self.keyLength= 8
    self.scheme= 'bug'
    self.numElements= 200
    self.order= 'ASCENDING'
    self.maxDimensions= -1
    self.prompt= 0
    self.stable= 0
    self.wait= 0
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
    parser.add_option('-i', '--initialOrder', dest= 'initialOrder', metavar= 'string', help= 'Initial Order of data (random/reverse) [random]')
    parser.add_option('-I', '--interval', dest= 'interval', metavar= 'n', help= 'interval in seconds between sort passes [0]')
    parser.add_option('-l', '--keyLength', dest= 'keyLength', metavar= 'n', help= 'Key Length [8]')
    parser.add_option('-m', '--maxDimensions', dest= 'maxDimensions', metavar= 'n', help= 'Maximum num of dims when testing')
    parser.add_option('-n', '--numElements', dest= 'numElements', metavar= 'n', help= 'Number of elements to sort [200]')
    parser.add_option('-p', '--prompt', dest= 'prompt', action= 'store_true', default= False, help= 'prompt to continue between sort passes [False]')
    parser.add_option('-s', '--scheme', dest= 'scheme', metavar= 'string', help= 'Sort scheme (basic/bug/modified) [bug]')
    parser.add_option('-S', '--stable', dest= 'stable', action= 'store_true', default= False, help= 'Make the sort stable by adding a secondary key [False]')
    parser.add_option('-W', '--wait', dest= 'wait', metavar= 'n', help= 'Wait (sleep) seconds after finish [0]')
    options, arguments= parser.parse_args()

    if options.ascending:
      self.order= 'ASCENDING'

    if options.descending:
      self.order= 'DESCENDING'

    if options.doubleSort:
      self.order= 'DOUBLESORT'

    if options.initialOrder:
      if options.initialOrder == 'random':
        self.initialOrder= 'random'
      elif options.initialOrder == 'reverse':
        self.initialOrder= 'reverse'
      else:
        self.errors.append('initailOrder not random/reverse')
        self.status= 1

    if options.interval:
      self.interval= int(options.interval)

    if options.keyLength:
      self.keyLength= int(options.keyLength)

    if options.maxDimensions:
      self.maxDimensions= int(options.maxDimensions)

    if options.numElements:
      self.numElements= int(options.numElements)

    if options.prompt:
      self.prompt= 1

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

    if options.wait:
      self.wait= int(options.wait)
#--------------------------------------------------------------
