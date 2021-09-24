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

def get_reweighting_factor(histofolder, suffix):
    
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
                #"track_nValidPixelHits",
                #"track_nValidPixelHits_short",
                #"track_nValidPixelHits_long",
                "h_muonPtCand",
                "h_muonPt2Cand",
                "h_muonPt",
                #"track_pt",
                "track_pt_short",
                #"track_pt_long",
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

    print "all loaded"

    # hweight = histTarget_NPixHits.Clone(); hweight.Divide(histSimulation)
    hweight = {}
    
    for label in histolabels:

        hweight[label] = {}

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
                
                #num = hists[period]["track_nValidPixelHits"].Clone()
                #denom = hists[mc]["track_nValidPixelHits"].Clone()
                num = hists[period][label].Clone()
                denom = hists[mc][label].Clone()

                if num.Integral()>0:
                    num.Scale(1.0/num.Integral())
                else:
                    print label, year, period, num.Integral()

                if denom.Integral()>0:
                    denom.Scale(1.0/denom.Integral())
                else:
                    print label, year, period, denom.Integral()

                hweight[label][period] = num.Clone()
                hweight[label][period].Divide(denom)
                hweight[label][period].SetName(period + "_" + label)
                shared_utils.histoStyler(hweight[label][period])
                hweight[label][period].SetLineColor(colors.pop(0))
                hweight[label][period].GetYaxis().SetRangeUser(0,5)
                #hweight[label][period].SetTitle(";number of pixel hits;weight")
                hweight[label][period].SetTitle(";track p_{T} (GeV);weight")
            
                #hweight[label][period].GetXaxis().SetRangeUser(0, 250)
            
                if i==0:
                    hweight[label][period].Draw("hist e")
                else:
                    hweight[label][period].Draw("hist e same")

                # Draw overflow:
                last_bin = hweight[label][period].GetNbinsX()+1
                overflow = hweight[label][period].GetBinContent(last_bin)
                print overflow
                hweight[label][period].AddBinContent((last_bin-1), overflow)

                legend.SetTextSize(0.035)
                legend.AddEntry(hweight[label][period], period)
            
            legend.Draw()
            shared_utils.stamp()
            canvas.SaveAs("plots/hweights_%s_%s.pdf" % (label, year))

    # save weights:
    fout = TFile("hweights.root", "recreate")
    for label in histolabels:
        for period in hweight[label]:
            hweight[label][period].Write()
    fout.Close()
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "test3")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")

    (options, args) = parser.parse_args()
    
    get_reweighting_factor(options.histofolder, options.suffix)
