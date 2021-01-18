#!/bin/env python
import sys
import os
import commands
import glob

datasets = []
blocks = [
    "/SingleMuon/Run2016H-ZMu-07Aug17-v1/RAW-RECO#141d02d0-8650-11e7-9af5-02163e0184a6",
	"/SingleMuon/Run2016B-ZMu-07Aug17_ver2-v1/RAW-RECO#ddf76db8-8167-11e7-9af5-02163e0184a6",
	"/SingleMuon/Run2016C-ZMu-07Aug17-v1/RAW-RECO#1a4de264-817d-11e7-9af5-02163e0184a6",
	"/SingleMuon/Run2016D-ZMu-07Aug17-v1/RAW-RECO#06639f50-8aec-11e7-a42c-001e67abefa8",
	"/SingleMuon/Run2016E-ZMu-07Aug17-v1/RAW-RECO#6efbb766-7f96-11e7-a42c-001e67abefa8",
	"/SingleMuon/Run2016F-ZMu-07Aug17-v1/RAW-RECO#06bf27be-921a-11e7-9adb-001e67abf518",
	"/SingleMuon/Run2016G-ZMu-07Aug17-v1/RAW-RECO#1a182cf8-9967-11e7-bd98-001e67abefa8",
	"/SingleMuon/Run2016H-ZMu-07Aug17-v1/RAW-RECO#141d02d0-8650-11e7-9af5-02163e0184a6",
	"/SingleMuon/Run2017B-ZMu-17Nov2017-v1/RAW-RECO#19263ab0-d7b5-11e7-aa2a-02163e01b396",
	"/SingleMuon/Run2017C-ZMu-17Nov2017-v1/RAW-RECO#0580dc82-d84a-11e7-aa2a-02163e01b396",
	"/SingleMuon/Run2017D-ZMu-17Nov2017-v1/RAW-RECO#0bed5830-decf-11e7-aa2a-02163e01b396",
	#"/SingleMuon/Run2017E-ZMu-17Nov2017-v1/RAW-RECO#11c265d6-e1d4-11e7-b157-02163e01b46e",
	"/SingleMuon/Run2017F-ZMu-17Nov2017-v1/RAW-RECO#0bd812f2-e11f-11e7-aa2a-02163e01b396",
	"/SingleMuon/Run2018A-ZMu-17Sep2018-v2/RAW-RECO#02e473af-4162-4cbd-b89d-3344140cbef9",
	#"/SingleMuon/Run2018B-ZMu-17Sep2018-v1/RAW-RECO#1bf74a4e-6d8c-453f-8ec6-32cc86c305cf",
	"/SingleMuon/Run2018C-ZMu-17Sep2018-v1/RAW-RECO#1f3da39a-b5c3-44ca-9c8a-7e6f4cd789a5",
	"/SingleMuon/Run2018D-ZMu-PromptReco-v2/RAW-RECO#00b6daf6-f61c-4822-9971-4c0f0ac8cb06",
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
    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/%s" % folder)

    if os.path.exists("/nfs/dust/cms/user/kutznerv/%s/%s" % (folder, ifile.split("/")[-1])):
        print "already there"
        continue
    
    os.system("cp /pnfs/desy.de/cms/tier2/%s ~/dust/%s/" % (ifile, folder))