#!/bin/env python
import sys
import os
import commands
import glob

########### configure ###########

target = "/nfs/dust/cms/user/kutznerv"
copy_from_desy_dcache = False
copy_to_desy_dcache = True

datasets = []
blocks = [
    "/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW#0149acf0-6b06-43c9-b99f-dfc531b6eecb",
]
files = []

########### configure ###########

for dataset in datasets:
    status, output = commands.getstatusoutput("""dasgoclient --query="file dataset=%s" """ % dataset)
    files += output.split("\n")

for block in blocks:
    status, output = commands.getstatusoutput("""dasgoclient --query="file block=%s" """ % block)
    files += output.split("\n")

print files

for ifile in files:
    
    print ifile
    folder = "/".join(ifile.split("/")[:-1])
    os.system("mkdir -p %s/%s" % (target, folder))

    if os.path.exists("%s/%s/%s" % (target, folder, ifile.split("/")[-1])):
        print "already there"
        continue
    
    if copy_from_desy_dcache:
        cmd = "cp /pnfs/desy.de/cms/tier2/%s ~/dust/%s/" % (ifile, folder)
        os.system(cmd)
    elif copy_to_desy_dcache:
        cmd = "gfal-mkdir srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/vkutzner/%s" % folder
        os.system(cmd)
        print cmd
        cmd = "gfal-copy srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/%s srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/store/user/vkutzner/%s/" % (ifile, folder)
        os.system(cmd)
    else:
        os.system("xrdcp root://cmsxrootd.fnal.gov/%s ~/dust%s" % (ifile, ifile))
    
    