#!/usr/bin/env python3
#######################
# EXTERNAL MODULES
#######################
import os, sys
import random
from mdbSortGenerateDataFileParameters import MdbSortGenerateDataFileParameters
#######################
# MAIN
#######################

if __name__ == '__main__':

  parameterList= sys.argv
  params= MdbSortGenerateDataFileParameters(parameterList)

  if params.status:
    print('Parameter Error:')
    for item in params.errors:
      print('****', item)

    sys.exit()

  for item in params.errors:
    print('****', item)

  print()
  print('Element count:     ', params.numElements)
  print('InitialOrder:      ', params.initialOrder)
  print('Output File Name:  ', params.outputFile)
  print()

  # Generate reverse range
  t= range(params.numElements - 1, -1, -1)
  data= []

  for item in t:
    data.append(str(item).zfill(10) + '\n')

  # Randomise if random initial order
  if params.initialOrder == 'random':
    random.shuffle(data)

  # Write the data
  # First check that the file doesn't already exist
  if os.path.lexists(params.outputFile):
    print('Output file already exists')
    sys.exit()
  else:
    # Nope, so write the data
    try:
      print('Write output file...')
      f= open(params.outputFile, 'w')
      fs= f.writelines(data)
      f.close()
      print('Write output file...Ok')
    except:
      print('Unable to create output file')
