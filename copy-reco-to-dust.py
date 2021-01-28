#!/bin/env python
import sys
import os
import commands
import glob

target = "/nfs/dust/cms/user/kutznerv"
copy_from_desy_dcache = True

datasets = []
blocks = [
    "/SingleMuon/Run2017C-ZMu-09Aug2019_UL2017-v1/RAW-RECO#1b049b00-9bb7-47f1-9cf4-f41771a76211",
]
files = []

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
        os.system("cp /pnfs/desy.de/cms/tier2/%s ~/dust/%s/" % (ifile, folder))
    else:
        os.system("xrdcp root://cmsxrootd.fnal.gov/%s ~/dust%s" % (ifile, ifile))
    
    