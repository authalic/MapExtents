import arcpy
import os.path

rootdir = r'C:\projects'
outpath = r'C:\test\output'

for (dirName, subdirList, fileList) in os.walk(rootdir):
    for filename in fileList:
        # test if a file is an .mxd
        if os.path.splitext(filename)[1].lower() == ".mxd":
            
            mxdfile = os.path.join(dirName, filename)
            
            mxd = arcpy.mapping.MapDocument(mxdfile)
            print "MXD Path: " + mxd.filePath + "\n"
            
            arcpy.mapping.ExportToJPEG(mxd, os.path.join(outpath, filename[:-3] + "jpg"))

print("done")