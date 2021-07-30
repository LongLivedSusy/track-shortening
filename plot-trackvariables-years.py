#!/bin/env python
import os
import glob
import shared_utils
import plotting
import math
from ROOT import *
from optparse import OptionParser

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()


def fill_num_denom(i_finaleff, i_year, i_category, i_value):
    if not i_finaleff[i_category][i_year]:
        i_finaleff[i_category][i_year] = i_value
    else:
        i_finaleff[i_category][i_year].Add(i_value)


if __name__ == "__main__":

    #./plot-trackvariables-years.py --suffix ShortsBaselineV5 &        
    #./plot-trackvariables-years.py --suffix ShortsBaselineV5noRelIso & 
    #./plot-trackvariables-years.py --suffix ShortsBaselineV5noDeltaPt &
    #./plot-trackvariables-years.py --suffix ShortsBaselineV5noPixelHits &
    #./plot-trackvariables-years.py --suffix ShortsBaselineV5noDeltaPt &
    #./plot-trackvariables-years.py --suffix ShortsBaselineV5TighterDxy &

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "ShortsBaselineV5")
    parser.add_option("--mcsuffix", dest = "mcsuffix", default = "")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")
    parser.add_option("--reweighted", dest = "mc_reweighted", action = "store_true")

    (options, args) = parser.parse_args()
    
    histofolder = options.histofolder
    suffix = options.suffix
    
    plotfolder = "plots%s_new2" % options.suffix
    if options.mcsuffix != "":
        plotfolder = plotfolder.replace("_new2", "_%s_new2" % options.mcsuffix)
    
    os.system("mkdir -p %s" % plotfolder)

    periods = [
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
              ]
              
    if options.mc_reweighted:
        periods += [
                "Summer16rwRun2016B",
                "Summer16rwRun2016C",
                "Summer16rwRun2016D",
                "Summer16rwRun2016E",
                "Summer16rwRun2016F",
                "Summer16rwRun2016G",
                "Summer16rwRun2016H",
                "Fall17rwRun2017B",
                "Fall17rwRun2017C",
                "Fall17rwRun2017D",
                "Fall17rwRun2017E",
                "Fall17rwRun2017F",
                "Autumn18rwRun2018A",
                "Autumn18rwRun2018B",
                "Autumn18rwRun2018C",
                "Autumn18rwRun2018D",
              ]
    else:
        periods += [
                "Summer16",
                "Fall17",
                "Autumn18",
                   ]
    
    variables = {
                  #"track_trkRelIso": [[0, 0.005, 0.01, 0.015, 0.02, 0.2], 0, 0.2, "relative track isolation"],
                  #"track_dxyVtx": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "d_{xy} (cm)"],
                  #"track_dzVtx": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "d_{z} (cm)"],
                  #"track_nMissingOuterHits": [20, 0, 20, "missing outer hits"],
                  #"track_nValidPixelHits": [10, 0, 10, "pixel hits"],
                  #"track_nValidTrackerHits": [20, 0, 20, "tracker hits"],
                  #"track_chi2perNdof": [20, 0, 5.0, "track #chi^{2}/ndof"],
                  #"track_ptErrOverPt2": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "#Delta p_{T} / p_{T}^{2} (GeV^{-1})"],                  
                  #"track_matchedCaloEnergy": [20, 0, 50, "E_{dep} (GeV)"],
                  "track_dxyVtx"                       : [20, 0, 0.1 , "track_dxyVtx"],
                  "track_dzVtx"                        : [20, 0, 0.1 , "track_dzVtx"],
                  "track_trkRelIso"                    : [20, 0, 0.2 , "track_trkRelIso"],
                  "track_nValidPixelHits"              : [10, 0, 10  , "track_nValidPixelHits"],
                  "track_nValidTrackerHits"            : [20, 0, 20  , "track_nValidTrackerHits"],
                  "track_trackerLayersWithMeasurement" : [20, 0, 20  , "track_trackerLayersWithMeasurement"],
                  "track_ptErrOverPt2"                 : [20, 0, 0.01, "track_ptErrOverPt2"],
                  "track_chi2perNdof"                  : [20, 0, 2   , "track_chi2perNdof"],
                  "track_mva"                          : [20, -1, 1  , "track_mva"],
                  "track_pt"                           : [20, 0, 200 , "track_pt"],
                  "track_trackQualityHighPurity"       : [2, 0, 2    , "track_trackQualityHighPurity"],
                  "track_nMissingInnerHits"            : [5, 0, 5    , "track_nMissingInnerHits"],
                  "track_passPFCandVeto"               : [2, 0, 2    , "track_passPFCandVeto"],
                  "track_nMissingOuterHits"            : [10, 0, 10  , "track_nMissingOuterHits"],
                  "track_matchedCaloEnergy"            : [25, 0, 50  , "track_matchedCaloEnergy"],
                  "track_p"                            : [20, 0, 200 , "track_p"],
                  "cutflow"                              : [25, 0, 25, ""],
                  #"h_tracks_algo"                        : [50, 0, 50, "h_tracks_algo"],
                 }
    
    # get all histos:
    hists = {}
    for period in periods:
        hists[period] = {}
        for category in [
                        #"",
                        "_short",
                        "_long",
                        ]:
                
            for label in variables:
                
                print period, category, label
                fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, period), "open")                       
                hists[period][label + category] = fin.Get(label + category)
                hists[period][label + category].SetDirectory(0)
                hists[period][label + category].SetLineWidth(2)
                shared_utils.histoStyler(hists[period][label + category])
                fin.Close()

    # add years lumiweighted:

    # Lumi-weighting:
    official_lumis = {
        "Run2016B": 5.8,
        "Run2016C": 2.6,
        "Run2016D": 4.2,
        "Run2016E": 4.0,
        "Run2016F": 3.1,
        "Run2016G": 7.5,
        "Run2016H": 8.6,
        "Run2017B": 4.8,
        "Run2017C": 9.7,
        "Run2017D": 4.3 ,
        "Run2017E": 9.3,
        "Run2017F": 13.5,
        "Run2018A": 14,
        "Run2018B": 7.1 ,
        "Run2018C": 6.94 ,
        "Run2018D": 31.93,
    }
    
    for category in [
                    "_short",
                    "_long",
                    ]:
        for year in ["2016", "2017", "2018"]:
            if not "Run%s" % year in hists:
                hists["Run%s" % year] = {}
            for label in variables:
                hists["Run%s" % year][label + category] = 0
                for i_period in periods:
                    if year in i_period and "rw" not in i_period:
                        scaledhisto = hists[i_period][label + category].Clone()
                        if "Run201" in i_period:
                            scaledhisto.Scale(official_lumis[i_period])
                        if not hists["Run%s" % year][label + category]:
                            hists["Run%s" % year][label + category] = scaledhisto.Clone()
                        else:
                            hists["Run%s" % year][label + category].Add(scaledhisto)
                        
    for category in [
                    #"",
                    "_short",
                    "_long",
                    ]:
        
        for label in variables:
        
            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.6, y1=0.55, x2=0.85, y2=0.85)
        
            pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0.0)
            pad1.SetLeftMargin(0.12)
            pad1.SetGridx()
            pad1.Draw()
            pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
            pad2.SetTopMargin(0.0)
            pad2.SetBottomMargin(0.4)
            pad2.SetLeftMargin(0.12)
            pad2.SetGridx()
            pad2.SetGridy()
            pad2.Draw()
            pad1.cd()
            
            for i_year, year in enumerate(["2016", "2017", "2018"]):
                
                if i_year == 0:
                    drawoption = "hist e same"
                    drawoption_data = "p e same"
                else:
                    drawoption = "hist e same"
                    drawoption_data = "p e same"
                            
                if category == "":
                    legend.SetHeader("short + long tracks")
                else:    
                    legend.SetHeader("%s tracks" % (category.replace("_", "")))
                legend.SetTextSize(0.045)
                
                if year == "2016":
                    mcperiod = "Summer16"
                    color = kBlue
                elif year == "2017":
                    mcperiod = "Fall17"
                    color = kRed
                elif year == "2018":
                    mcperiod = "Autumn18"
                    color = kGreen
                
                period = "Run%s" % year
                print year, period, mcperiod
                
                pad1.cd()
                pad1.SetLogy()
                                
                # normalize
                
                #colors = [97, 94, 91, 86, 81, 70, 65, 61, 51]
                #color = colors.pop(0)
                
                legend.AddEntry(hists[period][label + category], period)

                pad1.cd()
                
                # normalize:
                if hists[period][label + category].Integral()>0:
                    hists[period][label + category].Scale(1.0/hists[period][label + category].Integral())
                hists[period][label + category].SetMarkerStyle(20)
                #hists[period][label + category].SetMarkerSize(3)
                hists[period][label + category].Draw(drawoption_data)
                if "cutflow" in label:
                    hists[period][label + category].GetYaxis().SetRangeUser(1e-2,1e0)
                else:
                    hists[period][label + category].GetYaxis().SetRangeUser(1e-5,1e1)
                hists[period][label + category].SetLineColor(color)
                hists[period][label + category].SetMarkerColor(color)
                hists[period][label + category].SetLineStyle(1)
                #hists[period][label + category].SetTitle(";%s;Normalized Data / normalized MC" % label)
                hists[period][label + category].SetTitle(";;Normalized events")
                #hists[period][label + category].GetYaxis().SetRangeUser(0,2.5)


                if hists[mcperiod][label + category].Integral()>0:
                    hists[mcperiod][label + category].Scale(1.0/hists[mcperiod][label + category].Integral())
                
                hists[mcperiod][label + category].Draw(drawoption)
                hists[mcperiod][label + category].SetLineColor(color)
                hists[mcperiod][label + category].SetLineStyle(2)
                hists[mcperiod][label + category].SetLineWidth(3)
                hists[mcperiod][label + category].SetTitle(";;Events")
                legend.AddEntry(hists[mcperiod][label + category], mcperiod)
                
                if "cutflow" in label:
                    hists[period][label + category].GetXaxis().SetTitleSize(0.04)
                    hists[period][label + category].GetXaxis().SetLabelSize(0.04)   
                
                    #canvas.SetLogy(False)
                
                    binlabels = {
                                  0: "#mu-matched tracks",
                                  1: "p_{T}>25 (40) GeV",
                                  2: "high purity",
                                  3: "|eta|<2.0",
                                  4: "#Delta p_{T}/p_{T}^{2}<10/GeV",
                                  5: "dz<0.1 cm",
                                  6: "relIso<0.2",
                                  7: "tracker layer #geq2",
                                  8: "tracker hits #geq2",
                                  9: "no miss. inner hits",
                                  10: "pixel hits #geq2",
                                  11: "PF cand. veto",
                                  12: "missing outer hits",
                                  13: "BDT> 0.1 (0.1)",
                                  14: "E_{dep}<15 or E_{dep}/p<0.15",
                    }
                
                    if "Run2016" not in period and "Summer16" not in period:
                        binlabels[13] = "BDT> 0.12 (0.15)"

                    for i in binlabels:
                        hists[period][label + category].GetXaxis().SetBinLabel(i + 1, binlabels[i]);
                        hists[mcperiod][label + category].GetXaxis().SetBinLabel(i + 1, binlabels[i]);
            
                    hists[period][label + category].GetXaxis().SetRangeUser(0,15)
                    hists[mcperiod][label + category].GetXaxis().SetRangeUser(0,15)
                    #hists[period][label + category].GetYaxis().SetRangeUser(0,1)
                    hists[period][label + category].SetTitle(";;fraction of remaining shortened tracks")
                
                pad2.cd()
                #num = hists[period][label + category].Clone()
                #num.Scale(1.0/num.Integral())
                #denom = hists[mcperiod][label + category].Clone()
                #denom.Scale(1.0/denom.Integral())
                #hists[period][label + category + "_ratio"] = num.Clone()
                #hists[period][label + category + "_ratio"].Divide(denom)
                
                # ratio:
                hists[period][label + category + "_ratio"] = hists[period][label + category].Clone()
                hists[period][label + category + "_ratio"].Divide(hists[mcperiod][label + category])
                hists[period][label + category + "_ratio"].SetLineColor(color)
                hists[period][label + category + "_ratio"].SetLineStyle(1)
                if "cutflow" in label:
                    hists[period][label + category + "_ratio"].SetTitle(";;Normalized Data / normalized MC")
                else:               
                    hists[period][label + category + "_ratio"].SetTitle(";%s;Normalized Data / normalized MC" % label)
                hists[period][label + category + "_ratio"].GetYaxis().SetRangeUser(0, 2)
                hists[period][label + category + "_ratio"].GetYaxis().SetNdivisions(4)
                hists[period][label + category + "_ratio"].GetXaxis().SetTitleSize(0.17)
                hists[period][label + category + "_ratio"].GetXaxis().SetLabelSize(0.17)
                hists[period][label + category + "_ratio"].GetYaxis().SetTitleSize(0.17)
                hists[period][label + category + "_ratio"].GetYaxis().SetLabelSize(0.17)
                hists[period][label + category + "_ratio"].Draw("pe same")
            
            pad1.cd()
            shared_utils.stamp()
            legend.Draw()
            pdfname = "%s/trackvar%s_%s.pdf" % (plotfolder, category, label)
            canvas.SaveAs(pdfname)
