# Use the ArcPy Mapping module to export a JPEG and obtain the extent of an MXD layout
# Note:  This script runs very slowly, so don't get impatient.

import arcpy
import arcpy.mapping

MapDoc = arcpy.mapping.MapDocument(r'C:\projects\arcpy\newpark.mxd')

outputpath = r'C:\projects\arcpy\test.jpg'

def exportMXDtoJPEG(MapDoc, outputpath):
    "Exports a MapDocument object to a JPEG saved in outputpath"
    arcpy.mapping.ExportToJPEG(MapDoc, outputpath, resolution=100)

exportMXDtoJPEG(MapDoc, outputpath)


# Extent of the DataFrame is exported in the coordinate system of the DataFrame
# This will need to be reprojected to NAD83 dec.deg. for Google Maps API 

for df in arcpy.mapping.ListDataFrames(MapDoc):
    
    dfextent = df.extent
    
    # check if data frame is already in WGS 1984
    # WKID 4326: GCS_WGS_1984 (decimal degrees)
    if not dfextent.spatialReference.factoryCode == 4326:
        dfextent = df.extent.projectAs(arcpy.SpatialReference(4326))  # WKID 4326: GCS_WGS_1984 (decimal degrees)
    
    
    print dfextent.spatialReference.factoryCode
    print dfextent.JSON
    
    
