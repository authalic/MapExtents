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
    # {"xmin":454071.06987482228,"ymin":4507675.2277499037,"xmax":454589.22443413141,"ymax":4508387.6991748465,"spatialReference":{"wkid":26912,"latestWkid":26912}}
    
    newdf = df.extent.projectAs(arcpy.SpatialReference(4326))  # WKID 4326: GCS_WGS_1984 (decimal degrees)
    
    print newdf.JSON
    # {"xmin":-111.54385862989017,"ymin":40.718719659772312,"xmax":-111.53767161146764,"ymax":40.725166537926839,"spatialReference":{"wkid":4326,"latestWkid":4326}}
    
