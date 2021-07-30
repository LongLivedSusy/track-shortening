#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

if __name__ == "__main__":
                        
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_64_p15OptionalJetVeto_merged"
    input_files_p0 = glob.glob(folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq*root")
    input_files_p1 = glob.glob(folder + "/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq*root")
    base_cut = "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975 && tracks_nMissingMiddleHits==0"
    #base_cut = "tracks_chiCandGenMatchingDR<0.01 "

    cuts = {}
    cuts["BDT_short"] = [
                "tracks_is_pixel_track==1",
                "tracks_pt>15",
                "tracks_passmask==1",
                "tracks_trackQualityHighPurity==1",
                "abs(tracks_eta)<2.4",
                "tracks_ptErrOverPt2<10",
                "tracks_dzVtx<0.1",
                "tracks_trkRelIso<0.2",
                "tracks_trackerLayersWithMeasurement>=2",
                "tracks_nValidTrackerHits>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nValidPixelHits>=2",
                "tracks_passPFCandVeto==1",
                "tracks_passleptonveto==1",
                "tracks_passpionveto==1",
                "tracks_passjetveto==1",
                #"tracks_deDxHarmonic2pixel>2.0",
                "tracks_nMissingOuterHits>=0",
                "tracks_matchedCaloEnergy/tracks_p<0.2",
                "tracks_mva_tight_may20_chi2_pt10>0",
    ]

    cuts["BDT_long"] = [
                "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
                "tracks_pt>40",
                "tracks_passmask==1",
                "tracks_trackQualityHighPurity==1",
                "abs(tracks_eta)<2.4",
                "tracks_ptErrOverPt2<10",
                "tracks_dzVtx<0.1",
                "tracks_trkRelIso<0.2",
                "tracks_trackerLayersWithMeasurement>=2",
                "tracks_nValidTrackerHits>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nValidPixelHits>=2",
                "tracks_passPFCandVeto==1",
                "tracks_passleptonveto==1",
                "tracks_passpionveto==1",
                "tracks_passjetveto==1",
                ##"tracks_deDxHarmonic2pixel>2.0",
                "tracks_nMissingOuterHits>=2",
                "tracks_matchedCaloEnergy/tracks_p<0.2",
                "tracks_mva_tight_may20_chi2_pt10>0",
    ]
    
    for phase in [0, 1]:
    
        if phase == 0:
            input_files = input_files_p0
        else:
            input_files = input_files_p1        
    
        signal_matchedtracks = plotting.get_histogram_from_file(input_files, "Events", "tracks_trackerLayersWithMeasurement", base_cut, nBinsX=21, xmin=0, xmax=21)
        signal_taggedtracks_short = plotting.get_histogram_from_file(input_files, "Events", "tracks_trackerLayersWithMeasurement", base_cut + " && " + " && ".join(cuts["BDT_short"]), nBinsX=21, xmin=0, xmax=21)
        signal_taggedtracks_long = plotting.get_histogram_from_file(input_files, "Events", "tracks_trackerLayersWithMeasurement", base_cut + " && " + " && ".join(cuts["BDT_long"]), nBinsX=21, xmin=0, xmax=21)
            
        signal_matchedtracks.SetLineWidth(2)
        signal_taggedtracks_short.SetLineWidth(2)
        signal_taggedtracks_long.SetLineWidth(2)
        shared_utils.histoStyler(signal_matchedtracks)
        shared_utils.histoStyler(signal_taggedtracks_short)
        shared_utils.histoStyler(signal_taggedtracks_long)
        
        signal_taggedtracks = signal_taggedtracks_short.Clone()
        signal_taggedtracks.SetName("h_tagged")
        signal_taggedtracks.Add(signal_taggedtracks_long)
    
        if phase == 0:
            h_efficiency_p0 = signal_taggedtracks.Clone()
            h_efficiency_p0.SetName("h_tagefficiency_p0")
            h_efficiency_p0.Divide(signal_matchedtracks)
        else:
            h_efficiency_p1 = signal_taggedtracks.Clone()
            h_efficiency_p1.SetName("h_tagefficiency_p1")
            h_efficiency_p1.Divide(signal_matchedtracks)
    
    # draw efficiency:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.35, y1=0.2, x2=0.9, y2=0.4)
    legend.SetHeader("Signal (m_{glu}=2 TeV, m_{LSP}==1.975 TeV)")
    legend.SetTextSize(0.04)
    h_efficiency_p0.GetYaxis().SetRangeUser(0,1.2)
    h_efficiency_p0.SetTitle(";layers with measurement;efficiency")
    h_efficiency_p0.Draw("hist e")
    h_efficiency_p0.SetLineColor(kBlack)
    legend.AddEntry(h_efficiency_p0, "tagging efficiency (Phase-0)")
    h_efficiency_p1.Draw("hist e same")
    h_efficiency_p1.SetLineColor(kBlue)
    legend.AddEntry(h_efficiency_p1, "tagging efficiency (Phase-1)")
    shared_utils.stamp()
    legend.Draw()
    canvas.Print("plots/trackShortening_efficiency_signal.pdf")  
    