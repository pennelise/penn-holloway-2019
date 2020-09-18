import netCDF4
import numpy as np
import glob
import datetime

# Created by Elise Penn; last modified 09/17/2020.

baseDir = '/Volumes/Space/penn_holloway_github/' # CHANGE THIS to your directory path
omiDir  = '{}WHIPS-output/DOMINO/grid0_25x0_25/'.format(baseDir)
go2Dir  = '{}WHIPS-output/GOME2/grid0_25x0_25_no_big_pixels/'.format(baseDir)

omiPrefix = 'knmi_omi_minPix250_maxPix2100_0_25x0_25_CONUS_'
go2Prefix = 'nobigpixels_'
# go2Prefix = 'gome2_pixMin3150_pixMax5800_0_25x0_25_CONUS_'
omiSuffix = '*.nc'
go2Suffix = '*.nc' # because there are _only_trop.nc files which only have tropVCD and no AK, etc
# omiSuffix = 'cloudfrac_0.nc'
# go2Suffix = 'cloudfrac_0.nc'

outDir = '{}level3data/'.format(baseDir)
outLabel = '0_25x0_25_CONUS_OMNO2d'

startDay = '06-01-2007'
stopDay = '08-31-2007'

fillValue = -9999.0

startDT = datetime.datetime.strptime(startDay, '%m-%d-%Y')
stopDT = datetime.datetime.strptime(stopDay, '%m-%d-%Y')

# put together a list of datetimes to use throughout
dayDelta = datetime.timedelta(1)
timesList = []
while startDT <= stopDT:
    timesList.append(startDT)
    startDT += dayDelta

# initialize variables
dummyDataset = netCDF4.Dataset(
                               glob.glob(omiDir + omiPrefix + 
                               timesList[0].strftime('%m-%d-%Y') + omiSuffix)[0])
dataShape = np.shape(dummyDataset.variables['tropVCD'])
omiSum = np.zeros(dataShape,dtype='float64')
go2Sum = np.zeros(dataShape,dtype='float64')
nValidDays = np.zeros(dataShape,dtype='float64')
omiValidPixelsSum = np.zeros(dataShape,dtype='float64')
go2ValidPixelsSum = np.zeros(dataShape,dtype='float64')
omiAvg = np.empty(dataShape,dtype='float64')
omiAvg.fill(fillValue)
go2Avg = np.empty(dataShape,dtype='float64')
go2Avg.fill(fillValue)
fileListStr = ''

for day in timesList:
    omiFileName = glob.glob(
                    omiDir + omiPrefix + day.strftime('%m-%d-%Y') + omiSuffix)[0]
    go2FileName = glob.glob(
                    go2Dir + go2Prefix + day.strftime('%m-%d-%Y') + go2Suffix)[0]
    print(omiFileName)
    print(go2FileName)
    omiConc = netCDF4.Dataset(omiFileName).variables['tropVCD']
    go2Conc = netCDF4.Dataset(go2FileName).variables['tropVCD']
    omiValidPixels = netCDF4.Dataset(omiFileName).variables['ValidPixelCount']
    go2ValidPixels = netCDF4.Dataset(go2FileName).variables['ValidPixelCount']
    
    # if one of the datasets is missing, set missing to true
    missing = np.logical_or(
            omiConc==omiConc._FillValue, go2Conc==go2Conc._FillValue)

    # add concentration to the sum if the grid is present in both datasets
    omiSum = np.where(missing, omiSum, omiSum+omiConc)
    go2Sum = np.where(missing, go2Sum, go2Sum+go2Conc)
    # add valid pixels to see total number of pixels used for each grid
    omiValidPixelsSum = np.where(missing, omiValidPixelsSum, omiValidPixelsSum+omiValidPixels)
    go2ValidPixelsSum = np.where(missing, go2ValidPixelsSum, go2ValidPixelsSum+go2ValidPixels)
    # add 1 to nValidDays if the gridcell is present in both datasets
    nValidDays = np.where(missing, nValidDays, nValidDays+1.)
    # record the files used in this average
    fileListStr = ' '.join([fileListStr, omiFileName, go2FileName])

# Average all valid pixels. If there are no valid gridcells, input fillValue.
np.divide(omiSum, nValidDays, out=omiAvg, where=nValidDays!=0.)
np.divide(go2Sum, nValidDays, out=go2Avg, where=nValidDays!=0.)
# divide omiAvg by 10^15 to get units of molec./cm^2*10^15
omiAvg = np.where(omiAvg!=fillValue,omiAvg/(10.**15.),fillValue)

#Write out netcdf file
varDims = ['row', 'col']

#Output OMI file as a netCDF
outFidOmi = netCDF4.Dataset(
                    outDir+"OMI_"+outLabel+"_from"+startDay+"_to"+stopDay+".nc",
                    'w', format='NETCDF3_CLASSIC')
# create dimensions
outFidOmi.createDimension('row',dataShape[0])
outFidOmi.createDimension('col',dataShape[1])
# set all attributes
setattr(outFidOmi, 'Level_2_retrieval', 'KNMI DOMINO v2.0')
setattr(outFidOmi, 'File_start_date',startDay)
setattr(outFidOmi, 'File_end_date',stopDay)
setattr(outFidOmi, 'Input_files', fileListStr)
# assumes these attributes are same in all files
setattr(outFidOmi, 'Version', getattr(dummyDataset,'Version'))
setattr(outFidOmi, 'Projection', getattr(dummyDataset,'Projection'))
setattr(outFidOmi, 'Max_valid_cloud_fraction', 
        getattr(dummyDataset,'Max_valid_cloud_fraction'))
setattr(outFidOmi, 'Max_valid_solar_zenith_angle', 
        getattr(dummyDataset,'Max_valid_solar_zenith_angle'))
setattr(outFidOmi, 'Time_comparison_scheme', 
        getattr(dummyDataset,'Time_comparison_scheme'))
# write out NO2 concentration variable
varHandle = outFidOmi.createVariable(
                      'NO2Conc', 'd', varDims, fill_value=fillValue)
varHandle[:] = omiAvg
# write out num valid pixels variable
varHandle2 = outFidOmi.createVariable(
                      'nValidPixels', 'd', varDims, fill_value=fillValue)
varHandle2[:] = omiValidPixelsSum
# write out num valid days variable
varHandle3 = outFidOmi.createVariable(
                      'nValidDays', 'd', varDims, fill_value=fillValue)
varHandle3[:] = nValidDays
outFidOmi.close()

#Output GOME2 file as a netCDF
outFidGo2 = netCDF4.Dataset(
                  outDir+"GOME2_"+outLabel+"_from"+startDay+"_to"+stopDay+".nc",
                  'w', format='NETCDF3_CLASSIC')
# create dimensions
outFidGo2.createDimension('row',dataShape[0])
outFidGo2.createDimension('col',dataShape[1])
# set all attributes
setattr(outFidGo2, 'Level_2_retrieval', 'KNMI GOME-2 v2.3')
setattr(outFidGo2, 'File_start_date',startDay)
setattr(outFidGo2, 'File_end_date',stopDay)
setattr(outFidGo2, 'Input_files', fileListStr)
# assumes these attributes are same in all files
setattr(outFidGo2, 'Version', getattr(dummyDataset,'Version'))
setattr(outFidGo2, 'Projection', getattr(dummyDataset,'Projection'))
setattr(outFidGo2, 'Max_valid_cloud_fraction', 
        getattr(dummyDataset,'Max_valid_cloud_fraction'))
setattr(outFidGo2, 'Max_valid_solar_zenith_angle', 
        getattr(dummyDataset,'Max_valid_solar_zenith_angle'))
setattr(outFidGo2, 'Time_comparison_scheme', 
        getattr(dummyDataset,'Time_comparison_scheme'))
# write out NO2 concentration variable
varHandle = outFidGo2.createVariable(
                      'NO2Conc', 'd', varDims, fill_value=fillValue)
varHandle[:] = go2Avg
# write out num valid pixels variable
varHandle2 = outFidGo2.createVariable(
                      'nValidPixels', 'd', varDims, fill_value=fillValue)
varHandle2[:] = go2ValidPixelsSum
# write out num valid days variable
varHandle3 = outFidGo2.createVariable(
                      'nValidDays', 'd', varDims, fill_value=fillValue)
varHandle3[:] = nValidDays
outFidGo2.close()
