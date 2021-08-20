#!/bin/env python
import GridEngineTools
import os
import glob
from os.path import expanduser
from optparse import OptionParser

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

periods = [
            #"Summer16",
            #"Run2016B",
            #"Run2016C",
            #"Run2016D",
            #"Run2016E",
            #"Run2016F",
            #"Run2016G",
            #"Run2016H",
            "Fall17",
            "Run2017B",
            "Run2017C",
            "Run2017D",
            "Run2017E",
            "Run2017F",
            #"Autumn18",
            #"Run2018A",
            #"Run2018B",
            #"Run2018C",
            #"Run2018D",
            ##"RunUL2017C",
            ##"Fall17UL",
          ]
          
          
suffixes = {
            #"":                 " ",
            #"onlyP0DiffXsec":   " --onlyp0bdt --bdt may21 ",
            #"Verifymay21":       " --bdt may21",
            #"Verifymay21equSgXsec3":       " --bdt may21-equSgXsec3",
            #"ShortsBaselineV2":    " --bdt jun21 ",
            #"ShortsCombinedV2":    " --bdt jun21 --combinedShortBDTs",
            #"ShortsRedefinedV2":   " --bdt jun21 --redefineCategories",
            #"ShortsBaselineV3":    " --bdt jun21 ",
            #"ShortsCombinedV3":    " --bdt jun21 --combinedShortBDTs",
            #"ShortsRedefinedV4":   " --bdt jun21 --redefineCategories",
            #"ShortsBaselineV3":    " --bdt jun21 ",
            #"ShortsBaselineV4":    " --bdt nov20-noEdep ",
            #"ShortsBaselineV4a2":    " --bdt nov20-noEdep ",
            #"ShortsBaselineV4spt15":    " --bdt nov20-noEdep --shortsMinPt 15",
            #"ShortsBaselineV4spt30":    " --bdt nov20-noEdep --shortsMinPt 30",
            #"ShortsBaselineV4spt40":    " --bdt nov20-noEdep --shortsMinPt 40",
            #"ShortsBaselineV5spt15":    " --bdt nov20-noEdep --shortsMinPt 15 --high_pt 25",
            #"ShortsBaselineV5spt25":    " --bdt nov20-noEdep --shortsMinPt 25 --high_pt 35",
            #"ShortsBaselineV5spt35":    " --bdt nov20-noEdep --shortsMinPt 35 --high_pt 50",
            #"ShortsBaselineV5":             " --bdt jun21",
            #"ShortsBaselineV5noRelIso":     " --bdt jul21-noRelIso",
            #"ShortsBaselineV5noDeltaPt":    " --bdt jul21-noDeltaPt",
            #"ShortsBaselineV5noPixelHits":  " --bdt jul21-noRelIso",
            #"ShortsBaselineV5noDeltaPt":    " --bdt jul21-noPixelHits",
            #"ShortsBaselineV5TighterDxy":   " --bdt jul21-TighterDxy",
            #"ShortsBaselineV5noPixelHitsnoDeltaPt":     " --bdt jul21-noPixelHits-noDeltaPt",
            #"ShortsBaselineV6":                         " --bdt jun21",
            #"ShortsBaselineV6noRelIso":                 " --bdt jul21-noRelIso",
            #"ShortsBaselineV6noDeltaPt":                " --bdt jul21-noDeltaPt",
            #"ShortsBaselineV6noPixelHits":              " --bdt jul21-noPixelHits",
            #"ShortsBaselineV6noPixelHitsnoDeltaPt":     " --bdt jul21-noPixelHits-noDeltaPt",
            #"ShortsBaselineV7":                         " --bdt jun21",
            #"ShortsBaselineV7baseline":                 " --bdt jul21-baseline",
            #"ShortsBaselineV7noRelIso":                 " --bdt jul21-noRelIso",
            #"ShortsBaselineV7noDeltaPt":                " --bdt jul21-noDeltaPt",
            #"ShortsBaselineV7noPixelHits":              " --bdt jul21-noPixelHits",
            #"verifyV2Aug21baseline":                    " --bdt aug21-baseline",
            #"verifyV2Aug21noPixel":                     " --bdt aug21-noPixelHits",
            #"verifyV2Aug21noDeltaPt":                   " --bdt aug21-noDeltaPt",
            #"verify-aug21v3-baseline":                  " --bdt aug21v3-baseline",
            #"verify-aug21v3-noPixelHits":               " --bdt aug21v3-noPixelHits",
            #"verify-aug21v3-noDeltaPt":                 " --bdt aug21v3-noDeltaPt",
            #"verify-aug21v3-noPixelHits-noDeltaPt":     " --bdt aug21v3-noPixelHits-noDeltaPt",
            #"verify-aug21v3-baseline-ptL":               " --bdt aug21v3-baseline --shortsMinPt 25 --shortsMaxPt 33",
            #"verify-aug21v3-baseline-ptM":               " --bdt aug21v3-baseline --shortsMinPt 33 --shortsMaxPt 40",
            #"verify-aug21v3-baseline-ptH":               " --bdt aug21v3-baseline --shortsMinPt 40",
            "verify-aug21v3-baseline-bdtp10p1":           " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 0.1",
            "verify-aug21v3-baseline-bdtp10p05":          " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 0.05",
            "verify-aug21v3-baseline-bdtp10p0":           " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 0.00",
            "verify-aug21v3-baseline-bdtp1m0p05":         " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 -0.05",
            "verify-aug21v3-baseline-bdtp1m0p1":          " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 -0.10",
            #"ShortsBaselineV7noPixelHitsnoDeltaPt":     " --bdt jul21-noPixelHits-noDeltaPt",
            #"Aug21V1baseline":                          " --bdt aug21-baseline               ",
            #"Aug21V1noDeltaPt":                         " --bdt aug21-noDeltaPt              ",
            #"Aug21V1noPixelHits":                       " --bdt aug21-noPixelHits            ",
            #"Aug21V1noPixelHitsnoDeltaPt":              " --bdt aug21-noPixelHits-noDeltaPt  ",
            #"Aug21V1noRelIso":                          " --bdt aug21-noRelIso               ",
            #"Aug21V1onlyT1qqqq":                        " --bdt aug21-onlyT1qqqq             ",
            #"Aug21V1onlyT2bt":                          " --bdt aug21-onlyT2bt               ",
            #"Aug21V1useLayers":                         " --bdt aug21-useLayers              ",
            #"BaselineV4A":     " --bdt jun21-noJetVeto ",
            #"BaselineV4B":     " --bdt jun21-noPixelHits ",
            #"BaselineV4C":     " --bdt jun21-noVetoes ",
            #"BaselineV4D":     " --bdt jun21-oldWeights ",
            #"BaselineV4E":     " --bdt jun21-oldWeights-noJetVeto ",
            #"BaselineV4F":     " --bdt jun21-oldWeights-noVetoes ",
            #"DiffXsecMay":      " --bdt may21 ",
            #"DiffXsecNov":      " --bdt nov20-noEdep ",
            #"EquXsecMay":       " --bdt may21-equSgXsec3 ",
            #"EquXsecMayA":      " --bdt may21-equSgXsec3 --bdtShortP1 0.05",
            #"EquXsecMayB":      " --bdt may21-equSgXsec3 --bdtShortP1 0.00",
            #"EquXsecMayC":      " --bdt may21-equSgXsec3 --bdtShortP1 -0.05",
            #"NewShort":         " --bdt may21v2 ",
            #"NewShortPresel":   " --bdt may21v2 ",
            #"MCReweighting":    " --bdt may21v2 --reweightfile hweights.root",
            #"BdtJun21":          " --bdt jun21",
            #"BdtCutP1A":           " --bdt may21v2 --bdtShortP1 0.05",
            #"BdtCutP1B":           " --bdt may21v2 --bdtShortP1 0.00",
            #"BdtCutP1C":           " --bdt may21v2 --bdtShortP1 -0.1",
            #"BdtCutP1D":           " --bdt may21v2 --bdtShortP1 -0.2",
            #"BdtCutP1E":           " --bdt may21v2 --bdtShortP1 -0.3",
            #"MCReweightingE":   " --bdt may21v2 --reweightfile hweights_a.root",
            ##"MCReweightingF":  " --bdt may21v2 --reweightfile hweights_b.root",
            #"NewShortA":        " --bdt may21v2 ",
            #"NewShortB":        " --bdt may21v2 --bdtShortP1 0.05 ",
            #"NewShortC":        " --bdt may21v2 --bdtShortP1 0.00 ",
            #"NewShortC":        " --bdt may21v2 ",
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
         
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--submit", dest = "submit", action="store_true")
    parser.add_option("--hadd", dest = "hadd", action="store_true")
    parser.add_option("--plot", dest = "plot", action="store_true")
    (options, args) = parser.parse_args()
      
    overwrite = False
      
    histofolder = "histograms"
    
    homedir = expanduser("~")
    
    commands = []
    for period in periods: 
        for i in range(1, 21):
            for suffix in suffixes:
                allfiles = glob.glob("%s_RERECO/*_%s.root" % (period, i))
                
                #FIXME
                allfiles = [allfiles[0]]
                
                for i_iFiles, iFiles in enumerate(chunks( allfiles , 20 )):
                                
                    if suffix == "":
                        suffixterm = ""
                    else:
                        suffixterm = " --suffix %s " % suffix
                    
                    extraargs = suffixes[suffix] + " %s --outputfolder %s " % (suffixterm, histofolder)
                    cmd = "HOME=%s; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_6_2/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py --chunkid %s %s %s " % (homedir, i_iFiles, " ".join(iFiles), extraargs)
                    
                    outfilename = "%s/histograms%s_%s_%s_%s.root" % (histofolder, suffix, period, i_iFiles, i)
                    if os.path.exists(outfilename) and not overwrite:
                        continue
                    
                    commands.append(cmd)
                    
                    # add reweighting:
                    if "Run201" not in period and "reweightfile" in suffixes[suffix]:
                        if "Summer16" in period:
                            for rwperiod in [
                                            "Run2016B",
                                            "Run2016C",
                                            "Run2016D",
                                            "Run2016E",
                                            "Run2016F",
                                            "Run2016G",
                                            "Run2016H",
                                            ]:
                                commands.append(cmd + " --reweightmc " + rwperiod)
                        if "Fall17" in period:
                            for rwperiod in [
                                            "Run2017B",
                                            "Run2017C",
                                            "Run2017D",
                                            "Run2017E",
                                            "Run2017F",
                                            ]:
                                commands.append(cmd + " --reweightmc " + rwperiod)
                        if "Autumn18" in period:
                            for rwperiod in [
                                            "Run2018A",
                                            "Run2018B",
                                            "Run2018C",
                                            "Run2018D",
                                            ]:
                                commands.append(cmd + " --reweightmc " + rwperiod)
                
    if options.submit:
        
        #print len(commands), commands[0]
        #print len(commands), commands[-1]
        
        print commands
        print len(commands)
        raw_input("OK?")
        
        GridEngineTools.runParallel(commands, "multi", confirm=0, condorDir="condor.analysis7", use_sl6=0)
        #GridEngineTools.runParallel(commands, "grid", confirm=0, condorDir="condor.analysis4a2", use_sl6=0)
        #GridEngineTools.runParallel(commands, "multi", confirm=0, condorDir="condor.analysis5", use_sl6=0)
    
    if options.hadd:
        for period in periods: 
            for suffix in suffixes:
                os.system("hadd -f %s/histograms%s_%s.root histograms/histograms%s_%s_*.root &" % (histofolder, suffix, period, suffix, period))
                
                if "Run201" not in period and "reweightfile" in suffixes[suffix]:
                    if "Summer16" in period:
                        for rwperiod in [
                                        "Run2016B",
                                        "Run2016C",
                                        "Run2016D",
                                        "Run2016E",
                                        "Run2016F",
                                        "Run2016G",
                                        "Run2016H",
                                        ]:
                            os.system("hadd -f %s/histograms%s_%s.root histograms/histograms%s_%s_*.root &" % (histofolder, suffix, period + "rw" + rwperiod, suffix, period + "rw" + rwperiod))
                    if "Fall17" in period:
                        for rwperiod in [
                                        "Run2017B",
                                        "Run2017C",
                                        "Run2017D",
                                        "Run2017E",
                                        "Run2017F",
                                        ]:
                            os.system("hadd -f %s/histograms%s_%s.root histograms/histograms%s_%s_*.root &" % (histofolder, suffix, period + "rw" + rwperiod, suffix, period + "rw" + rwperiod))
                    if "Autumn18" in period:
                        for rwperiod in [
                                        "Run2018A",
                                        "Run2018B",
                                        "Run2018C",
                                        "Run2018D",
                                        ]:
                            os.system("hadd -f %s/histograms%s_%s.root histograms/histograms%s_%s_*.root &" % (histofolder, suffix, period + "rw" + rwperiod, suffix, period + "rw" + rwperiod))
                    
    
    if options.plot:
        for suffix in suffixes:
            if suffix == "":
                os.system("./plot-reweighting-scalefactors-and-efficiencies.py --histofolder %s &" % (histofolder))
            else:
                os.system("./plot-reweighting-scalefactors-and-efficiencies.py --histofolder %s --suffix %s &" % (histofolder, suffix))
                
    
            
    
