#!/bin/env python
import GridEngineTools
import os
import glob
import plot
from os.path import expanduser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--submit", dest = "submit", action="store_true")
parser.add_option("--hadd", dest = "hadd", action="store_true")
(options, args) = parser.parse_args()

periods = [
            "Summer16",
            "Fall17",
            "Autumn18",
            "Run2016B",
            "Run2016C",
            "Run2016D",
            "Run2016E",
            "Run2016F",
            "Run2016G",
            "Run2016H",
            "Run2017B",
            "Run2017C",
            "Run2017D",
            "Run2017E",
            "Run2017F",
            "Run2018A",
            "Run2018B",
            "Run2018C",
            "Run2018D",
            "RunUL2017C",
            #"Fall17UL",
          ]
          
suffixes = [
            "",
            "low",
            "medium", 
            "high",
            "Barrel",
            "Endcap", 
            #"lowBarrel",
            #"lowEndcap", 
            #"mediumBarrel",
            #"mediumEndcap",
            #"highBarrel", 
            #"highEndcap",
           ]

homedir = expanduser("~")
    
commands = []
for period in periods: 
    for i in range(1, 21):
        for suffix in suffixes:

            extraargs = ""
            
            if suffix == "low":
                extraargs += "--low_pt 15 --high_pt 40 --suffix low "
            elif suffix == "medium":
                extraargs += "--low_pt 40 --high_pt 70 --suffix medium "
            elif suffix == "high":
                extraargs += "--low_pt 70 --high_pt 99999 --suffix high "
            elif suffix == "Barrel":            
                extraargs += "--low_eta 0 --high_eta 1.479 --suffix Barrel "
            elif suffix == "Endcap":             
                extraargs += "--low_eta 1.479 --high_eta 2.2 --suffix Endcap "
            
            #commands.append("HOME=%s; cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py %s_RERECO/*_%s.root %s" % (homedir, period, i, extraargs))
            commands.append("HOME=%s; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_6_2/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py %s_RERECO/*_%s.root %s" % (homedir, period, i, extraargs))
            
                
if options.submit:
    GridEngineTools.runParallel(commands, "grid", confirm=0, condorDir="condor.analysis2", use_sl6=0)

if options.hadd:
    for period in periods: 
        for suffix in suffixes:
            os.system("hadd -f histograms/histograms%s_%s.root histograms/histograms%s_%s_*.root" % (suffix, period, suffix, period))
        
