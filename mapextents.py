
import os
import os.path
import arcpy
import arcpy.mapping
import json
import geojson # https://pypi.python.org/pypi/geojson/1.2.0
import time
import datetime
from arcpy import env

print "working"

rootdir = r"M:\TenantAerials\ArcMap"
# rootdir = r"C:\test\input"
JPEGpath = r"C:\test\output"
PDFpath = r"C:\test\output"

JSONoutfile = r"C:\test\output\extents.json"

datadict = {}

# check if the JSON file exists
if os.path.exists(JSONoutfile):
    # read the current contents into the dictionary
    datadict = json.load(open(JSONoutfile, 'r'))

# sample code:  Get all of the map names from the datadict
#for x in datadict['features']:
#    print x['properties']['map']


def mxdwalk(rootdir):
    
    # returns a dictionary of MXD filenames and timestamps
    # key = full path and filename of mxd file
    # value = timestamp of last modification
    
    mxdfiles = {}  
    
    for (dirName, subdirList, fileList) in os.walk(rootdir):
        for fname in fileList:
            # test if a file is an .mxd
            if os.path.splitext(fname)[1].lower() == ".mxd":
                mxdfile = os.path.join(dirName, fname)
                # append filename and timestamp to dictionary as key
                # add the integer timestamp of last modification as value
                mxdfiles[mxdfile] = os.stat(mxdfile).st_mtime

    return mxdfiles


def GeoJSONfeature(extent, mapname, timestamp):
    "Converts Map Document Dataframe Extent object to a GeoJSON Polygon Feature"
    
    # build tuples of each corner point (x, y)
    UL = (extent.XMin, extent.YMax)  # upper-left corner of extent
    UR = (extent.XMax, extent.YMax)  # upper-right
    LR = (extent.XMax, extent.YMin)  # lower-right
    LL = (extent.XMin, extent.YMin)  # lower-left
    
    # build the GeoJSON Polygon feature
    pg = geojson.Polygon([[UL, UR, LR, LL, UL]])
    
    # build the GeoJSON Feature using the Polygon
    # add any additional Properties here

    datestamptext = datetime.date.fromtimestamp(timestamp)
    print "datestamp:", datestamptext

    # PROBLEM HERE
    # The timetext variable might need to be converted to a string
    # if it's some kind of Date object, it's not capable of being serialized into a JSON file
    # try converting it to a String

    fp = geojson.Feature(geometry=pg, properties=dict(map=mapname, modified=timestamp, timetext=str(datetime.date.fromtimestamp(timestamp))))

    print fp

    return fp


# Get all MXD files in the root directory and its subdirectories
mxdDictionary = mxdwalk(rootdir)

# Get a list of all MXD file paths
mxdPaths = mxdDictionary.keys()
mxdPaths.sort()

# Loop through all of the MXD files

# future:  Check an external data file to see if the timestamp has changed since the previous run

# Export a JPEG and PDF of the Layout
# Extract the Extent of each Data Frame in the Map Document

# create a list to store the extent geometries of each MXD as GeoJSON Features
geoJSONfeatures = []


for mxdPath in mxdPaths:
    print "processing: " + mxdPath
    
    JPEGfilename = os.path.splitext(os.path.split(mxdPath)[1])[0] + ".jpg"
    PDFfilename  = os.path.splitext(os.path.split(mxdPath)[1])[0] + ".pdf"

    mapname = os.path.splitext(os.path.split(mxdPath)[1])[0]

    timestamp = mxdDictionary[mxdPath]

    print "timestamp:", timestamp


    # Get the map document
    mxd = arcpy.mapping.MapDocument(mxdPath)
    
    # export the layout of the map document to a JPEG or PDF in the output path specified above
    
    # BUG NOTE:
    # the arcpy.mapping methods to export images seem to crash at some point when looping through files
    # it's an ESRI bug somewhere, apparently.
    # see: http://gis.stackexchange.com/questions/146477/python-crashes-when-running-arcpys-exporttopdf-exporttopng-exporttojpeg


    arcpy.mapping.ExportToJPEG(mxd, os.path.join(JPEGpath, JPEGfilename) , resolution=200)
    arcpy.mapping.ExportToPDF(mxd, os.path.join(PDFpath, PDFfilename),resolution=200, image_quality='BEST' )

    # WORKAROUND tested:
    # use the multiprocessing module to add freeze support
    # the Pickle module doesn't seem to like to use a Map object as a parameter

    for df in arcpy.mapping.ListDataFrames(mxd):
        dfextent = df.extent

        # check if data frame is already in WGS 1984
        # WKID 4326: GCS_WGS_1984 (decimal degrees)

        if not dfextent.spatialReference.factoryCode == 4326:
            # reproject to WGS84
            dfextent = df.extent.projectAs(arcpy.SpatialReference(4326))  # WKID 4326: GCS_WGS_1984 (decimal degrees)

        # get a GeoJSON Polygon Feature using the dataframe extent
        GeoFeature = GeoJSONfeature(dfextent, mapname, timestamp)

        # append the geo GeoJSON polygon to the list of all GeoJSON extents
        geoJSONfeatures.append(GeoFeature)
    
    time.sleep(10)

fc = geojson.FeatureCollection(geoJSONfeatures)
dump = geojson.dumps(fc)

with open(JSONoutfile, 'w') as JSONoutput:
    JSONoutput.write(dump)

print "done"
