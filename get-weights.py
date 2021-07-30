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

def get_reweighting_factor(histofolder, plotfolder, suffix):
    
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
              ]
    
    histolabels = [
                "track_nValidPixelHits",
              ]
    
    hists = {}
    for period in periods:
        hists[period] = {}
        for label in histolabels:
            fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, period), "open")                       

            print label, histofolder, suffix, period

            hists[period][label] = fin.Get(label)
            hists[period][label].SetDirectory(0)
            hists[period][label].SetLineWidth(2)
            shared_utils.histoStyler(hists[period][label])
            fin.Close()

    # hweight = histTarget_NPixHits.Clone(); hweight.Divide(histSimulation)
    hweight = {}
    
    for year in ["2016", "2017", "2018"]:
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.6, y1=0.6, x2=0.85, y2=0.85)
        colors = range(209,250)[::3]
        
        for i, period in enumerate(sorted(periods)):
            
            if year not in period: continue
            
            if "Run2016" in period:
                mc = "Summer16"
            elif "Run2017" in period:
                mc = "Fall17"
            elif "Run2018" in period:
                mc = "Autumn18"
            else:
                continue
            
            num = hists[period]["track_nValidPixelHits"].Clone()
            denom = hists[mc]["track_nValidPixelHits"].Clone()
            num.Scale(1.0/num.Integral())
            denom.Scale(1.0/denom.Integral())
            hweight[period] = num.Clone()
            hweight[period].Divide(denom)
            hweight[period].SetName(period)
            shared_utils.histoStyler(hweight[period])
            hweight[period].SetLineColor(colors.pop(0))
            hweight[period].GetYaxis().SetRangeUser(0,5)
            hweight[period].SetTitle(";number of pixel hits;weight")
        
            if i==0:
                hweight[period].Draw("hist e")
            else:
                hweight[period].Draw("hist e same")
            
            legend.SetTextSize(0.035)
            legend.AddEntry(hweight[period], period)
        
        legend.Draw()
        shared_utils.stamp()
        canvas.SaveAs("hweights_%s.pdf" % year)

    # save weights:
    fout = TFile("hweights.root", "recreate")
    for period in hweight:
        hweight[period].Write()
    fout.Close()
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "NewShortPresel")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms_beforereweighting")

    (options, args) = parser.parse_args()
    
    plotfolder = "plots%s" % options.suffix
    get_reweighting_factor(options.histofolder, plotfolder, options.suffix)
