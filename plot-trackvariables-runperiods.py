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

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "MCReweighting")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")
    parser.add_option("--reweighted", dest = "mc_reweighted", action = "store_true")

    (options, args) = parser.parse_args()
    
    histofolder = options.histofolder
    suffix = options.suffix
    
    plotfolder = "plots_%s" % options.suffix
    
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
                  "track_trkRelIso": [[0, 0.005, 0.01, 0.015, 0.02, 0.2], 0, 0.2, "relative track isolation"],
                  "track_dxyVtx": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "d_{xy} (cm)"],
                  "track_dzVtx": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "d_{z} (cm)"],
                  "track_nMissingOuterHits": [20, 0, 20, "missing outer hits"],
                  "track_nValidPixelHits": [10, 0, 10, "pixel hits"],
                  "track_nValidTrackerHits": [20, 0, 20, "tracker hits"],
                  "track_chi2perNdof": [20, 0, 5.0, "track #chi^{2}/ndof"],
                  "track_ptErrOverPt2": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "#Delta p_{T} / p_{T}^{2} (GeV^{-1})"],                  
                  "track_matchedCaloEnergy": [20, 0, 50, "E_{dep} (GeV)"],
                  "h_muonPt": [20, 0, 1000 , "h_muonPt"],
                 }
    
    categories = [
                    "",
                    #"_short",
                    #"_long",
                    ]

    years = [
                     "2016",
                     "2017",
                     "2018"
                    ]

    # get all histos:
    hists = {}
    for period in periods:
        hists[period] = {}
        for category in categories:
                
            for label in variables:

                if category == "" and "h_muon" not in label: continue
                if "h_muon" in label and category != "": continue

                fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, period), "open")                       
                hists[period][label + category] = fin.Get(label + category)
                hists[period][label + category].SetDirectory(0)
                hists[period][label + category].SetLineWidth(2)
                shared_utils.histoStyler(hists[period][label + category])
                fin.Close()

    for category in categories:
        
        for year in years:
            
            for label in variables:
            
                if category == "" and "h_muon" not in label: continue
                if "h_muon" in label and category != "": continue

                canvas = shared_utils.mkcanvas()
                
                pad1 = TPad("pad1", "pad1", 0, 0.25, 1, 1.0)
                pad1.SetBottomMargin(0.0)
                pad1.SetLeftMargin(0.12)
                pad1.SetGridx()
                pad1.Draw()
                pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.25)
                pad2.SetTopMargin(0.0)
                pad2.SetBottomMargin(0.3)
                pad2.SetLeftMargin(0.12)
                pad2.SetGridx()
                pad2.SetGridy()
                pad2.Draw()
                pad1.cd()
                
                legend = shared_utils.mklegend(x1=0.6, y1=0.6, x2=0.85, y2=0.85)
                if category == "":
                    legend.SetHeader("short + long tracks")
                else:    
                    legend.SetHeader("%s tracks" % (category.replace("_", "")))
                legend.SetTextSize(0.035)
                              
                pad1.cd()
                pad1.SetLogy()
                color = kBlack
                
                if not options.mc_reweighted:
                
                    if year == "2016":
                        mcperiod = "Summer16"
                    elif year == "2017":
                        mcperiod = "Fall17"
                    elif year == "2018":
                        mcperiod = "Autumn18"

                    print hists[mcperiod].keys()
                    
                    # normalize
                    if hists[mcperiod][label + category].Integral()>0:
                        hists[mcperiod][label + category].Scale(1.0/hists[mcperiod][label + category].Integral())
                    
                    hists[mcperiod][label + category].Draw("hist e")
                    hists[mcperiod][label + category].SetLineColor(color)
                    hists[mcperiod][label + category].SetLineStyle(1)
                    hists[mcperiod][label + category].SetTitle(";;Events")
                    legend.AddEntry(hists[mcperiod][label + category], mcperiod)
                
                colors = [97, 94, 91, 86, 81, 70, 65, 61, 51]
                
                for i_period, period in enumerate(periods):
                    if "Run201" not in period: continue
                    if "rw" in period: continue
                                
                    if year not in period: continue

                    color = colors.pop(0)
                    
                    if i_period == 0:
                        drawoption = "hist e"
                    else:
                        drawoption = "hist e same"

                    legend.AddEntry(hists[period][label + category], period)

                    pad1.cd()
                    
                    # normalize:
                    if hists[period][label + category].Integral() > 0:
                        hists[period][label + category].Scale(1.0/hists[period][label + category].Integral())
                    
                    hists[period][label + category].Draw(drawoption)
                    hists[period][label + category].SetLineColor(color)
                    hists[period][label + category].SetLineStyle(1)
                    #hists[period][label + category].SetTitle(";%s;Normalized Data / normalized MC" % label)
                    hists[period][label + category].SetTitle(";;Events")
                    #hists[period][label + category].GetYaxis().SetRangeUser(0,2.5)


                    # MC:
                    if options.mc_reweighted:
                        if year == "2016":
                            this_mcperiod = "Summer16rw" + period
                        elif year == "2017":
                            this_mcperiod = "Fall17rw" + period
                        elif year == "2018":
                            this_mcperiod = "Autumn18rw" + period

                        if hists[this_mcperiod][label + category].Integral()>0:
                            hists[this_mcperiod][label + category].Scale(1.0/hists[this_mcperiod][label + category].Integral())
                        hists[this_mcperiod][label + category].Draw(drawoption)
                        hists[this_mcperiod][label + category].SetLineColor(color)
                        hists[this_mcperiod][label + category].SetLineStyle(1)
                        hists[this_mcperiod][label + category].SetTitle(";;Events")
                        legend.AddEntry(hists[this_mcperiod][label + category], this_mcperiod)

                    pad2.cd()
                    #num = hists[period][label + category].Clone()
                    #num.Scale(1.0/num.Integral())
                    #denom = hists[mcperiod][label + category].Clone()
                    #denom.Scale(1.0/denom.Integral())
                    #hists[period][label + category + "_ratio"] = num.Clone()
                    #hists[period][label + category + "_ratio"].Divide(denom)
                    
                    # ratio:
                    hists[period][label + category + "_ratio"] = hists[period][label + category].Clone()
                    if not options.mc_reweighted:
                        hists[period][label + category + "_ratio"].Divide(hists[mcperiod][label + category])
                    else:
                        hists[period][label + category + "_ratio"].Divide(hists[this_mcperiod][label + category])
                    
                    hists[period][label + category + "_ratio"].Draw(drawoption)
                    hists[period][label + category + "_ratio"].SetLineColor(color)
                    hists[period][label + category + "_ratio"].SetLineStyle(1)
                    hists[period][label + category + "_ratio"].SetTitle(";%s;Normalized Data / normalized MC" % label)
                    hists[period][label + category + "_ratio"].GetYaxis().SetRangeUser(0,2.5)
                    
                pad1.cd()   
                shared_utils.stamp()
                legend.Draw()
                pdfname = "%s/trackvar_runperiods_%s%s_%s.pdf" % (plotfolder, label, category, year)
                
                if options.mc_reweighted:
                    pdfname = pdfname.replace(".pdf", "_reweighted.pdf")
                canvas.SaveAs(pdfname)
            
        
                             
