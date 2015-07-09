
# top-level file
#
# This will be the final working application
# Code developed in other files will be incorporated into this file as it is completed


import os.path
import arcpy
import arcpy.mapping
import geojson # https://pypi.python.org/pypi/geojson/1.2.0

rootdir = r'C:\projects\arcpy'
# rootdir = r"C:\projects\EDCU\EDCU 2012\MXD files"
JPEGpath = r"C:\test\output"


def mxdwalk(rootdir):
    
    # create empty dictionary
    # key = full path and filename of mxd file
    # value = timestamp last modification
    
    mxdfiles = {}  
    
    for (dirName, subdirList, fileList) in os.walk(rootdir):
        for fname in fileList:
            # test if a file is an .mxd
            if os.path.splitext(fname)[1].lower() == ".mxd":
                mxdfile = os.path.join(dirName, fname)
                # append filename and timestamp to dictionary
                # index 8 of os.stat(file) is the integer timestamp of last modification
                mxdfiles[mxdfile] = os.stat(mxdfile)[8]

    return mxdfiles


def extentGeoJSONfeature(extent):
    "Converts Map Document Dataframe Extent object to a GeoJSON Polygon Feature"
    
    # build tuples of each corner point (x, y)
    UL = (extent.XMin, extent.YMax)  # upper-left corner of extent
    UR = (extent.XMax, extent.YMax)  # upper-right
    LR = (extent.XMax, extent.YMin)  # lower-right
    LL = (extent.XMin, extent.YMin)  # lower-left
    
    # build the GeoJSON Polygon
    pg = geojson.Polygon([[UL, UR, LR, LL, UL]])
    
    # build the GeoJSON Feature using the Polygon
    fp = geojson.Feature(geometry=pg)
    
    return fp



########  START THE FUN  ########

# Get all MXD files in the root directory and its subdirectories
mxdDictionary = mxdwalk(rootdir)

# Get a list of all MXD file paths
mxdPaths = mxdDictionary.keys()
mxdPaths.sort()

# Loop through all of the MXD files
# future:  Check an external data file to see if the timestamp has changed since the previous run
# Export a JPEG of the Layout
# Extract the Extent of each Data Frame in the Map Document

# create a list to store the extent geometries of each MXD as GeoJSON Features
geoJSONfeatures = []

for mxdPath in mxdPaths:
    JPEGfilename = os.path.splitext(os.path.split(mxdPath)[1])[0] + ".jpg"
    
    # Get the map document
    mxd = arcpy.mapping.MapDocument(mxdPath)
    
    # export the layout of the map document to a JPEG in the output path specified above
    # arcpy.mapping.ExportToJPEG(mxd, os.path.join(JPEGpath, JPEGfilename) , resolution=100)
    
    for df in arcpy.mapping.ListDataFrames(mxd):
        dfextent = df.extent
        
        # check if data frame is already in WGS 1984
        # WKID 4326: GCS_WGS_1984 (decimal degrees)
        if not dfextent.spatialReference.factoryCode == 4326:
            dfextent = df.extent.projectAs(arcpy.SpatialReference(4326))  # WKID 4326: GCS_WGS_1984 (decimal degrees)
        
        # reproject to WGS84 and append the Extent to the list of GeoJSON Features
        ext = extentGeoJSONfeature(dfextent)
        geoJSONfeatures.append(ext)


fc = geojson.FeatureCollection(geoJSONfeatures)
dump = geojson.dumps(fc)

print dump


