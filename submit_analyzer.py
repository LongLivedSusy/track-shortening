#!/bin/env python
import GridEngineTools
import os
import glob
import plot

def submit():
    
    commands = []
    
    for period in ["Summer16", "Run2016"]: 
        for i in range(1, 21):
            commands.append("cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py %s_ISOTRACKS/*_%s.root" % (period, i))
            commands.append("cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py %s_ISOTRACKS/*_%s.root --low_pt 15 --high_pt 50 --suffix low" % (period, i))
            commands.append("cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py %s_ISOTRACKS/*_%s.root --low_pt 50 --high_pt 99999 --suffix high" % (period, i))

    GridEngineTools.runParallel(commands, "grid", confirm=False, condorDir="condor.analysis")
    for period in ["Summer16", "Run2016"]: 
        os.system("hadd -f histograms_%s.root histograms_%s_?.root histograms_%s_??.root && rm histograms_%s_?.root && rm histograms_%s_??.root" % (period, period, period, period, period))
        os.system("hadd -f histogramslow_%s.root histogramslow_%s_?.root histogramslow_%s_??.root && rm histogramslow_%s_?.root && rm histogramslow_%s_??.root" % (period, period, period, period, period))
        os.system("hadd -f histogramshigh_%s.root histogramshigh_%s_?.root histogramshigh_%s_??.root && rm histogramshigh_%s_?.root && rm histogramshigh_%s_??.root" % (period, period, period, period, period))
        
submit()

plot.doplots()