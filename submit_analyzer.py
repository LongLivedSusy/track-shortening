#!/bin/env python
import GridEngineTools
import os
import shared_utils
from ROOT import *

def submit(period):
    
    commands = [
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_1.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_2.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_3.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_4.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_5.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_6.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_7.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_8.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_9.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_10.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_11.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_12.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_13.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_14.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_15.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_16.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_17.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_18.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_19.root" % period,
        "cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile reRECO_%s_trackInfo_20.root" % period,
    ]

    commands_simple = [
        "python analyzer_simple.py --inputfile reRECO_%s_1.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_2.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_3.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_4.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_5.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_6.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_7.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_8.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_9.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_10.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_11.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_12.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_13.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_14.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_15.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_16.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_17.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_18.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_19.root" % period,
        "python analyzer_simple.py --inputfile reRECO_%s_20.root" % period,
    ]

    GridEngineTools.runParallel(commands, "multi")
    os.system("hadd -f histograms_%s.root histograms_*root && rm histograms_?.root && rm histograms_??.root" % period)


def plot(period):

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    # get histos:
    fin = TFile("histograms_%s.root" % period, "open")
    h_tracks_reco = fin.Get("h_tracks_reco")
    h_tracks_rereco = fin.Get("h_tracks_rereco")
    h_tracks_tagged = fin.Get("h_tracks_tagged")
    h_layers2D = fin.Get("h_layers2D")
    h_tracks_reco.SetDirectory(0)
    h_tracks_rereco.SetDirectory(0)
    h_layers2D.SetDirectory(0)
    h_tracks_tagged.SetDirectory(0)
    fin.Close()

    shared_utils.histoStyler(h_tracks_reco)
    shared_utils.histoStyler(h_tracks_rereco)
    shared_utils.histoStyler(h_tracks_tagged)
    h_tracks_reco.SetLineWidth(2)
    h_tracks_rereco.SetLineWidth(2)
    h_tracks_tagged.SetLineWidth(2)

    h_efficiency = h_tracks_rereco.Clone()
    h_efficiency.SetName("h_efficiency")
    h_efficiency.SetLineWidth(2)
    h_efficiency.Divide(h_tracks_reco)

    # draw efficiency:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.4, y1=0.17, x2=0.9, y2=0.4)
    legend.SetHeader(period)
    legend.SetTextSize(0.04)
    h_efficiency.Draw("hist e")
    legend.AddEntry(h_efficiency, "reconstruction efficiency")
    h_efficiency.SetTitle(";remaining layers;efficiency")
    h_efficiency.GetXaxis().SetRangeUser(0,11)
    h_efficiency.GetYaxis().SetRangeUser(0,1)
    shared_utils.stamp()
    legend.Draw()
    canvas.Print("plot_efficiency_%s.pdf" % period)  

    # draw abs values:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.4, y1=0.3, x2=0.9, y2=0.55)
    legend.SetHeader(period)
    legend.SetTextSize(0.035)
    h_tracks_reco.Draw("hist")
    h_tracks_reco.SetTitle(";remaining layers;tracks")
    h_tracks_reco.GetXaxis().SetRangeUser(0,11)
    h_tracks_rereco.Draw("same hist")
    h_tracks_rereco.SetLineStyle(2)
    h_tracks_tagged.Draw("same hist")
    h_tracks_tagged.SetLineStyle(2)
    h_tracks_tagged.SetLineColor(kRed)
    legend.AddEntry(h_tracks_reco, "tracks matched to muons")
    legend.AddEntry(h_tracks_rereco, "shortenend tracks")
    legend.AddEntry(h_tracks_tagged, "shortenend & tagged tracks")
    shared_utils.stamp()
    legend.Draw()
    canvas.Print("plot_absval_%s.pdf" % period)  

    # draw 2D plot:
    canvas = shared_utils.mkcanvas()
    h_layers2D.Draw("colz")
    shared_utils.stamp()
    canvas.Print("plot_layers2D_%s.pdf" % period)  
    
#os.system("rm histograms_*root")
#submit("Run2016")
plot("Run2016")
#os.system("rm histograms_*root")
#submit("Summer16")
#plot("Summer16")
