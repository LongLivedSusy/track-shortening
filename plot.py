#!/bin/env python
import os
import glob
import shared_utils
import plotting
from ROOT import *

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

histolabels = [
                "h_tracks_reco",                     
                "h_tracks_rereco",                   
                "h_tracks_preselection",             
                "h_tracks_tagged",                   
                "h_tracks_tagged_rebinned",                   
                "h_tracks_reco_rebinned",                     
                "h_tracks_rereco_rebinned",                   
                "h_tracks_tagged_short",                   
                "h_tracks_reco_short",                     
                "h_tracks_rereco_short",                   
                "h_tracks_tagged_long",                   
                "h_tracks_reco_long",                     
                "h_tracks_rereco_long",                   
                "h_layers2D",                        
                "h_shortbdt2D",                      
                "h_longbdt2D",                       
                "h_muonPt",                          
                "h_muonEta",                         
                "h_muonPtCand",                          
                "h_muonEtaCand",                         
                "h_pfIso",                           
                #"track_is_pixel_track",              
                #"track_dxyVtx",                      
                #"track_dzVtx",                                     
                #"track_trkRelIso",                   
                #"track_nValidPixelHits",             
                #"track_nValidTrackerHits",           
                #"track_trackerLayersWithMeasurement",
                #"track_ptErrOverPt2",                
                #"track_chi2perNdof",                 
                #"track_mva",                         
                #"track_pt",                          
                #"track_trackQualityHighPurity",      
                #"track_nMissingInnerHits",           
                #"track_passPFCandVeto",              
                #"track_nMissingOuterHits",           
                #"track_matchedCaloEnergy",           
                #"track_p",         
                "cutflow",
                "h_ptratio",
                "h_ptratio2D",
                "h_chi2ndof2D",
              ]
              
# add layer-dependent track variable histograms:
for label in list(histolabels):
    if "track_" in label or "h_ptratio" in label:
        for i in range(3,9):
            histolabels.append(label + "_layer%s" % i)


def plot(period, suffix):
    
    print period

    os.system("mkdir -p plots%s" % suffix)

    # get histos:
    fin = TFile("histograms/histograms%s_%s.root" % (suffix, period), "open")
    hists = {}
    for label in histolabels:
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
    canvas.Print("plots%s/trackShortening_efficiency_%s.pdf" % (suffix, period))  

    # draw abs values:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
    legend.SetHeader(period)
    legend.SetTextSize(0.035)
    hists["h_tracks_reco"].Draw("hist e")
    hists["h_tracks_reco"].SetTitle(";remaining layers;tracks")
    #hists["h_tracks_reco"].GetXaxis().SetRangeUser(0,11)
    hists["h_tracks_rereco"].Draw("hist e same")
    hists["h_tracks_rereco"].SetLineStyle(2)
    #h_tracks_preselection.Draw("same hist")
    #h_tracks_preselection.SetLineStyle(2)
    #h_tracks_preselection.SetLineStyle(2)
    #h_tracks_preselection.SetLineColor(kBlue)
    hists["h_tracks_tagged"].Draw("same hist e")
    hists["h_tracks_tagged"].SetLineStyle(2)
    hists["h_tracks_tagged"].SetLineColor(kRed)
    legend.AddEntry(hists["h_tracks_reco"], "tracks matched to muons")
    legend.AddEntry(hists["h_tracks_rereco"], "shortenend tracks")
    #legend.AddEntry(h_tracks_preselection, "shortenend & preselected tracks")
    legend.AddEntry(hists["h_tracks_tagged"], "shortenend & tagged tracks")
    shared_utils.stamp()
    legend.Draw()
    canvas.Print("plots%s/trackShortening_absval_%s.pdf" % (suffix, period))  

    # draw other plots:
    for label in histolabels:
        if label in ["h_layers2D", "h_shortbdt2D", "h_longbdt2D", "h_ptratio2D", "h_chi2ndof2D"]:
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
            else:
                canvas.SetLogy(True)
                hists[label].Scale(1.0/hists[label].Integral())
                hists[label].GetYaxis().SetRangeUser(1e-4,1e1)
                hists[label].Draw("hist e")
                hists[label].SetTitle(";%s;normalized events" % label)
                            
            shared_utils.stamp()
            canvas.Print("plots%s/trackShortening_%s_%s.pdf" % (suffix, label.replace("h_", ""), period))  


def allperiods(suffix = ""):
        
    #extra = "_short"
    #extra = "_long"
    extra = ""
        
    periods = [
                "Summer16",
                "Fall17",
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
    
    # get histos:
    hists = {}
    for period in periods:
        hists[period] = {}
        for label in histolabels:
            fin = TFile("histograms/histograms%s_%s.root" % (suffix, period), "open")
            hists[period][label] = fin.Get(label)
            hists[period][label].SetDirectory(0)
            hists[period][label].SetLineWidth(2)
            shared_utils.histoStyler(hists[period][label])
            fin.Close()
            
    for period in periods:
        
        if "Run" not in period:
            continue
        
        if "Run2016" in period:
            mcperiod = "Summer16"
        else:
            mcperiod = "Fall17"
        
        print period
        
        # tagging:
        
        hists[period]["h_tagefficiency"] = hists[period]["h_tracks_tagged" + extra].Clone()
        hists[period]["h_tagefficiency"].SetName("h_tagefficiency")
        hists[period]["h_tagefficiency"].SetLineWidth(2)
        hists[period]["h_tagefficiency"].Divide(hists[period]["h_tracks_rereco" + extra])
        
        hists[mcperiod]["h_tagefficiency"] = hists[mcperiod]["h_tracks_tagged" + extra].Clone()
        hists[mcperiod]["h_tagefficiency"].SetName("h_tagefficiency")
        hists[mcperiod]["h_tagefficiency"].SetLineWidth(2)
        hists[mcperiod]["h_tagefficiency"].Divide(hists[mcperiod]["h_tracks_rereco" + extra])
        
        hists[period]["h_tagscalefactor"] = hists[period]["h_tagefficiency"].Clone()
        hists[period]["h_tagscalefactor"].SetName("h_tagscalefactor")
        hists[period]["h_tagscalefactor"].SetLineWidth(2)
        hists[period]["h_tagscalefactor"].Divide(hists[mcperiod]["h_tagefficiency"])
        
        # reconstruction:
        
        hists[period]["h_recoefficiency"] = hists[period]["h_tracks_reco" + extra].Clone()
        hists[period]["h_recoefficiency"].SetName("h_recoefficiency")
        hists[period]["h_recoefficiency"].SetLineWidth(2)
        hists[period]["h_recoefficiency"].Divide(hists[period]["h_tracks_rereco" + extra])
        
        hists[mcperiod]["h_recoefficiency"] = hists[mcperiod]["h_tracks_reco" + extra].Clone()
        hists[mcperiod]["h_recoefficiency"].SetName("h_recoefficiency")
        hists[mcperiod]["h_recoefficiency"].SetLineWidth(2)
        hists[mcperiod]["h_recoefficiency"].Divide(hists[mcperiod]["h_tracks_rereco" + extra])
        
        hists[period]["h_recoscalefactor"] = hists[period]["h_recoefficiency"].Clone()
        hists[period]["h_recoscalefactor"].SetName("h_recoscalefactor")
        hists[period]["h_recoscalefactor"].SetLineWidth(2)
        hists[period]["h_recoscalefactor"].Divide(hists[mcperiod]["h_recoefficiency"])
        
        # global scale factor
        
        hists[period]["h_scalefactor"] = hists[period]["h_tagscalefactor"].Clone()
        hists[period]["h_scalefactor"].SetName("h_scalefactor")
        hists[period]["h_scalefactor"].SetLineWidth(2)
        hists[period]["h_scalefactor"].Multiply(hists[period]["h_recoefficiency"])
        
    # draw:
    
    colors = [kBlack, kRed, kRed-6, kPink-2, kMagenta, kViolet, kBlue, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8]
    
    for year in ["Run", "2016", "2017", "2018"]:    

        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.3, y1=0.2, x2=0.6, y2=0.35)
        for i, period in enumerate(periods):
            
            if year not in period: continue
            
            if i == 0:
                hists[period]["h_scalefactor"].Draw("hist e")
            else:
                hists[period]["h_scalefactor"].Draw("hist e same")
            hists[period]["h_scalefactor"].GetXaxis().SetRangeUser(3,21)
            hists[period]["h_scalefactor"].GetYaxis().SetRangeUser(0,2)
            hists[period]["h_scalefactor"].SetTitle(";remaining layers;scale factor")
            legend.AddEntry(hists[period]["h_scalefactor"], period)
            hists[period]["h_scalefactor"].SetLineColor(colors.pop(0))
            
        legend.Draw()
        shared_utils.stamp()
        canvas.Print("plots%s/trackShortening_allSF_%s%s.pdf" % (suffix, year, extra))

        if year == "Run":
            colors = [kBlack, kRed, kRed-6, kPink-2, kMagenta, kViolet, kBlue, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8]
            
    

def scalefactors(dataperiod, mcperiod, suffix, extralabel):
    
    # get histos:
    hists_data = {}
    hists_mc = {}
    for label in histolabels:
        fin = TFile("histograms/histograms%s_%s.root" % (suffix, dataperiod), "open")
        hists_data[label] = fin.Get(label)
        hists_data[label].SetDirectory(0)
        hists_data[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_data[label])
        fin.Close()
        
        fin = TFile("histograms/histograms%s_%s.root" % (suffix, mcperiod), "open")
        hists_mc[label] = fin.Get(label)
        hists_mc[label].SetDirectory(0)
        hists_mc[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_mc[label])
        fin.Close()
    
    if False:
    
        # taging SF:
            
        hists_data["h_tagefficiency"] = hists_data["h_tracks_tagged"].Clone()
        hists_data["h_tagefficiency"].SetName("h_tagefficiency")
        hists_data["h_tagefficiency"].SetLineWidth(2)
        hists_data["h_tagefficiency"].Divide(hists_data["h_tracks_rereco"])
        
        hists_mc["h_tagefficiency"] = hists_mc["h_tracks_tagged"].Clone()
        hists_mc["h_tagefficiency"].SetName("h_tagefficiency")
        hists_mc["h_tagefficiency"].SetLineWidth(2)
        hists_mc["h_tagefficiency"].Divide(hists_mc["h_tracks_rereco"])
        
        hists_data["h_tagscalefactor"] = hists_data["h_tagefficiency"].Clone()
        hists_data["h_tagscalefactor"].SetName("h_tagscalefactor")
        hists_data["h_tagscalefactor"].SetLineWidth(2)
        hists_data["h_tagscalefactor"].Divide(hists_mc["h_tagefficiency"])
        
        hists_data["h_tagefficiency_short"] = hists_data["h_tracks_tagged_short"].Clone()
        hists_data["h_tagefficiency_short"].SetName("h_tagefficiency_short")
        hists_data["h_tagefficiency_short"].SetLineWidth(2)
        hists_data["h_tagefficiency_short"].Divide(hists_data["h_tracks_rereco_short"])
        
        hists_mc["h_tagefficiency_short"] = hists_mc["h_tracks_tagged_short"].Clone()
        hists_mc["h_tagefficiency_short"].SetName("h_tagefficiency_short")
        hists_mc["h_tagefficiency_short"].SetLineWidth(2)
        hists_mc["h_tagefficiency_short"].Divide(hists_mc["h_tracks_rereco_short"])
        
        hists_data["h_tagscalefactor_short"] = hists_data["h_tagefficiency_short"].Clone()
        hists_data["h_tagscalefactor_short"].SetName("h_tagscalefactor_short")
        hists_data["h_tagscalefactor_short"].SetLineWidth(2)
        hists_data["h_tagscalefactor_short"].Divide(hists_mc["h_tagefficiency_short"])
        
        hists_data["h_tagefficiency_long"] = hists_data["h_tracks_tagged_long"].Clone()
        hists_data["h_tagefficiency_long"].SetName("h_tagefficiency_long")
        hists_data["h_tagefficiency_long"].SetLineWidth(2)
        hists_data["h_tagefficiency_long"].Divide(hists_data["h_tracks_rereco_long"])
        
        hists_mc["h_tagefficiency_long"] = hists_mc["h_tracks_tagged_long"].Clone()
        hists_mc["h_tagefficiency_long"].SetName("h_tagefficiency_long")
        hists_mc["h_tagefficiency_long"].SetLineWidth(2)
        hists_mc["h_tagefficiency_long"].Divide(hists_mc["h_tracks_rereco_long"])
        
        hists_data["h_tagscalefactor_long"] = hists_data["h_tagefficiency_long"].Clone()
        hists_data["h_tagscalefactor_long"].SetName("h_tagscalefactor_long")
        hists_data["h_tagscalefactor_long"].SetLineWidth(2)
        hists_data["h_tagscalefactor_long"].Divide(hists_mc["h_tagefficiency_long"])
        
        # RECO SF:
        
        hists_data["h_recoefficiency"] = hists_data["h_tracks_reco"].Clone()
        hists_data["h_recoefficiency"].SetName("h_recoefficiency")
        hists_data["h_recoefficiency"].SetLineWidth(2)
        hists_data["h_recoefficiency"].Divide(hists_data["h_tracks_rereco"])
        
        hists_mc["h_recoefficiency"] = hists_mc["h_tracks_reco"].Clone()
        hists_mc["h_recoefficiency"].SetName("h_recoefficiency")
        hists_mc["h_recoefficiency"].SetLineWidth(2)
        hists_mc["h_recoefficiency"].Divide(hists_mc["h_tracks_rereco"])
        
        hists_data["h_recoscalefactor"] = hists_data["h_recoefficiency"].Clone()
        hists_data["h_recoscalefactor"].SetName("h_recoscalefactor")
        hists_data["h_recoscalefactor"].SetLineWidth(2)
        hists_data["h_recoscalefactor"].Divide(hists_mc["h_recoefficiency"])
        
        hists_data["h_scalefactor"] = hists_data["h_tagscalefactor"].Clone()
        hists_data["h_scalefactor"].SetName("h_scalefactor")
        hists_data["h_scalefactor"].SetLineWidth(2)
        hists_data["h_scalefactor"].Multiply(hists_data["h_recoefficiency"])
        
        hists_data["h_recoefficiency_short"] = hists_data["h_tracks_reco_short"].Clone()
        hists_data["h_recoefficiency_short"].SetName("h_recoefficiency_short")
        hists_data["h_recoefficiency_short"].SetLineWidth(2)
        hists_data["h_recoefficiency_short"].Divide(hists_data["h_tracks_rereco_short"])
        
        hists_mc["h_recoefficiency_short"] = hists_mc["h_tracks_reco_short"].Clone()
        hists_mc["h_recoefficiency_short"].SetName("h_recoefficiency_short")
        hists_mc["h_recoefficiency_short"].SetLineWidth(2)
        hists_mc["h_recoefficiency_short"].Divide(hists_mc["h_tracks_rereco_short"])
        
        hists_data["h_recoscalefactor_short"] = hists_data["h_recoefficiency_short"].Clone()
        hists_data["h_recoscalefactor_short"].SetName("h_recoscalefactor_short")
        hists_data["h_recoscalefactor_short"].SetLineWidth(2)
        hists_data["h_recoscalefactor_short"].Divide(hists_mc["h_recoefficiency_short"])
        
        hists_data["h_scalefactor_short"] = hists_data["h_tagscalefactor_short"].Clone()
        hists_data["h_scalefactor_short"].SetName("h_scalefactor_short")
        hists_data["h_scalefactor_short"].SetLineWidth(2)
        hists_data["h_scalefactor_short"].Multiply(hists_data["h_recoefficiency_short"])
        
        hists_data["h_recoefficiency_long"] = hists_data["h_tracks_reco_long"].Clone()
        hists_data["h_recoefficiency_long"].SetName("h_recoefficiency_long")
        hists_data["h_recoefficiency_long"].SetLineWidth(2)
        hists_data["h_recoefficiency_long"].Divide(hists_data["h_tracks_rereco_long"])
        
        hists_mc["h_recoefficiency_long"] = hists_mc["h_tracks_reco_long"].Clone()
        hists_mc["h_recoefficiency_long"].SetName("h_recoefficiency_long")
        hists_mc["h_recoefficiency_long"].SetLineWidth(2)
        hists_mc["h_recoefficiency_long"].Divide(hists_mc["h_tracks_rereco_long"])
        
        hists_data["h_recoscalefactor_long"] = hists_data["h_recoefficiency_long"].Clone()
        hists_data["h_recoscalefactor_long"].SetName("h_recoscalefactor_long")
        hists_data["h_recoscalefactor_long"].SetLineWidth(2)
        hists_data["h_recoscalefactor_long"].Divide(hists_mc["h_recoefficiency_long"])
        
        hists_data["h_scalefactor_long"] = hists_data["h_tagscalefactor_long"].Clone()
        hists_data["h_scalefactor_long"].SetName("h_scalefactor_long")
        hists_data["h_scalefactor_long"].SetLineWidth(2)
        hists_data["h_scalefactor_long"].Multiply(hists_data["h_recoefficiency_long"])
        
        # draw scale factor:
        canvas = shared_utils.mkcanvas()
        hists_data["h_recoscalefactor"].SetLineColor(kTeal) 
        hists_data["h_recoscalefactor"].Draw("hist e")
        hists_data["h_recoscalefactor"].GetXaxis().SetRangeUser(3,21)
        #hists_data["h_recoscalefactor"].SetYaxis().SetRangerUser(0,2)
        hists_data["h_tagscalefactor"].SetLineColor(kBlack)
        hists_data["h_tagscalefactor"].SetLineStyle(2)
        hists_data["h_tagscalefactor"].Draw("hist e same")
        hists_data["h_scalefactor"].SetLineColor(kBlack)
        hists_data["h_scalefactor"].Draw("hist e same")
        
        legend = shared_utils.mklegend(x1=0.3, y1=0.2, x2=0.6, y2=0.35)
        legend.AddEntry(hists_data["h_recoscalefactor"], "SF_{reco}")
        legend.AddEntry(hists_data["h_tagscalefactor"], "SF_{tagging}")
        legend.AddEntry(hists_data["h_scalefactor"], "SF_{reco} * SF_{tagging}")
        legend.Draw()
        
        #hists_data["h_scalefactor_rebinned"].SetLineColor(kRed)
        #hists_data["h_scalefactor_rebinned"].Draw("hist e same")
        
        #ErrorHistogram = hists_data["h_scalefactorg"].Clone('ErrorHistogram')
        #ErrorHistogram.SetFillStyle(3244)
        #ErrorHistogram.SetFillColor(kGray+1)
        #ErrorHistogram.Draw('e2 sames')
        
        hists_data["h_recoscalefactor"].SetTitle(";remaining layers;scale factor")
        hists_data["h_recoscalefactor"].GetYaxis().SetRangeUser(0,2.5)
        shared_utils.stamp()
        canvas.Print("plots%s/trackShortening_scalefactor%s.pdf" % (suffix, extralabel))
        
        # fit:    
        hists_data["h_scalefactor"].Draw("hist e")
        hists_data["h_scalefactor"].GetXaxis().SetRangeUser(3,21)
        hists_data["h_scalefactor"].GetYaxis().SetRangeUser(0,2)    
        hists_data["h_scalefactor"].SetTitle(";remaining layers;scale factor")
        
        g1 = TF1( 'g1', '[0]',  3,  4 )
        g2 = TF1( 'g2', '[0]+[1]*x',  4,  15 )
        hists_data["h_scalefactor"].Fit(g1, "", "same", 3, 4)
        g1.Draw("same E3")
        grint1 = hists_data["h_scalefactor"].Clone()
        TVirtualFitter.GetFitter().GetConfidenceIntervals(grint1)
        grint1.SetFillStyle(3244)
        grint1.SetFillColor(kGray+1)
        #grint1.Draw("e2 sames")
        
        hists_data["h_scalefactor"].Fit(g2, "", "same", 4, 15)    
        g2.Draw("same E3")
        grint2 = hists_data["h_scalefactor"].Clone()
        TVirtualFitter.GetFitter().GetConfidenceIntervals(grint2)
        grint2.SetFillStyle(3244)
        grint2.SetFillColor(kGray+1)
        grint2.Draw("e2 sames")
        
        shared_utils.stamp()
        canvas.Print("plots%s/trackShortening_scalefactor_fit%s.pdf" % (suffix, extralabel))
        
        
        
        # short/long:
            
        hists_data["h_scalefactor_short"].Draw("hist e")
        hists_data["h_scalefactor_short"].GetXaxis().SetRangeUser(3,21)
        hists_data["h_scalefactor_short"].GetYaxis().SetRangeUser(0,2)    
        hists_data["h_scalefactor_short"].SetTitle(";remaining layers;scale factor")
        
        g1 = TF1( 'g1', '[0]',  3,  15 )
        hists_data["h_scalefactor_short"].Fit(g1, "", "same", 3, 15)
        g1.Draw("same E3")
        grint1 = hists_data["h_scalefactor_short"].Clone()
        TVirtualFitter.GetFitter().GetConfidenceIntervals(grint1)
        grint1.SetFillStyle(3244)
        grint1.SetFillColor(kGray+1)
        
        shared_utils.stamp()
        canvas.Print("plots%s/trackShortening_scalefactor_fit_short%s.pdf" % (suffix, extralabel))
        
        hists_data["h_scalefactor_long"].Draw("hist e")
        hists_data["h_scalefactor_long"].GetXaxis().SetRangeUser(3,21)
        hists_data["h_scalefactor_long"].GetYaxis().SetRangeUser(0,2)    
        hists_data["h_scalefactor_long"].SetTitle(";remaining layers;scale factor")
        
        g1 = TF1( 'g1', '[0]',  3,  15 )
        hists_data["h_scalefactor_long"].Fit(g1, "", "same", 3, 15)
        g1.Draw("same E3")
        grint1 = hists_data["h_scalefactor_long"].Clone()
        TVirtualFitter.GetFitter().GetConfidenceIntervals(grint1)
        grint1.SetFillStyle(3244)
        grint1.SetFillColor(kGray+1)
        
        shared_utils.stamp()
        canvas.Print("plots%s/trackShortening_scalefactor_fit_long%s.pdf" % (suffix, extralabel))
    
    # draw pt:
    for variable in histolabels:
        if variable in ["h_muonPt", "h_muonEta", "h_muonPtCand", "h_muonEtaCand", "h_pfIso"] or "track_" in variable or "cutflow" in variable or "h_ptratio_layer" in variable:
            
            #if variable == "cutflow":
            #    canvas = shared_utils.mkcanvas_wide("cutflow")
            #else:            
            canvas = shared_utils.mkcanvas()
            canvas.SetLogy(True)
            hists_data[variable].SetMarkerStyle(20)
            hists_data[variable].Draw("p")
            hists_mc[variable].Draw("hist e same")
            if "cutflow" not in variable:
                if hists_data[variable].Integral():
                    hists_data[variable].Scale(1.0/hists_data[variable].Integral())
                if hists_mc[variable].Integral():
                    hists_mc[variable].Scale(1.0/hists_mc[variable].Integral())
            else:
                hists_data[variable].Scale(1.0/hists_data[variable].GetBinContent(1))
                hists_mc[variable].Scale(1.0/hists_mc[variable].GetBinContent(1))
                
            hists_data[variable].GetYaxis().SetRangeUser(1e-4,1e1)
            
            vartext = variable.replace("h_muonPtCand", "p_{T}^{#mu} (GeV)")
            vartext = vartext.replace("h_muonEtaCand", "|#eta|")
            vartext = variable.replace("h_muonPt", "p_{T}^{#mu} (GeV)")
            vartext = vartext.replace("h_muonEta", "|#eta|")
            vartext = vartext.replace("track_is_pixel_track", "pixel track")              
            vartext = vartext.replace("track_dxyVtx", "dxy (cm)")                      
            vartext = vartext.replace("track_dzVtx", "dz (cm)")                       
            vartext = vartext.replace("track_trkRelIso", "track relative isolation")                   
            vartext = vartext.replace("track_nValidPixelHits", "pixel hits")             
            vartext = vartext.replace("track_nValidTrackerHits", "tracker hits")           
            vartext = vartext.replace("track_trackerLayersWithMeasurement", "tracker layers with measurement")
            vartext = vartext.replace("track_ptErrOverPt2", "#Delta p_{T} / p_{T}^{2} (1/GeV)")                
            vartext = vartext.replace("track_chi2perNdof", "#chi^{2}/ndof")                 
            vartext = vartext.replace("track_mva", "BDT score")                         
            vartext = vartext.replace("track_pt", "p_{T}^{track} (GeV)")                          
            vartext = vartext.replace("track_trackQualityHighPurity", "high-purity track")      
            vartext = vartext.replace("track_nMissingInnerHits", "missing inner hits")           
            vartext = vartext.replace("track_passPFCandVeto", "pass PF cand. veto")              
            vartext = vartext.replace("track_nMissingOuterHits", "missing outer hits")           
            vartext = vartext.replace("track_matchedCaloEnergy", "E_{dep} (GeV)")           
            vartext = vartext.replace("track_p", "p^{track} (GeV)")     
            vartext = vartext.replace("h_pfIso", "(#Sigma p_{T}^{PF cand}) / p_{T}^{#mu}")                 
            vartext = vartext.split("_layer")[0]
            
            if "h_ptratio_layer" in variable:   
                vartext = "p_{T}^{shortened track} / p_{T}^{#mu-matched track}"
            
            if "track_" in variable:
                hists_data[variable].SetTitle(";%s;normalized number of tracks" % vartext)
            else:
                hists_data[variable].SetTitle(";%s;normalized number of events" % vartext)
            
            if "track_" in variable or "h_muonPt" in variable or "h_pfIso" in variable:
                legend = shared_utils.mklegend(x1=0.55, y1=0.7, x2=0.9, y2=0.9)
                legend.AddEntry(hists_data[variable], "SingleMuon Data")
                legend.AddEntry(hists_mc[variable], "DYJetsToLL MC")
                if "_layer" in variable:
                    legend.SetHeader("%s layers" % variable.split("_layer")[-1])
                legend.Draw()
            
            # if track variable, let's include the signal too!
            if "track_" in variable:
                folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_64_p15OptionalJetVeto_merged"
                input_files = glob.glob(folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq*root")
                base_cut = "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975 && tracks_nMissingMiddleHits==0"
                
                if "_layer" in variable:
                    base_cut += " && tracks_trackerLayersWithMeasurement==%s" % variable.split("_layer")[-1]
                    h_signal = plotting.get_histogram_from_file(input_files, "Events", variable.split("_layer")[0].replace("track_", "tracks_"), cutstring=base_cut, nBinsX=hists_data[variable].GetNbinsX(), xmin=hists_data[variable].GetXaxis().GetXmin(), xmax=hists_data[variable].GetXaxis().GetXmax())
                else:
                    h_signal = plotting.get_histogram_from_file(input_files, "Events", variable.replace("track_", "tracks_"), cutstring=base_cut, nBinsX=hists_data[variable].GetNbinsX(), xmin=hists_data[variable].GetXaxis().GetXmin(), xmax=hists_data[variable].GetXaxis().GetXmax())
                            
                # alright, all set
                shared_utils.histoStyler(h_signal)
                h_signal.SetLineWidth(2)
                h_signal.SetLineColor(kBlue)
                if h_signal.Integral()>0:
                    h_signal.Scale(1.0/h_signal.Integral())
                h_signal.Draw("hist e same")
                legend.AddEntry(h_signal, "Signal")
                
                # get mean
                if "track_chi2perNdof" in variable:
                    data_mean = hists_data[variable].GetMean()
                    mc_mean = hists_mc[variable].GetMean()
                    latex = TLatex()
                    latex.SetTextSize(0.04)
                    latex.SetNDC(True)
                    latex.SetTextAlign(13)
                    latex.DrawLatex(.4,.3,"<#chi^{2}/ndof>_{Data}=%.2f" % data_mean)
                    latex.DrawLatex(.4,.25,"<#chi^{2}/ndof>_{MC}=%.2f" % mc_mean)
                
            shared_utils.stamp()
                
            if "h_ptratio_layer" in variable:
                legend = shared_utils.mklegend(x1=0.5, y1=0.7, x2=0.9, y2=0.9)
                legend.AddEntry(hists_data[variable], "SingleMuon Data")
                legend.AddEntry(hists_mc[variable], "DYJetsToLL MC")
                legend.SetHeader("target track length: %s layers" % variable.split("h_ptratio_layer")[-1])
                legend.Draw()
                
                
            if variable == "h_pfIso":
                
                cutline = TLine(0.2,1e-4,0.2,1e1)
                cutline.SetLineColor(kRed)
                cutline.SetLineWidth(2)
                cutline.Draw("same")
                hists_data[variable].GetYaxis().SetRangeUser(1e-4,1e1)
            
            if variable == "cutflow":
                
                legend = shared_utils.mklegend(x1=0.55, y1=0.2, x2=0.9, y2=0.4)
                legend.AddEntry(hists_data[variable], "SingleMuon Data")
                legend.AddEntry(hists_mc[variable], "DYJetsToLL MC")
                legend.Draw()
                
            	hists_data[variable].GetXaxis().SetTitleSize(0.04)
            	hists_data[variable].GetXaxis().SetLabelSize(0.04)   
                
                
                canvas.SetLogy(False)
                
                binlabels = {
                              0: "#mu-matched tracks",
                              1: "pt>15 (40) GeV",
                              2: "high purity",
                              3: "|eta|<2.4",
                              4: "#Delta p_{T}/p_{T}^{2}<10/GeV",
                              5: "dz<0.1 cm",
                              6: "relIso<0.2",
                              7: "tracker layer #geq2",
                              8: "tracker hits #geq2",
                              9: "no miss. inner hits",
                              10: "pixel hits #geq2",
                              11: "PF cand. veto",
                              12: "missing outer hits",
                              13: "BDT> 0 (0.05)",
                              14: "E_{dep}/p<0.2",
                }

                for i in binlabels:
                    hists_data[variable].GetXaxis().SetBinLabel(i + 1, binlabels[i]);
                    hists_mc[variable].GetXaxis().SetBinLabel(i + 1, binlabels[i]);
            
                hists_data[variable].GetXaxis().SetRangeUser(0,16)
                hists_data[variable].GetYaxis().SetRangeUser(0,1)
                hists_data[variable].SetTitle(";;fraction of remaining shortened tracks")
            
            canvas.Print("plots%s/trackShortening_%s%s.pdf" % (suffix, variable.replace("h_", ""), extralabel))


def doplots(periods = ["Summer16", "Fall17", "Run2016H", "Run2016B", "Run2017B", "Run2017F"], suffixes = ["", "low", "medium", "high"]):        

    periods = [
                "Summer16",
                "Fall17",
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
                #"Run2018A",
                #"Run2018B",
                #"Run2018C",
                #"Run2018D",
                #"Run2017CUL",
              ]
              
    suffixes = [
                 "",
                 #"low",
                 #"medium",
                 #"high",
               ]
    
    allperiods()
                   
    for suffix in suffixes:
        for period in periods: 
            plot(period, suffix)
    
        #scalefactors("Run2016B", "Summer16", suffix, "_2016B")
        #scalefactors("Run2016C", "Summer16", suffix, "_2016C")
        #scalefactors("Run2016D", "Summer16", suffix, "_2016D")
        #scalefactors("Run2016E", "Summer16", suffix, "_2016E")
        #scalefactors("Run2016F", "Summer16", suffix, "_2016F")
        #scalefactors("Run2016G", "Summer16", suffix, "_2016G")
        #scalefactors("Run2016H", "Summer16", suffix, "_2016H")
        #scalefactors("Run2017B", "Fall17", suffix, "_2017B")
        #scalefactors("Run2017C", "Fall17", suffix, "_2017C")
        #scalefactors("Run2017D", "Fall17", suffix, "_2017D")
        #scalefactors("Run2017E", "Fall17", suffix, "_2017E")
        #scalefactors("Run2017F", "Fall17", suffix, "_2017F")
        #scalefactors("Run2018A", "Fall17", suffix, "_2018A")
        #scalefactors("Run2018B", "Fall17", suffix, "_2018B")
        #scalefactors("Run2018C", "Fall17", suffix, "_2018C")
        #scalefactors("Run2018D", "Fall17", suffix, "_2018D")

    
if __name__ == "__main__":

    doplots()