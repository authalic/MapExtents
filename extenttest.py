# Use the ArcPy Mapping module to export a JPEG and obtain the extent of an MXD layout
# Note:  This script runs very slowly, so don't get impatient.

import arcpy
import arcpy.mapping

mxd = arcpy.mapping.MapDocument(r'C:\projects\arcpy\newpark.mxd')

# Export a JPEG of the layout
arcpy.mapping.ExportToJPEG(mxd, r'C:\projects\arcpy\test.jpg', resolution=100)

# Extent of the DataFrame is exported in the coordinate system of the DataFrame
# This will need to be reprojected to NAD83 dec.deg. for Google Maps API 

for df in arcpy.mapping.ListDataFrames(mxd):
    print df.extent.JSON
    newdf = df.extent.projectAs(arcpy.SpatialReference(4326))  # WKID 4326: GCS_WGS_1984 (decimal degrees)
    print newdf.JSON
