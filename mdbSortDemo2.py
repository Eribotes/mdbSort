#!/usr/bin/env python3
#######################
# EXTERNAL MODULES
#######################
from mdbSortData import            MdbSortData
from mdbSortEngine import          MdbSortEngine
from mdbSortDemo2Parameters import MdbSortDemo2Parameters
from mdbSortDemo2Display import    MdbSortDemo2Display
from mdbSortTimer import           MdbSortTimer
import sys
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
  params= MdbSortDemo2Parameters(parameterList)

  if params.status:
    print('Parameter Error:')
    for item in params.errors:
      print('****', item)

    sys.exit()

  mdbSortData= MdbSortData('DEMO2', '', params.numElements, params.initialOrder)

  mdbSortEngine= MdbSortEngine(mdbSortData.data, mdbSortData.numDimensions, mdbSortData.offsets, params.maxDimensions, params.keyLength, params.scheme, params.stable, params.order)

  # Get the window dims
  winSize= int(params.numElements**0.5)
  if winSize**2 < params.numElements:
    winSize+= 1

  print()
  print('Element count:     ', params.numElements)
  print('Dimensions:        ', mdbSortData.numDimensions)
  print('InitialOrder:      ', params.initialOrder)
  print('Interval:          ', params.interval)
  print('Test Offsets:      ', mdbSortData.offsets)
  print('Window Size:       ', winSize)
  print('Sort Order:        ', params.order)
  print('Key Length:        ', params.keyLength)
  print('Max Dimensions:    ', params.maxDimensions)
  print('Scheme:            ', params.scheme)
  print('Prompt:            ', params.prompt)
  print('Stable:            ', params.stable)
  print('Wait (sleep):      ', params.wait)
  print()

  display= MdbSortDemo2Display(winSize, 'mdbSortDemo2')

  display.update(mdbSortData.data, params.interval)

  # Create and start the timer
  mdbSortTimer= MdbSortTimer()
  mdbSortTimer.startTimer()
  print('Start time:        ', mdbSortTimer.start)
  print()
  print('Iteration Statistics:')
  print('=====================')

  if params.order == 'DOUBLESORT':
    print('Sort Ascending:')
    mdbSortEngine.sortOrder= 'ASCENDING'
    while mdbSortEngine.iterStatistics[3] != 0:

      mdbSortEngine.iterate()
      display.update(mdbSortEngine.data, params.interval)

      for item in mdbSortEngine.iterStatistics:
        print(item, end= ' ')

      print()
      if params.prompt:
        issuePrompt()

    print('=====================')
    print('Cumulative Statistics (Ascending phase):')
    print(mdbSortEngine.cumuStatistics)
    print('=====================')
    print('Sort Descending:')

    mdbSortEngine.resetStatistics()
    mdbSortEngine.sortOrder= 'DESCENDING'

    while mdbSortEngine.iterStatistics[3] != 0:

      mdbSortEngine.iterate()
      display.update(mdbSortEngine.data, params.interval)

      for item in mdbSortEngine.iterStatistics:
        print(item, end= ' ')

      print()
      if params.prompt:
        issuePrompt()

    print('=====================')
    print('Cumulative Statistics (Descending phase):')
    print(mdbSortEngine.cumuStatistics)
    print('=====================')

  else:
    while mdbSortEngine.iterStatistics[3] != 0:

      mdbSortEngine.iterate()
      display.update(mdbSortEngine.data, params.interval)

      for item in mdbSortEngine.iterStatistics:
        print(item, end= ' ')

      print()
      if params.prompt:
        issuePrompt()

    print('=====================')
    print('Cumulative Statistics:')
    print(mdbSortEngine.cumuStatistics)
    print('=====================')

  # Stop the timer
  mdbSortTimer.stopTimer()
  print()
  print('Finish time: ', mdbSortTimer.stop)
  print('Elapsed time:', mdbSortTimer.elapsed)
  print()

  if params.wait:
    print('Sleeping...', params.wait, 'seconds...')
    time.sleep(params.wait)
