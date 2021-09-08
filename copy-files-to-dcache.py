#!/bin/env python
import sys
import os
import commands
import glob
import fnmatch
import os
import time

#folder = "/nfs/dust/cms/user/kutznerv/store/"
#folder = "/nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/"
folder = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RERECO/"

matches = []
for root, dirnames, filenames in os.walk(folder):
    for filename in fnmatch.filter(filenames, '*'):
        matches.append(os.path.join(root, filename))    
                
print matches
     
for i_ifile, ifile in enumerate(matches):
       
    print i_ifile, "/", len(matches), ifile
    folder = "/".join(ifile.split("/")[:-1])
    
    folder = folder.replace("/nfs/dust/cms/user/kutznerv/", "")
    
    cmd = "eval `scram unsetenv -sh`; gfal-mkdir srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/vkutzner/%s" % folder
    #print cmd
    os.system(cmd)
    #cmd = "eval `scram unsetenv -sh`; gfal-copy srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/%s srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/vkutzner/%s/" % (ifile, folder)
    cmd = "eval `scram unsetenv -sh`; gfal-copy %s srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/vkutzner/%s/" % (ifile, folder)
    os.system(cmd)
    #print cmd

    if i_ifile+1%1000==0:
        time.sleep(60)