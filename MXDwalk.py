
# Walk through a drive or directory, recusively.
# produces a list of MXD files, with full path, and last-modified date

import os

rootDir = r'Y:\maps'

mxdCount = 0

for (dirName, subdirList, fileList) in os.walk(rootDir):
    for fname in fileList:
        if os.path.splitext(fname)[1] == ".mxd":
            print(os.path.join(dirName, fname))
            mxdCount+=1

print("done: %i files found" % mxdCount)