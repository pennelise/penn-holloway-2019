#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
'''
Script to process KNMI DOMINO data from OMI.

Uses the version 1.1 interface

Outputs daily files, using the command-line IO interface

Attempts to incorporate all files potentially relevant to
each day (including the final file from the previous day).

Runs for both start and end day

Set up for the standard CONUS 36km domain

Uses "default" settings for averaging parameters
'''
# define the first and last days to process
startDay = '07-10-2007'
stopDay = '07-31-2007'

#-------------------------------------------------------------#
#-------------------END USER INPUT SECTION--------------------#
#-------------------------------------------------------------#

import os
import datetime
import subprocess
import glob
import pdb

# parse user input dates
startDT = datetime.datetime.strptime(startDay, '%m-%d-%Y')
stopDT = datetime.datetime.strptime(stopDay, '%m-%d-%Y')

# put together a list of datetimes to use throughout
dayDelta = datetime.timedelta(1)
timesList = []
while startDT <= stopDT:
    timesList.append(startDT)
    startDT += dayDelta

# dumb hack so we make a grid file on day 1 and that's it
dayone = True

for day in timesList:

    # initiate list that will become the call
    call = ['whips.py']
    
    # create the filelist and tack that and directory on
    directory = '/Users/Elise/penn_holloway/WHIPS/DOMINO/2007/'
    prefix = 'OMI-Aura_L2-OMDOMINO_' 
    today = glob.glob(os.path.join(directory, prefix+day.strftime('%Ym%m%d')+'*'))
    yesterday = glob.glob(os.path.join(directory, prefix+(day-dayDelta).strftime('%Ym%m%d')+'*'))
    try:
        flist = today+[yesterday[-1]]
    except IndexError:
        flist = today
    call.extend(['--directory', directory])
    call.extend(['--fileList']+flist)
    call.extend(['--filetype', 'OMI_NO2_KNMI_HDF_v2_0_postFeb2006_OMNO2d'])

    # create the grid projection and tack that on
    call.extend(['--gridProj', 'latlon'])
    gProj = ['xOrig:-126.0',
             'yOrig:24.0',
             'xCell:0.25',
             'yCell:0.25',
             'nRows:104',
             'nCols:240']
    call.extend(['--projAttrs']+gProj)

    # specify mapping function
    call.extend(['--mapFunc', 'OMNO2d_regional'])

    # create output function and specs
    # define the fields we want to process.
    inFields = ['TroposphericVerticalColumn']
              #['AveragingKernel','TroposphericVerticalColumn', 'AirMassFactor',
              # 'AirMassFactorTropospheric','TM4SurfacePressure',
              # 'TM4PressurelevelA', 'TM4PressurelevelB']
    outFields = ['tropVCD']
               #['avkern','tropVCD','AMF','tropAMF','TM4pSurf','TM4presLevA',
               # 'TM4presLevB']
    oAttrs = ['inFieldNames:'+','.join(inFields),
              'outFieldNames:'+','.join(outFields),
              'timeStart:00:00:00_'+day.strftime('%m-%d-%Y'),
              'timeStop:23:59:59_'+day.strftime('%m-%d-%Y'),
              'timeComparison:UTC',
              'fillVal:-9999',
              'cloudFractUpperCutoff:0.3',
              'solarZenAngUpperCutoff:85',
              'includePixelCount:True']
              
    call.extend(['--outFuncAttrs']+oAttrs)
    
    # output file information
    outDir = '/Users/Elise/penn_holloway/WHIPS-output/DOMINO/'
    call.extend(['--outDirectory', outDir])
    call.extend(['--outFileName', 'knmi_omi_minPix250_maxPix2100_0_25x0_25_CONUS_'+day.strftime('%m-%d-%Y')+'tropVCD_only'+'.nc'])

    if dayone:
        call.extend(['--includeGrid', os.path.join(outDir,'0_25x0_25_CONUS_gridfile.nc')])
        dayone = False
    
    # random other variables
    call.extend(['--verbose', 'True'])
    call.extend(['--interactive', 'False'])
    
    # print the call
    print call

    # execute the call
    subprocess.call(call)
