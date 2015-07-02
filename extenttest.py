
# Use the ArcPy Mapping module to obtain the extent of an MXD layout as a polygon feature

import arcpy
import arcpy.mapping as map

mxd = map.MapDocument(r'C:\projects\arcpy\newpark.mxd')

# Export a JPEG of the layout
# map.ExportToJPEG(mxd, r'C:\projects\arcpy\test.jpg', resolution=100)

# create an empty feature set

fs = arcpy.FeatureSet()

# get a  list of the data frames in the MXD
# loop through the list
# print the extent Geometry object in GeoJSON as a 2D envelope
# http://resources.arcgis.com/en/help/rest/apiref/geometry.html


for df in map.ListDataFrames(mxd):
    print df.extent.JSON
