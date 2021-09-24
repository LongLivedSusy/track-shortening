#!/bin/env python
import os
import submit_analyzer
from ROOT import *
import shared_utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

for label in ["fit_sf_short", "fit_sfreco_short", "fit_sftag_short"]:

    if label == "fit_sf_short":
        ytitle = "combined scale factor"
    if label == "fit_sfreco_short":
        ytitle = "reconstruction scale factor"
    if label == "fit_sftag_short":
        ytitle = "tagging scale factor"

    xmax = len(submit_analyzer.suffixes)

    canvas = shared_utils.mkcanvas_wide("c1")
    histo2017 = TH1F("histo2017", ";;%s" % ytitle, xmax, 0, xmax)
    shared_utils.histoStyler(histo2017)
    histo2017.SetLineColor(kBlue)
    histo2018 = TH1F("histo2018", ";;%s" % ytitle, xmax, 0, xmax)
    shared_utils.histoStyler(histo2018)
    histo2018.SetLineColor(kRed)
    
    for i_suffix, suffix in enumerate(submit_analyzer.suffixes):
    
        try:
    
            fin = TFile("plots%s_new2/allperiods_sf_combined.root" % suffix, "read")
            
            fit_sf_short = fin.Get(label)
            
            #print i_suffix, "\t", suffix, "\t", fit_sf_short.GetBinContent(1), "\t", fit_sf_short.GetBinContent(2)
            print i_suffix, "\t", suffix
            
            histo2017.SetBinContent(i_suffix+1, fit_sf_short.GetBinContent(1))
            histo2017.SetBinError(i_suffix+1, fit_sf_short.GetBinError(1))
            histo2018.SetBinContent(i_suffix+1, fit_sf_short.GetBinContent(2))
            histo2018.SetBinError(i_suffix+1, fit_sf_short.GetBinError(2))
            
            #histo2017.GetXaxis().SetBinLabel(i_suffix+1, suffix.replace("aug21v4-", ""))    
            #histo2018.GetXaxis().SetBinLabel(i_suffix+1, suffix.replace("aug21v4-", ""))    
            histo2017.GetYaxis().SetTitleOffset(0.7)
            histo2018.GetYaxis().SetTitleOffset(0.7)
            #histo2017.GetXaxis().SetLabelSize(0.03)    
            #histo2018.GetXaxis().SetLabelSize(0.03)            
            
            fin.Close()
        
        except:
            
            print "Ignoring", suffix
    
    legend = shared_utils.mklegend(0.15, 0.15, 0.45, 0.3)
    
    legend.SetHeader("constant #epsilon_{bg} = 7.25%")
    legend.SetTextSize(0.035)
    
    histo2018.Draw("hist e")
    histo2017.Draw("hist e same")
    
    legend.AddEntry(histo2017, "2017")
    legend.AddEntry(histo2018, "2018")
    
    histo2017.GetYaxis().SetRangeUser(0.25,1.25)
    histo2018.GetYaxis().SetRangeUser(0.25,1.25)
    
    canvas.SetGridx(True)
    canvas.SetGridy(True)
    
    legend.Draw()
    
    canvas.SaveAs("plots/bdt_same_bg_eff_with_%s.pdf" % label)
