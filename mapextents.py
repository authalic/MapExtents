
# top level

# Search a path for all MXD files
# Create a dictionary, containing:
#    full path filename (string)
#    timestamp of last modification (integer)
#    coordinates of layout extent (list of doubles)
#       reproject to WGS84 or include the CRS in the GeoJSON
#    path to exported image (string)
# Store the dictionary in some kind of persistent data structure (JSON, xml, or pickle)
# for each run of the application...
#    locate and list each mxd file
#       if the file has not been modified since the last run, move to the next mxd file..
#    open the file and export a JPEG of the layout to an images folder
#    export the extent of the layout (JSON or a polygon shapefile)
#    (re)export the layout and extent info to GeoJSON file

import os
import geojson # https://pypi.python.org/pypi/geojson/1.2.0

rootdir = r"Y:\maps"

# open the existing data file

mxddata = open(r'mxddatafile.json', 'r')


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


# geojson sample code
# creates and exports a GeogJSON polygon (extent) from four input points 

# create the Polygon
pg = geojson.Polygon([[(-111.898898, 40.764253), (-111.891796, 40.764253), (-111.891796, 40.758667), (-111.898898, 40.758667), (-111.898898, 40.764253)]])

# create a Feature from the Polygon
fp1 = geojson.Feature(geometry=pg)

# create a FeatureCollection from the Feature
fcpoly = geojson.FeatureCollection([fp1])

# additional Features can be added to the FeatureCollection using .update([Feature])  maybe.

# encode the FeatureCollection to GeoJson 
polydump = geojson.dumps(fcpoly)

print(polydump)


