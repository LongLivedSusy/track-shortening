#!/bin/env python
import GridEngineTools
import os
import glob
import plot
from os.path import expanduser

periods = ["Summer16", "Fall17"]    #"Run2016H", "Run2016B", "Run2017B", "Run2017F", 
#periods = ["SummerOld16"]   #"Run2016PromptH"

homedir = expanduser("~")

def submit():
    
    commands = []
    for period in periods: 
        for i in range(1, 21):
            commands.append("HOME=%s; cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py %s_RERECO/*_%s.root" % (homedir, period, i))
            #commands.append("HOME=%s; cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py %s_RERECO/*_%s.root --low_pt 15 --high_pt 60 --suffix low" % (homedir, period, i))
            #commands.append("HOME=%s; cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py %s_RERECO/*_%s.root --low_pt 60 --high_pt 99999 --suffix high" % (homedir, period, i))

    
    #GridEngineTools.runParallel(commands, "multi", confirm=0, condorDir="condor.analysis", use_sl6=0)
    
    for period in periods: 
        os.system("hadd -f histograms_%s.root histograms_%s_*.root" % (period, period))
        os.system("hadd -f histogramslow_%s.root histogramslow_%s_*.root" % (period, period))
        os.system("hadd -f histogramshigh_%s.root histogramshigh_%s_*.root" % (period, period))
        
submit()

plot.doplots(periods = periods)