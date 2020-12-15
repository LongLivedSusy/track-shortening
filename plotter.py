#!/bin/env python
import shared_utils
from ROOT import *

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

# get histos:
fin = TFile("histograms.root", "open")
h_tracks_reco = fin.Get("h_tracks_reco")
h_tracks_rereco = fin.Get("h_tracks_rereco")
h_layers2D = fin.Get("h_layers2D")
h_tracks_reco.SetDirectory(0)
h_tracks_rereco.SetDirectory(0)
h_layers2D.SetDirectory(0)
fin.Close()

shared_utils.histoStyler(h_tracks_reco)
shared_utils.histoStyler(h_tracks_rereco)
h_tracks_reco.SetLineWidth(2)
h_tracks_rereco.SetLineWidth(2)

h_efficiency = h_tracks_rereco.Clone()
h_efficiency.SetName("h_efficiency")
h_efficiency.SetLineWidth(2)
h_efficiency.Divide(h_tracks_reco)

# draw efficiency:
canvas = shared_utils.mkcanvas()
legend = shared_utils.mklegend(x1=0.4, y1=0.17, x2=0.9, y2=0.4)
legend.SetHeader("2016 SingleMuon Data")
legend.SetTextSize(0.04)
h_efficiency.Draw("hist")
h_efficiency.SetTitle(";remaining layers;efficiency")
h_efficiency.GetXaxis().SetRangeUser(0,11)
h_efficiency.GetYaxis().SetRangeUser(0,1)
shared_utils.stamp()
legend.Draw()
canvas.Print("plot_efficiency.pdf")  

# draw abs values:
canvas = shared_utils.mkcanvas()
legend = shared_utils.mklegend(x1=0.4, y1=0.17, x2=0.9, y2=0.4)
legend.SetHeader("2016 SingleMuon Data")
legend.SetTextSize(0.04)

h_tracks_reco.Draw("hist")
h_tracks_reco.SetTitle(";remaining layers;tracks")
h_tracks_reco.GetXaxis().SetRangeUser(0,11)
h_tracks_rereco.Draw("same hist")
h_tracks_rereco.SetLineStyle(2)
legend.AddEntry(h_tracks_reco, "tracks matched to muons")
legend.AddEntry(h_tracks_rereco, "after track shortening")
shared_utils.stamp()
legend.Draw()
canvas.Print("plot_absval.pdf")  

# draw 2D plot:
canvas = shared_utils.mkcanvas()
h_layers2D.Draw("colz")
canvas.Print("plot_layers2D.pdf")  

