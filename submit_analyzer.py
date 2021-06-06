#!/bin/env python
import GridEngineTools
import os
import glob
#import plot
from os.path import expanduser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--submit", dest = "submit", action="store_true")
parser.add_option("--hadd", dest = "hadd", action="store_true")
parser.add_option("--plot", dest = "plot", action="store_true")
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
            #"RunUL2017C",
            #"Fall17UL",
          ]
          
suffixes = {
            #"":                 " ",
            #"onlyP1DiffXsec":   " --onlyp1bdt --bdt may21 ",
            #"DiffXsecMay":      " --bdt may21 ",
            #"DiffXsecNov":      " --bdt nov20-noEdep ",
            #"EquXsecMay":       " --bdt may21-equSgXsec3 ",
            #"EquXsecMayA":      " --bdt may21-equSgXsec3 --bdtShortP1 0.05",
            #"EquXsecMayB":      " --bdt may21-equSgXsec3 --bdtShortP1 0.00",
            #"EquXsecMayC":      " --bdt may21-equSgXsec3 --bdtShortP1 -0.05",
            "NewShort":          " --bdt may21v2 ",
            #"NewShortPS":        " --bdt may21v2 ",
            #"NewShortA":         " --bdt may21v2 ",
            #"NewShortB":         " --bdt may21v2 --bdtShortP1 0.05 ",
            #"NewShortC":         " --bdt may21v2 --bdtShortP1 0.00 ",
            #"NewShortC":          " --bdt may21v2 ",
            #"low":              "--low_pt 30 --high_pt 35 --override_category_pt ",
            #"medium":           "--low_pt 35 --high_pt 40 --override_category_pt ",
            #"high":             "--low_pt 40 --high_pt 45 --override_category_pt ",
            #"high2":            "--low_pt 45 --high_pt 50 --override_category_pt ",
            #"high3":            "--low_pt 55 --high_pt 60 --override_category_pt ",
            #"high4":            "--low_pt 50 --high_pt 55 --override_category_pt ",
            #"new5":             "--low_pt 0 --high_pt 50 --override_category_pt ",
            #"new6":             "--low_pt 0 --high_pt 50 ",
            #"new7":             "--low_pt 50 --high_pt 99999 --override_category_pt ",
            #"noniso4":          "--iso 4 ",
            #"noniso5":          "--iso 5 ",
            #"Barrel":           "--low_eta 0 --high_eta 1.479 ",
            #"Endcap":           "--low_eta 1.479 --high_eta 2.2 ",
           }
           
histofolder = "histograms"

homedir = expanduser("~")

commands = []
for period in periods: 
    for i in range(1, 21):
        for suffix in suffixes:
            if suffix == "":
                suffixterm = ""
            else:
                suffixterm = " --suffix %s " % suffix

            extraargs = suffixes[suffix] + " %s --outputfolder %s " % (suffixterm, histofolder)
            commands.append("HOME=%s; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_6_2/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py %s_RERECO/*_%s.root %s; " % (homedir, period, i, extraargs))
        
if options.submit:
    GridEngineTools.runParallel(commands, "grid", confirm=0, condorDir="condor.analysis4", use_sl6=0)

if options.hadd:
    for period in periods: 
        for suffix in suffixes:
            os.system("hadd -f %s/histograms%s_%s.root histograms/histograms%s_%s_*.root &" % (histofolder, suffix, period, suffix, period))

if options.plot:
    #for period in periods: 
    for suffix in suffixes:
        if suffix == "":
            os.system("./plot.py --histofolder %s &" % (histofolder))
        else:
            os.system("./plot.py --histofolder %s --suffix %s &" % (histofolder, suffix))
            

        
