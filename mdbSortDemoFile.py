#!/usr/bin/env python3
#######################
# EXTERNAL MODULES
#######################
from mdbSortData import               MdbSortData
from mdbSortEngine import             MdbSortEngine
from mdbSortDemoFileParameters import MdbSortDemoFileParameters
from mdbSortTimer import              MdbSortTimer
import os, sys
import time
#######################
# Functions
#######################
def issuePrompt():
  vnul= input('Press ENTER to Continue')
#######################
# MAIN
#######################
if __name__ == '__main__':

  parameterList= sys.argv
  params= MdbSortDemoFileParameters(parameterList)

  if params.status:
    print('Parameter Error:')
    for item in params.errors:
      print('****', item)

    sys.exit()

  # Check that the output file does not already exist
  # First check that the file doesn't already exist
  if os.path.lexists(params.outputFile):
    print('Output file already exists')
    sys.exit()

  mdbSort= MdbSortData('FILE', params.inputFile, -1, '')

  if mdbSort.status:
    for item in mdbSort.errors:
      print('**', item)

  mdbSortEngine= MdbSortEngine(mdbSort.data, mdbSort.numDimensions, mdbSort.offsets, params.maxDimensions, params.keyLength, params.scheme, params.stable, params.order)

  # Create and start the timer
  mdbSortTimer= MdbSortTimer()
  mdbSortTimer.startTimer()

  if params.statistics:
    print()
    print('Input file:        ', params.inputFile)
    print('Output file:       ', params.outputFile)
    print('Element count:     ', mdbSort.numElements)
    print('Dimensions:        ', mdbSort.numDimensions)
    print('Test Offsets:      ', mdbSort.offsets)
    print('Sort Order:        ', params.order)
    print('Key Length:        ', params.keyLength)
    print('Max Dimensions:    ', params.maxDimensions)
    print('Scheme:            ', params.scheme)
    print('Stable:            ', params.stable)
    print('Statistics:        ', params.statistics)
    print()

    print('Start time:        ', mdbSortTimer.start)
    print()
    print('Iteration Statistics:')
    print('=====================')

  if params.order == 'DOUBLESORT':
    if params.statistics:
      print('Sort Ascending:')
    mdbSortEngine.sortOrder= 'ASCENDING'
    while mdbSortEngine.iterStatistics[3] != 0:

      mdbSortEngine.iterate()

      if params.statistics:
        for item in mdbSortEngine.iterStatistics:
          print(item, end= ' ')

        print()

    if params.statistics:
      print('=====================')
      print('Cumulative Statistics (Ascending phase):')
      print(mdbSortEngine.cumuStatistics)
      print('=====================')
      print('Sort Descending:')

    mdbSortEngine.resetStatistics()
    mdbSortEngine.sortOrder= 'DESCENDING'

    while mdbSortEngine.iterStatistics[3] != 0:

      mdbSortEngine.iterate()

      if params.statistics:
        for item in mdbSortEngine.iterStatistics:
          print(item, end= ' ')

        print()

    if params.statistics:
      print('=====================')
      print('Cumulative Statistics (Descending phase):')
      print(mdbSortEngine.cumuStatistics)
      print('=====================')

  else:
    while mdbSortEngine.iterStatistics[3] != 0:

      mdbSortEngine.iterate()

      if params.statistics:
        for item in mdbSortEngine.iterStatistics:
          print(item, end= ' ')

        print()

    if params.statistics:
      print('=====================')
      print('Cumulative Statistics:')
      print(mdbSortEngine.cumuStatistics)
      print('=====================')

  if params.outputFile:
    try:
      f= open(params.outputFile, 'w')
      fs= f.writelines(mdbSortEngine.data)
      f.close()
    except:
      print('Unable to create output file')
    pass
  else:
    for item in mdbSort.data:
      print(item[:-1])

  # Stop the timer
  mdbSortTimer.stopTimer()
  if params.statistics:
    print()
    print('Finish time: ', mdbSortTimer.stop)
    print('Elapsed time:', mdbSortTimer.elapsed)
    print()
