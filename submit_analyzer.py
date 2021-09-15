#!/bin/env python
import GridEngineTools
import os
import glob
from os.path import expanduser
from optparse import OptionParser
from collections import OrderedDict

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

periods = [
            "Summer16",
            "Run2016B",
            "Run2016C",
            "Run2016D",
            "Run2016E",
            "Run2016F",
            "Run2016G",
            "Run2016H",
            "Fall17",
            "Run2017B",
            "Run2017C",
            "Run2017D",
            "Run2017E",
            "Run2017F",
            "Autumn18",
            "Run2018A",
            "Run2018B",
            "Run2018C",
            "Run2018D",
            ##"RunUL2017C",
            ##"Fall17UL",
          ]
                    
suffixes = OrderedDict()
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
#"verify6-aug21v3-baseline-bdtp10p1":           " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 0.1",
#"verify6-aug21v3-baseline-bdtp10p05":          " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 0.05",
#"verify6-aug21v3-baseline-bdtp10p0":           " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 0.00",
#"verify6-aug21v3-baseline-bdtp1m0p05":         " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 -0.05",
#"verify6-aug21v3-baseline-bdtp1m0p1":          " --bdt aug21v3-baseline --onlyshorts --bdtShortP1 -0.10",
#"verify6-static":                              " --useExotag --onlyshorts",
#suffixes["aug21v4-baseline"] =                    " --onlyshorts --bdt aug21v4-baseline"
#suffixes["aug21v4-noChi2perNdof-noChi2perNdof"] = " --onlyshorts --bdt aug21v4-noChi2perNdof-noChi2perNdof"
#suffixes["aug21v4-noChi2perNdof-noDeltaPt"] =     " --onlyshorts --bdt aug21v4-noChi2perNdof-noDeltaPt"
#suffixes["aug21v4-noChi2perNdof-noDxy"] =         " --onlyshorts --bdt aug21v4-noChi2perNdof-noDxy"
#suffixes["aug21v4-noChi2perNdof-noDz"] =          " --onlyshorts --bdt aug21v4-noChi2perNdof-noDz"
#suffixes["aug21v4-noChi2perNdof-noPixelHits"] =   " --onlyshorts --bdt aug21v4-noChi2perNdof-noPixelHits"
#suffixes["aug21v4-noChi2perNdof-noRelIso"] =      " --onlyshorts --bdt aug21v4-noChi2perNdof-noRelIso"
#suffixes["aug21v4-noDeltaPt-noChi2perNdof"] =     " --onlyshorts --bdt aug21v4-noDeltaPt-noChi2perNdof"
#suffixes["aug21v4-noDeltaPt-noDeltaPt"] =         " --onlyshorts --bdt aug21v4-noDeltaPt-noDeltaPt"
#suffixes["aug21v4-noDeltaPt-noDxy"] =             " --onlyshorts --bdt aug21v4-noDeltaPt-noDxy"
#suffixes["aug21v4-noDeltaPt-noDz"] =              " --onlyshorts --bdt aug21v4-noDeltaPt-noDz"
#suffixes["aug21v4-noDeltaPt-noPixelHits"] =       " --onlyshorts --bdt aug21v4-noDeltaPt-noPixelHits"
#suffixes["aug21v4-noDeltaPt-noRelIso"] =          " --onlyshorts --bdt aug21v4-noDeltaPt-noRelIso"
#suffixes["aug21v4-noDxy-noChi2perNdof"] =         " --onlyshorts --bdt aug21v4-noDxy-noChi2perNdof"
#suffixes["aug21v4-noDxy-noDeltaPt"] =             " --onlyshorts --bdt aug21v4-noDxy-noDeltaPt"
#suffixes["aug21v4-noDxy-noDxy"] =                 " --onlyshorts --bdt aug21v4-noDxy-noDxy"
#suffixes["aug21v4-noDxy-noDz"] =                  " --onlyshorts --bdt aug21v4-noDxy-noDz"
#suffixes["aug21v4-noDxy-noPixelHits"] =           " --onlyshorts --bdt aug21v4-noDxy-noPixelHits"
#suffixes["aug21v4-noDxy-noRelIso"] =              " --onlyshorts --bdt aug21v4-noDxy-noRelIso"
#suffixes["aug21v4-noDz-noChi2perNdof"] =          " --onlyshorts --bdt aug21v4-noDz-noChi2perNdof"
#suffixes["aug21v4-noDz-noDeltaPt"] =              " --onlyshorts --bdt aug21v4-noDz-noDeltaPt"
#suffixes["aug21v4-noDz-noDxy"] =                  " --onlyshorts --bdt aug21v4-noDz-noDxy"
#suffixes["aug21v4-noDz-noDz"] =                   " --onlyshorts --bdt aug21v4-noDz-noDz"
#suffixes["aug21v4-noDz-noPixelHits"] =            " --onlyshorts --bdt aug21v4-noDz-noPixelHits"
#suffixes["aug21v4-noDz-noRelIso"] =               " --onlyshorts --bdt aug21v4-noDz-noRelIso"
#suffixes["aug21v4-noPixelHits-noChi2perNdof"] =   " --onlyshorts --bdt aug21v4-noPixelHits-noChi2perNdof"
#suffixes["aug21v4-noPixelHits-noDeltaPt"] =       " --onlyshorts --bdt aug21v4-noPixelHits-noDeltaPt"
#suffixes["aug21v4-noPixelHits-noDxy"] =           " --onlyshorts --bdt aug21v4-noPixelHits-noDxy"
#suffixes["aug21v4-noPixelHits-noDz"] =            " --onlyshorts --bdt aug21v4-noPixelHits-noDz"
#suffixes["aug21v4-noPixelHits-noPixelHits"] =     " --onlyshorts --bdt aug21v4-noPixelHits-noPixelHits"
#suffixes["aug21v4-noPixelHits-noRelIso"] =        " --onlyshorts --bdt aug21v4-noPixelHits-noRelIso"
#suffixes["aug21v4-noRelIso-noChi2perNdof"] =      " --onlyshorts --bdt aug21v4-noRelIso-noChi2perNdof"
#suffixes["aug21v4-noRelIso-noDeltaPt"] =          " --onlyshorts --bdt aug21v4-noRelIso-noDeltaPt"
#suffixes["aug21v4-noRelIso-noDxy"] =              " --onlyshorts --bdt aug21v4-noRelIso-noDxy"
#suffixes["aug21v4-noRelIso-noDz"] =               " --onlyshorts --bdt aug21v4-noRelIso-noDz"
#suffixes["aug21v4-noRelIso-noPixelHits"] =        " --onlyshorts --bdt aug21v4-noRelIso-noPixelHits"
#suffixes["aug21v4-noRelIso-noRelIso"] =           " --onlyshorts --bdt aug21v4-noRelIso-noRelIso"
#suffixes["aug21v5-withDPt-withChi2"] =                                     " --onlyshorts --bdt aug21v5-withDPt-withChi2"                                 
#suffixes["aug21v5-withDxy-withChi2"] =                                     " --onlyshorts --bdt aug21v5-withDxy-withChi2"                                 
#suffixes["aug21v5-withDxy-withDPt"] =                                      " --onlyshorts --bdt aug21v5-withDxy-withDPt"                                  
#suffixes["aug21v5-withDxy-withDPt-withChi2"] =                             " --onlyshorts --bdt aug21v5-withDxy-withDPt-withChi2"                         
#suffixes["aug21v5-withDxy-withDz"] =                                       " --onlyshorts --bdt aug21v5-withDxy-withDz"                                   
#suffixes["aug21v5-withDxy-withDz-withChi2"] =                              " --onlyshorts --bdt aug21v5-withDxy-withDz-withChi2"                          
#suffixes["aug21v5-withDxy-withDz-withDPt"] =                               " --onlyshorts --bdt aug21v5-withDxy-withDz-withDPt"                           
#suffixes["aug21v5-withDxy-withDz-withDPt-withChi2"] =                      " --onlyshorts --bdt aug21v5-withDxy-withDz-withDPt-withChi2"                  
#suffixes["aug21v5-withDxy-withDz-withPHits"] =                             " --onlyshorts --bdt aug21v5-withDxy-withDz-withPHits"                         
#suffixes["aug21v5-withDxy-withDz-withPHits-withChi2"] =                    " --onlyshorts --bdt aug21v5-withDxy-withDz-withPHits-withChi2"                
#suffixes["aug21v5-withDxy-withDz-withPHits-withDPt"] =                     " --onlyshorts --bdt aug21v5-withDxy-withDz-withPHits-withDPt"                 
#suffixes["aug21v5-withDxy-withDz-withPHits-withDPt-withChi2"] =            " --onlyshorts --bdt aug21v5-withDxy-withDz-withPHits-withDPt-withChi2"        
#suffixes["aug21v5-withDxy-withDz-withRIso"] =                              " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso"                          
#suffixes["aug21v5-withDxy-withDz-withRIso-withChi2"] =                     " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withChi2"                 
#suffixes["aug21v5-withDxy-withDz-withRIso-withDPt"] =                      " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withDPt"                  
#suffixes["aug21v5-withDxy-withDz-withRIso-withDPt-withChi2"] =             " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withDPt-withChi2"         
#suffixes["aug21v5-withDxy-withDz-withRIso-withPHits"] =                    " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withPHits"                
#suffixes["aug21v5-withDxy-withDz-withRIso-withPHits-withChi2"] =           " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withPHits-withChi2"       
#suffixes["aug21v5-withDxy-withDz-withRIso-withPHits-withDPt"] =            " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withPHits-withDPt"        
#suffixes["aug21v5-withDxy-withDz-withRIso-withPHits-withDPt-withChi2"] =   " --onlyshorts --bdt aug21v5-withDxy-withDz-withRIso-withPHits-withDPt-withChi2"
#suffixes["aug21v5-withDxy-withPHits"] =                                    " --onlyshorts --bdt aug21v5-withDxy-withPHits"                                
#suffixes["aug21v5-withDxy-withPHits-withChi2"] =                           " --onlyshorts --bdt aug21v5-withDxy-withPHits-withChi2"                       
#suffixes["aug21v5-withDxy-withPHits-withDPt"] =                            " --onlyshorts --bdt aug21v5-withDxy-withPHits-withDPt"                        
#suffixes["aug21v5-withDxy-withPHits-withDPt-withChi2"] =                   " --onlyshorts --bdt aug21v5-withDxy-withPHits-withDPt-withChi2"               
#suffixes["aug21v5-withDxy-withRIso"] =                                     " --onlyshorts --bdt aug21v5-withDxy-withRIso"                                 
#suffixes["aug21v5-withDxy-withRIso-withChi2"] =                            " --onlyshorts --bdt aug21v5-withDxy-withRIso-withChi2"                        
#suffixes["aug21v5-withDxy-withRIso-withDPt"] =                             " --onlyshorts --bdt aug21v5-withDxy-withRIso-withDPt"                         
#suffixes["aug21v5-withDxy-withRIso-withDPt-withChi2"] =                    " --onlyshorts --bdt aug21v5-withDxy-withRIso-withDPt-withChi2"                
#suffixes["aug21v5-withDxy-withRIso-withPHits"] =                           " --onlyshorts --bdt aug21v5-withDxy-withRIso-withPHits"                       
#suffixes["aug21v5-withDxy-withRIso-withPHits-withChi2"] =                  " --onlyshorts --bdt aug21v5-withDxy-withRIso-withPHits-withChi2"              
#suffixes["aug21v5-withDxy-withRIso-withPHits-withDPt"] =                   " --onlyshorts --bdt aug21v5-withDxy-withRIso-withPHits-withDPt"               
#suffixes["aug21v5-withDxy-withRIso-withPHits-withDPt-withChi2"] =          " --onlyshorts --bdt aug21v5-withDxy-withRIso-withPHits-withDPt-withChi2"      
#suffixes["aug21v5-withDz-withChi2"] =                                      " --onlyshorts --bdt aug21v5-withDz-withChi2"                                  
#suffixes["aug21v5-withDz-withDPt"] =                                       " --onlyshorts --bdt aug21v5-withDz-withDPt"                                   
#suffixes["aug21v5-withDz-withDPt-withChi2"] =                              " --onlyshorts --bdt aug21v5-withDz-withDPt-withChi2"                          
#suffixes["aug21v5-withDz-withPHits"] =                                     " --onlyshorts --bdt aug21v5-withDz-withPHits"                                 
#suffixes["aug21v5-withDz-withPHits-withChi2"] =                            " --onlyshorts --bdt aug21v5-withDz-withPHits-withChi2"                        
#suffixes["aug21v5-withDz-withPHits-withDPt"] =                             " --onlyshorts --bdt aug21v5-withDz-withPHits-withDPt"                         
#suffixes["aug21v5-withDz-withPHits-withDPt-withChi2"] =                    " --onlyshorts --bdt aug21v5-withDz-withPHits-withDPt-withChi2"                
#suffixes["aug21v5-withDz-withRIso"] =                                      " --onlyshorts --bdt aug21v5-withDz-withRIso"                                  
#suffixes["aug21v5-withDz-withRIso-withChi2"] =                             " --onlyshorts --bdt aug21v5-withDz-withRIso-withChi2"                         
#suffixes["aug21v5-withDz-withRIso-withDPt"] =                              " --onlyshorts --bdt aug21v5-withDz-withRIso-withDPt"                          
#suffixes["aug21v5-withDz-withRIso-withDPt-withChi2"] =                     " --onlyshorts --bdt aug21v5-withDz-withRIso-withDPt-withChi2"                 
#suffixes["aug21v5-withDz-withRIso-withPHits"] =                            " --onlyshorts --bdt aug21v5-withDz-withRIso-withPHits"                        
#suffixes["aug21v5-withDz-withRIso-withPHits-withChi2"] =                   " --onlyshorts --bdt aug21v5-withDz-withRIso-withPHits-withChi2"               
#suffixes["aug21v5-withDz-withRIso-withPHits-withDPt"] =                    " --onlyshorts --bdt aug21v5-withDz-withRIso-withPHits-withDPt"                
#suffixes["aug21v5-withDz-withRIso-withPHits-withDPt-withChi2"] =           " --onlyshorts --bdt aug21v5-withDz-withRIso-withPHits-withDPt-withChi2"       
#suffixes["aug21v5-withPHits-withChi2"] =                                   " --onlyshorts --bdt aug21v5-withPHits-withChi2"                               
#suffixes["aug21v5-withPHits-withDPt-withChi2"] =                           " --onlyshorts --bdt aug21v5-withPHits-withDPt-withChi2"                       
#suffixes["aug21v5-withRIso-withChi2"] =                                    " --onlyshorts --bdt aug21v5-withRIso-withChi2"                                
#suffixes["aug21v5-withRIso-withDPt"] =                                     " --onlyshorts --bdt aug21v5-withRIso-withDPt"                                 
#suffixes["aug21v5-withRIso-withDPt-withChi2"] =                            " --onlyshorts --bdt aug21v5-withRIso-withDPt-withChi2"                        
#suffixes["aug21v5-withRIso-withPHits"] =                                   " --onlyshorts --bdt aug21v5-withRIso-withPHits"                               
#suffixes["aug21v5-withRIso-withPHits-withChi2"] =                          " --onlyshorts --bdt aug21v5-withRIso-withPHits-withChi2"                      
#suffixes["aug21v5-withRIso-withPHits-withDPt"] =                           " --onlyshorts --bdt aug21v5-withRIso-withPHits-withDPt"                       
#suffixes["aug21v5-withRIso-withPHits-withDPt-withChi2"] =                  " --onlyshorts --bdt aug21v5-withRIso-withPHits-withDPt-withChi2"              
#suffixes["aug21v4-baseline-pt55"] =                                         " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 55"
#suffixes["aug21v4-baseline-pt100"] =                                        " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 100"
#suffixes["aug21v4-baseline-pt25To55"] =                                    " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 25 --shortsMaxPt 55"
#suffixes["aug21v4-baseline-pt55To100"] =                                   " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 55 --shortsMaxPt 100"
#suffixes["aug21v4-baseline-pt100ToInf"] =                                  " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 100"
#suffixes["aug21v4-baseline-dxy002"] =                                       " --onlyshorts --bdt aug21v4-baseline --shortCut 'track_dxyVtx<0.02'"
#suffixes["aug21v4-baseline-dxy005"] =                                       " --onlyshorts --bdt aug21v4-baseline --shortCut 'track_dxyVtx<0.05'"
#suffixes["aug21v4-baseline-pt55dxy002"] =                                   " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 55 --shortCut 'track_dxyVtx<0.02'"
#suffixes["sep21v1-baseline1"] =                                   " --onlyshorts --bdt sep21v1-baseline "
#suffixes["sep21v1-baseline2"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingMiddleHits==0' "
#suffixes["sep21v1-baseline3"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingMiddleHits==0 and track_dxyVtx<0.02 and track_dzVtx<0.5 and track_trkRelIso<0.05' "
#suffixes["sep21v1-baseline4"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingMiddleHits==0 and track_nMissingInnerHits==0 and track_nMissingOuterHits>=3 and track_pt>55 and abs(track_eta)<2.1 and track_nValidPixelHits>=3 and track_matchedCaloEnergy<10 and track_dxyVtx<0.02 and track_dzVtx<0.5 and track_trkRelIso<0.05' "

#suffixes["sep21v1-baseline5"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingMiddleHits==0' "
#suffixes["sep21v1-baseline6"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingOuterHits>=3' "
#suffixes["sep21v1-baseline7"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>55' "  #$$$
#suffixes["sep21v1-baseline8"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'abs(track_eta)<2.1' "
#suffixes["sep21v1-baseline9"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nValidPixelHits>=3' "
#suffixes["sep21v1-baseline10"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_matchedCaloEnergy<10' "
#suffixes["sep21v1-baseline11"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_dxyVtx<0.02' "
#suffixes["sep21v1-baseline12"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_dzVtx<0.5' "
#suffixes["sep21v1-baseline13"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_trkRelIso<0.05' "
#suffixes["sep21v1-baseline14"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_dxyVtx<0.02 and track_dzVtx<0.5 and track_trkRelIso<0.05' "
#suffixes["sep21v1-baseline15"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_dxyVtx<0.02 and track_dzVtx<0.5 and track_trkRelIso<0.05 and abs(track_eta)<2.1' "
#suffixes["sep21v1-baseline16"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingMiddleHits==0 and track_dxyVtx<0.02 and track_dzVtx<0.5 and track_trkRelIso<0.05' "
#suffixes["sep21v1-baseline17"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_nMissingMiddleHits==0 and track_dxyVtx<0.02 and track_dzVtx<0.5 and track_trkRelIso<0.05 and abs(track_eta)<2.1' "

#suffixes["sep21v2-baseline7a"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortsMinPt 55 "
#suffixes["sep21v2-baseline7aAUG"] =                                " --onlyshorts --bdt aug21v4-baseline --shortsMinPt 55 "
#suffixes["sep21v2-baseline7b"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>55' "
#suffixes["sep21v2-baseline7bAUG"] =                                " --onlyshorts --bdt aug21v4-baseline --shortCut 'track_pt>55' "
#suffixes["sep21v2-baseline7c"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>45' "
#suffixes["sep21v2-baseline7d"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>35' "


#suffixes["sep21v3-baseline5"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>50' "
#suffixes["sep21v3-baseline4"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>55' "
#suffixes["sep21v3-baseline3"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>45' "
#suffixes["sep21v3-baseline2"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>35' "
suffixes["sep21v3-baseline1"] =                                   " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>25' "
#suffixes["sep21v3-baseline1AUG"] =                                   " --onlyshorts --bdt aug21v4-baseline --shortCut 'track_pt>25' "

#suffixes["sep21v3-baseline1-RWh_muonPtCand"] =                     " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>25' --reweightfile hweights.root --reweightvariable h_muonPtCand"
#suffixes["sep21v3-baseline1-RWtrack_pt_short"] =                     " --onlyshorts --bdt sep21v1-baseline --shortCut 'track_pt>25' --reweightfile hweights.root --reweightvariable track_pt_short"


if False:

    # ensuring same BDT bg. efficiencies

    bdt_effs = {'2017-short-tracks-aug21v4-noChi2perNdof-noRelIso': 0.24482465779915613, '2017-short-tracks-aug21v4-noDz-noChi2perNdof': 0.17623134127899276, '2017-short-tracks-aug21v4-noDz-noDz': 0.17233519114088544, '2017-short-tracks-aug21v4-noDeltaPt-noDz': 0.17233519114088544, '2017-short-tracks-aug21v4-noDz-noRelIso': 0.2935819497450945, '2017-short-tracks-aug21v4-noChi2perNdof-noDz': 0.17623134127899276, '2017-short-tracks-aug21v4-noDeltaPt-noPixelHits': 0.1231699395352202, '2017-short-tracks-aug21v4-noChi2perNdof-noDxy': 0.16566607099688158, '2017-short-tracks-aug21v4-noChi2perNdof-noPixelHits': 0.12724080780213648, '2017-short-tracks-aug21v4-noDeltaPt-noChi2perNdof': 0.12442726007297045, '2017-short-tracks-aug21v4-noRelIso-noDz': 0.2935819497450945, '2017-short-tracks-aug21v4-noRelIso-noDeltaPt': 0.23125974177404796, '2017-short-tracks-aug21v4-noRelIso-noChi2perNdof': 0.24482465779915613, '2017-short-tracks-aug21v4-noDz-noPixelHits': 0.23065023858260833, '2017-short-tracks-aug21v4-noDeltaPt-noRelIso': 0.23125974177404796, '2017-short-tracks-aug21v4-noDz-noDeltaPt': 0.17233519114088544, '2017-short-tracks-aug21v4-noRelIso-noDxy': 0.34661664146252913, '2017-short-tracks-aug21v4-noDxy-noDz': 0.22132463513339093, '2017-short-tracks-aug21v4-noDxy-noChi2perNdof': 0.16566607099688158, '2017-short-tracks-aug21v4-noDeltaPt-noDeltaPt': 0.12000191221184353, '2017-short-tracks-aug21v4-noDeltaPt-noDxy': 0.17630066386378285, '2017-short-tracks-aug21v4-noRelIso-noPixelHits': 0.24136547860100158, '2017-short-tracks-aug21v4-noPixelHits-noPixelHits': 0.1231699395352202, '2017-short-tracks-aug21v4-noPixelHits-noDz': 0.23065023858260833, '2017-short-tracks-aug21v4-noPixelHits-noChi2perNdof': 0.12724080780213648, '2017-short-tracks-aug21v4-noDz-noDxy': 0.22132463513339093, '2017-short-tracks-aug21v4-noChi2perNdof-noDeltaPt': 0.12442726007297045, '2017-short-tracks-aug21v4-noPixelHits-noRelIso': 0.24136547860100158, '2017-short-tracks-aug21v4-noPixelHits-noDxy': 0.2196790694276018, '2017-short-tracks-aug21v4-noDxy-noRelIso': 0.34661664146252913, '2017-short-tracks-aug21v4-noDxy-noPixelHits': 0.2196790694276018, '2017-short-tracks-aug21v4-noPixelHits-noDeltaPt': 0.1231699395352202, '2017-short-tracks-aug21v4-noDxy-noDeltaPt': 0.17630066386378285, '2017-short-tracks-aug21v4-noDxy-noDxy': 0.17630066386378285, '2017-short-tracks-aug21v4-noRelIso-noRelIso': 0.23125974177404796, '2017-short-tracks-aug21v4-noChi2perNdof-noChi2perNdof': 0.12442726007297045}
    bdt_effs = {'2017-short-tracks-aug21v5-withDxy-withDz-withRIso': 0.12724080780213648, '2017-short-tracks-aug21v5-withDxy-withRIso-withPHits': 0.17623134127899276, '2017-short-tracks-aug21v5-withRIso-withDPt-withChi2': 0.058189521045053476, '2017-short-tracks-aug21v5-withDxy-withDz-withDPt-withChi2': 0.24136547860100158, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withPHits': 0.12442726007297045, '2017-short-tracks-aug21v5-withDz-withRIso-withDPt': 0.24181338757774834, '2017-short-tracks-aug21v5-withDxy-withRIso-withPHits-withDPt': 0.17623134127899276, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withPHits-withChi2': 0.12000191221184353, '2017-short-tracks-aug21v5-withDxy-withRIso-withPHits-withDPt-withChi2': 0.17233519114088544, '2017-short-tracks-aug21v5-withDxy-withRIso-withDPt-withChi2': 0.23065023858260833, '2017-short-tracks-aug21v5-withDz-withRIso-withPHits': 0.16566607099688158, '2017-short-tracks-aug21v5-withDxy-withRIso-withChi2': 0.23065023858260833, '2017-short-tracks-aug21v5-withDz-withRIso-withPHits-withDPt': 0.16566607099688158, '2017-short-tracks-aug21v5-withPHits-withChi2': 0.6294920191713487, '2017-short-tracks-aug21v5-withRIso-withPHits': 0.25320330862368295, '2017-short-tracks-aug21v5-withDxy-withRIso-withDPt': 0.23828383468967437, '2017-short-tracks-aug21v5-withDxy-withDz-withPHits-withChi2': 0.23125974177404796, '2017-short-tracks-aug21v5-withDxy-withPHits-withDPt': 0.3027392789325466, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withDPt-withChi2': 0.1231699395352202, '2017-short-tracks-aug21v5-withDxy-withPHits': 0.3027392789325466, '2017-short-tracks-aug21v5-withPHits-withDPt-withChi2': 0.6294920191713487, '2017-short-tracks-aug21v5-withDPt-withChi2': 0.6276500885834315, '2017-short-tracks-aug21v5-withDxy-withDz-withChi2': 0.24136547860100158, '2017-short-tracks-aug21v5-withDxy-withPHits-withChi2': 0.2935819497450945, '2017-short-tracks-aug21v5-withRIso-withPHits-withDPt-withChi2': 0.22132463513339093, '2017-short-tracks-aug21v5-withDz-withPHits-withDPt': 0.32455225971652135, '2017-short-tracks-aug21v5-withDz-withDPt-withChi2': 0.575533404423504, '2017-short-tracks-aug21v5-withDz-withRIso-withDPt-withChi2': 0.2196790694276018, '2017-short-tracks-aug21v5-withRIso-withPHits-withChi2': 0.22132463513339093, '2017-short-tracks-aug21v5-withDz-withChi2': 0.575533404423504, '2017-short-tracks-aug21v5-withRIso-withChi2': 0.058189521045053476, '2017-short-tracks-aug21v5-withDxy-withDz': 0.27009890352924343, '2017-short-tracks-aug21v5-withDz-withPHits-withChi2': 0.34661664146252913, '2017-short-tracks-aug21v5-withDxy-withPHits-withDPt-withChi2': 0.2935819497450945, '2017-short-tracks-aug21v5-withDxy-withDz-withPHits': 0.24482465779915613, '2017-short-tracks-aug21v5-withDxy-withDz-withPHits-withDPt-withChi2': 0.23125974177404796, '2017-short-tracks-aug21v5-withRIso-withDPt': 0.09796168333038908, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withChi2': 0.1231699395352202, '2017-short-tracks-aug21v5-withDxy-withChi2': 0.4178318929236899, '2017-short-tracks-aug21v5-withRIso-withPHits-withDPt': 0.25320330862368295, '2017-short-tracks-aug21v5-withDz-withRIso': 0.24181338757774834, '2017-short-tracks-aug21v5-withDz-withDPt': 0.7126109252407474, '2017-short-tracks-aug21v5-withDxy-withDz-withPHits-withDPt': 0.24482465779915613, '2017-short-tracks-aug21v5-withDxy-withDz-withDPt': 0.27009890352924343, '2017-short-tracks-aug21v5-withDz-withPHits': 0.32455225971652135, '2017-short-tracks-aug21v5-withDxy-withDPt': 0.4807103536019143, '2017-short-tracks-aug21v5-withDz-withRIso-withChi2': 0.2196790694276018, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withPHits-withDPt': 0.12442726007297045, '2017-short-tracks-aug21v5-withDz-withPHits-withDPt-withChi2': 0.34661664146252913, '2017-short-tracks-aug21v5-withDxy-withRIso': 0.23828383468967437, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withPHits-withDPt-withChi2': 0.12000191221184353, '2017-short-tracks-aug21v5-withDz-withRIso-withPHits-withChi2': 0.17630066386378285, '2017-short-tracks-aug21v5-withDz-withRIso-withPHits-withDPt-withChi2': 0.17630066386378285, '2017-short-tracks-aug21v5-withDxy-withRIso-withPHits-withChi2': 0.17233519114088544, '2017-short-tracks-aug21v5-withDxy-withDPt-withChi2': 0.4178318929236899, '2017-short-tracks-aug21v5-withDxy-withDz-withRIso-withDPt': 0.12724080780213648}
    
    for label in suffixes:
        replaced = False
        for i_eff in bdt_effs:
            if "2017-short-tracks-%s" % label == i_eff:
                suffixes[label] += " --bdtShortP1 %s" % bdt_effs[i_eff]
                print suffixes[label]
                replaced = True
        
        if not replaced:
            print "Not there:", label

        
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--submit", dest = "submit", action="store_true")
    parser.add_option("--hadd", dest = "hadd", action="store_true")
    parser.add_option("--plot", dest = "plot", action="store_true")
    (options, args) = parser.parse_args()
      
    overwrite = True
    lowstat = False
    runmode = "grid"
    files_per_job = 10
    njobs_divide_by = 1

    histofolder = "histograms"
    
    homedir = expanduser("~")
    
    commands = []
    for period in periods: 
        for suffix in suffixes:

            if "onlyshorts" in suffixes[suffix]:
                min_layers = 3
                max_layers = 6
            else:
                min_layers = 3
                max_layers = 14

            for i in range(min_layers, max_layers + 1):
                allfiles = glob.glob("%s_RERECO/*_%s.root" % (period, i))
                
                if lowstat:
                    allfiles = [allfiles[0]]
                
                for i_iFiles, iFiles in enumerate(chunks( allfiles , files_per_job )):
                                
                    if suffix == "":
                        suffixterm = ""
                    else:
                        suffixterm = " --suffix %s " % suffix
                    
                    extraargs = suffixes[suffix] + " %s --outputfolder %s " % (suffixterm, histofolder)
                    #cmd = "HOME=%s; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_6_2/src/; eval `scramv1 runtime -sh`; cd -; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py --chunkid %s %s %s " % (homedir, i_iFiles, " ".join(iFiles), extraargs)
                    cmd = "HOME=%s; cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening; python analyzer.py --chunkid %s %s %s " % (homedir, i_iFiles, " ".join(iFiles), extraargs)

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
                                            #"Run2016D",
                                            "Run2016E",
                                            "Run2016F",
                                            "Run2016G",
                                            #"Run2016H",
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
                
        if njobs_divide_by>1:        
            commands2 = []
            for command in chunks(commands, njobs_divide_by):
                commands2.append("; ".join(command))
                print commands2[-1]
            commands = commands2
        
        #print commands
        print commands[0]
        print len(commands)
        raw_input("OK?")
        
        GridEngineTools.runParallel(commands, runmode, confirm=0, condorDir="condor.analysis3", use_sl6=0)
    
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
                #os.system("./plot-reweighting-scalefactors-and-efficiencies.py --histofolder %s --suffix %s &" % (histofolder, suffix))
                os.system("./plot-reweighting-scalefactors-and-efficiencies-combined.py --suffix %s &" % suffix)
                os.system("./plot-trackvariables-years.py --suffix %s &" % suffix)
                os.system("./plot-trackvariables-years.py --suffix %s --tagged tagged &" % suffix)
                

