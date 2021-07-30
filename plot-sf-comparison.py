#!/bin/env python
import os
import glob
import shared_utils
import plotting
import math
from ROOT import *

hists = {}

colors = [kBlack, kRed, kBlue, kTeal, kGreen, kRed-6, kPink-2, kMagenta, kViolet, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8, kOrange-10]

for label in ["low", "medium", "high", "high2", "high3", "high4", "noniso4", "noniso5", "new5", "new6", "new7"]:

    fin = TFile("plots%s/allperiods_sf_fit_sf_lumiweighted.root" % label, "open")  
    
    color = colors.pop(0)
    
    hists[label + "_short"] = fin.Get("h_scalefactor_short")
    hists[label + "_short"].SetDirectory(0)
    shared_utils.histoStyler(hists[label + "_short"])
    hists[label + "_short"].SetLineStyle(1)
    hists[label + "_short"].SetLineWidth(2)
    hists[label + "_short"].SetLineColorAlpha(color, 0.4)
    
    hists[label + "_long"] = fin.Get("h_scalefactor_long")
    hists[label + "_long"].SetDirectory(0)
    hists[label + "_long"].SetLineStyle(1)
    shared_utils.histoStyler(hists[label + "_long"])
    hists[label + "_long"].SetLineWidth(2)
    hists[label + "_long"].SetLineColorAlpha(color, 0.4)
    
    fin.Close()

binlabels = ["2016", "2017", "2018"]


for category in ["short", "long"]:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.5, y1=0.6, x2=0.85, y2=0.85)
    
    #if category == "short":
    #    labels = ["low", "medium", "high", "high2", "high4", "high3"]
    #elif category == "long":
    #    labels = ["high", "high2", "high4", "high3"]
    
    labels = ["new6", "new7"]
    
    for i, label in enumerate(labels):
        
        if i == 0:
            hists[label + "_" + category].Draw("hist e")
            hists[label + "_" + category].SetTitle(";;scale factor")
            for i_binlabel, binlabel in enumerate(binlabels):
                hists[label + "_" + category].GetXaxis().SetBinLabel(i_binlabel + 1, binlabel)    
            hists[label + "_" + category].GetXaxis().SetLabelSize(0.1)
        else:
            hists[label + "_" + category].Draw("hist e same")
        hists[label + "_" + category].GetYaxis().SetRangeUser(0.25,1.5)
            
        if label == "low":
            leglabel = "p_{T} = (30, 35) GeV"
        elif label == "medium":
            leglabel = "p_{T} = (35, 40) GeV"
        elif label == "high":
            leglabel = "p_{T} = (40, 45) GeV"
        elif label == "high2":
            leglabel = "p_{T} = (45, 50) GeV"
        elif label == "high4":
            leglabel = "p_{T} = (50, 55) GeV"
        elif label == "high3":
            leglabel = "p_{T} = (55, 60) GeV"
        elif label == "new5":
            leglabel = "p_{T} < 50 GeV"
        elif label == "new6":
            leglabel = "p_{T} < 50 GeV"
        elif label == "new7":
            leglabel = "p_{T} > 50 GeV"
            
        legend.AddEntry(hists[label + "_" + category], leglabel)
    
    legend.SetHeader(category + " tracks")
    legend.SetTextSize(0.04)
    legend.Draw()
    shared_utils.stamp()
    canvas.Print("allsf_%s.pdf" % category)

    
for category in ["short", "long"]:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.5, y1=0.6, x2=0.85, y2=0.85)
    
    labels = ["noniso4", "noniso5"]
    
    for i, label in enumerate(labels):
        
        if i == 0:
            hists[label + "_" + category].Draw("hist e")
            hists[label + "_" + category].SetTitle(";;scale factor")
            for i_binlabel, binlabel in enumerate(binlabels):
                hists[label + "_" + category].GetXaxis().SetBinLabel(i_binlabel + 1, binlabel)    
            hists[label + "_" + category].GetXaxis().SetLabelSize(0.1)
        else:
            hists[label + "_" + category].Draw("hist e same")
            
        hists[label + "_" + category].GetYaxis().SetRangeUser(0.5,1.5)
        
        if label == "low":
            leglabel = "p_{T} = (30, 35) GeV"
        elif label == "medium":
            leglabel = "p_{T} = (35, 40) GeV"
        elif label == "high":
            leglabel = "p_{T} = (40, 45) GeV"
        elif label == "high2":
            leglabel = "p_{T} = (45, 50) GeV"
        elif label == "high4":
            leglabel = "p_{T} = (50, 55) GeV"        
        elif label == "high3":
            leglabel = "p_{T} = (55, 60) GeV"
        elif label == "noniso4":
            leglabel = "rel. isolation = (0, 0.1)"
        elif label == "noniso5":
            leglabel = "rel. isolation = (0.1, 0.2)"
            
        legend.AddEntry(hists[label + "_" + category], leglabel)
    
    legend.SetHeader(category + " tracks")
    legend.SetTextSize(0.04)
    legend.Draw()
    shared_utils.stamp()
    canvas.Print("allsf_iso_%s.pdf" % category)