#!/bin/env python
import GridEngineTools
import os
import shared_utils
from ROOT import *

os.system("mkdir -p plots")
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def submit(period):
    
    commands = []
    for i in range(1, 21):
        commands.append("cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py --inputfile %s_ISOTRACKS/*_%s.root" % (period, i))

    GridEngineTools.runParallel(commands, "multi")
    os.system("hadd -f histograms_%s.root histograms_%s_?.root histograms_%s_??.root && rm histograms_%s_?.root && rm histograms_%s_??.root" % (period, period, period, period, period))


def plot(period):

    # get histos:
    fin = TFile("histograms_%s.root" % period, "open")
    hists = {}
    for label in ["h_tracks_reco", "h_tracks_rereco", "h_tracks_preselection", "h_tracks_tagged", "h_layers2D", "h_shortbdt2D", "h_longbdt2D", "h_trkRelIso"]:
        hists[label] = fin.Get(label)
        hists[label].SetDirectory(0)
        hists[label].SetLineWidth(2)
        shared_utils.histoStyler(hists[label])
    fin.Close()

    hists["h_efficiency"] = hists["h_tracks_rereco"].Clone()
    hists["h_efficiency"].SetName("h_efficiency")
    hists["h_efficiency"].SetLineWidth(2)
    hists["h_efficiency"].Divide(hists["h_tracks_reco"])

    hists["h_tagefficiency"] = hists["h_tracks_tagged"].Clone()
    hists["h_tagefficiency"].SetName("h_tagefficiency")
    hists["h_tagefficiency"].SetLineWidth(2)
    hists["h_tagefficiency"].Divide(hists["h_tracks_rereco"])

    # draw efficiency:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
    legend.SetHeader(period)
    legend.SetTextSize(0.04)
    hists["h_efficiency"].Draw("hist e")
    hists["h_tagefficiency"].SetLineColor(kRed)
    hists["h_tagefficiency"].Draw("hist e same")
    legend.AddEntry(hists["h_efficiency"], "reconstruction efficiency")
    legend.AddEntry(hists["h_tagefficiency"], "tagging efficiency")
    hists["h_efficiency"].SetTitle(";remaining layers;efficiency")
    #hists["h_efficiency"].GetXaxis().SetRangeUser(0,11)
    hists["h_efficiency"].GetYaxis().SetRangeUser(0,1)
    shared_utils.stamp()
    legend.Draw()
    canvas.Print("plots/plot_efficiency_%s.pdf" % period)  

    # draw abs values:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
    legend.SetHeader(period)
    legend.SetTextSize(0.035)
    hists["h_tracks_reco"].Draw("hist")
    hists["h_tracks_reco"].SetTitle(";remaining layers;tracks")
    #hists["h_tracks_reco"].GetXaxis().SetRangeUser(0,11)
    hists["h_tracks_rereco"].Draw("same hist")
    hists["h_tracks_rereco"].SetLineStyle(2)
    #h_tracks_preselection.Draw("same hist")
    #h_tracks_preselection.SetLineStyle(2)
    #h_tracks_preselection.SetLineStyle(2)
    #h_tracks_preselection.SetLineColor(kBlue)
    hists["h_tracks_tagged"].Draw("same hist")
    hists["h_tracks_tagged"].SetLineStyle(2)
    hists["h_tracks_tagged"].SetLineColor(kRed)
    legend.AddEntry(hists["h_tracks_reco"], "tracks matched to muons")
    legend.AddEntry(hists["h_tracks_rereco"], "shortenend tracks")
    #legend.AddEntry(h_tracks_preselection, "shortenend & preselected tracks")
    legend.AddEntry(hists["h_tracks_tagged"], "shortenend & tagged tracks")
    shared_utils.stamp()
    legend.Draw()
    canvas.Print("plots/plot_absval_%s.pdf" % period)  

    # draw other plots:
    for label in ["h_layers2D", "h_shortbdt2D", "h_longbdt2D", "h_trkRelIso"]:
        canvas = shared_utils.mkcanvas()
        if "2D" in label:
            hists[label].Draw("colz")
            canvas.SetRightMargin(.18)
            size = 0.059
            font = 132
            hists[label].GetZaxis().SetLabelFont(font)
            hists[label].GetZaxis().SetTitleFont(font)
            hists[label].GetZaxis().SetTitleSize(size)
            hists[label].GetZaxis().SetLabelSize(size)
            hists[label].GetZaxis().SetTitleOffset(1.0)
            hists[label].GetZaxis().SetTitle("Events")
        else:
            hists[label].Draw("hist")        
        shared_utils.stamp()
        canvas.Print("plots/plot_%s_%s.pdf" % (label.replace("h_", ""), period))  


def scalefactors():

    # get histos:
    hists_data = {}
    hists_mc = {}
    for label in ["h_tracks_reco", "h_tracks_rereco", "h_tracks_preselection", "h_tracks_tagged", "h_layers2D", "h_shortbdt2D", "h_longbdt2D", "h_trkRelIso"]:
        fin = TFile("histograms_Run2016.root", "open")
        hists_data[label] = fin.Get(label)
        hists_data[label].SetDirectory(0)
        hists_data[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_data[label])
        fin.Close()
        
        fin = TFile("histograms_Summer16.root", "open")
        hists_mc[label] = fin.Get(label)
        hists_mc[label].SetDirectory(0)
        hists_mc[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_mc[label])
        fin.Close()

    hists_data["h_tagefficiency"] = hists_data["h_tracks_tagged"].Clone()
    hists_data["h_tagefficiency"].SetName("h_tagefficiency")
    hists_data["h_tagefficiency"].SetLineWidth(2)
    hists_data["h_tagefficiency"].Divide(hists_data["h_tracks_rereco"])
    
    hists_mc["h_tagefficiency"] = hists_mc["h_tracks_tagged"].Clone()
    hists_mc["h_tagefficiency"].SetName("h_tagefficiency")
    hists_mc["h_tagefficiency"].SetLineWidth(2)
    hists_mc["h_tagefficiency"].Divide(hists_mc["h_tracks_rereco"])

    hists_data["h_scalefactor"] = hists_data["h_tagefficiency"].Clone()
    hists_data["h_scalefactor"].SetName("h_scalefactor")
    hists_data["h_scalefactor"].SetLineWidth(2)
    hists_data["h_scalefactor"].Divide(hists_mc["h_tagefficiency"])
    
    # draw scale factor:
    canvas = shared_utils.mkcanvas()
    hists_data["h_scalefactor"].Draw("hist e")
    hists_data["h_scalefactor"].SetTitle(";remaining layers;scale factor")
    hists_data["h_scalefactor"].GetYaxis().SetRangeUser(0,2)
    shared_utils.stamp()
    canvas.Print("plots/plot_scalefactor.pdf")  

for period in ["Summer16", "Run2016"]:
    submit(period)
    plot(period)
scalefactors()
