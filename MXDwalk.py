
# Walk through a drive or directory, recusively.
# produces a dictionary of MXD files, with full path, and last-modified datestamp

import os

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
