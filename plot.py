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

def update_uncertainties_from_teff(ratiohisto, numerator, denominator):
    
    tempteff = TEfficiency(numerator.Clone(), denominator.Clone())
    tempteff.SetStatisticOption(TEfficiency.kFCP)
    for i in range(ratiohisto.GetNbinsX()):
        uncertainty_from_teff = math.sqrt(tempteff.GetEfficiencyErrorLow(i)**2 + tempteff.GetEfficiencyErrorUp(i)**2)
        ratiohisto.SetBinError(i, uncertainty_from_teff)
        
    return ratiohisto


def draw_2D_plots(hists, period, suffix, histolabels):

    # draw other plots:
    for label in histolabels:
        if label in ["h_layers2D", "h_shortbdt2D", "h_longbdt2D", "h_ptratio2D", "h_chi2ndof2D"]:
            canvas = shared_utils.mkcanvas()
            hists[label].Draw("colz")
            canvas.SetRightMargin(.18)
            size = 0.059
            font = 132
            if hists[label].Integral():
                hists[label].Scale(1.0/hists[label].Integral())
            hists[label].GetZaxis().SetLabelFont(font)
            hists[label].GetZaxis().SetTitleFont(font)
            hists[label].GetZaxis().SetTitleSize(size)
            hists[label].GetZaxis().SetLabelSize(size)
            hists[label].GetZaxis().SetTitleOffset(1.0)
                            
            shared_utils.stamp()
            canvas.SaveAs("plots%s/%s_%s.pdf" % (suffix, label.replace("h_", ""), period))  


def plotdatamc(dataperiod, suffix, extralabel, histolabels, muon_plots = False, category = ""):
    
    if "Run2016" in period:
        mcperiod = "Summer16"
    elif "Run2017" in period:
        mcperiod = "Fall17"
    elif "RunUL2017C" in period:
        mcperiod = "Fall17"
    elif "Run2018" in period:
        mcperiod = "Autumn18"
    
    if muon_plots:
        dataperiod += "_1"
        mcperiod += "_1"
    
    # get histos:
    hists_data = {}
    hists_mc = {}
    for label in histolabels:
        fin = TFile("histograms/histograms%s_%s.root" % (suffix, dataperiod), "open")
        hists_data[label] = fin.Get(label + category)
        hists_data[label].SetDirectory(0)
        hists_data[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_data[label])
        fin.Close()
        
        fin = TFile("histograms/histograms%s_%s.root" % (suffix, mcperiod), "open")
        hists_mc[label] = fin.Get(label + category)
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
        
        hists_data["h_recoefficiency"] = hists_data["h_tracks_rereco"].Clone()
        hists_data["h_recoefficiency"].SetName("h_recoefficiency")
        hists_data["h_recoefficiency"].SetLineWidth(2)
        hists_data["h_recoefficiency"].Divide(hists_data["h_tracks_reco"])
        
        hists_mc["h_recoefficiency"] = hists_mc["h_tracks_rereco"].Clone()
        hists_mc["h_recoefficiency"].SetName("h_recoefficiency")
        hists_mc["h_recoefficiency"].SetLineWidth(2)
        hists_mc["h_recoefficiency"].Divide(hists_mc["h_tracks_reco"])
        
        hists_data["h_recoscalefactor"] = hists_data["h_recoefficiency"].Clone()
        hists_data["h_recoscalefactor"].SetName("h_recoscalefactor")
        hists_data["h_recoscalefactor"].SetLineWidth(2)
        hists_data["h_recoscalefactor"].Divide(hists_mc["h_recoefficiency"])
        
        hists_data["h_scalefactor"] = hists_data["h_tagscalefactor"].Clone()
        hists_data["h_scalefactor"].SetName("h_scalefactor")
        hists_data["h_scalefactor"].SetLineWidth(2)
        hists_data["h_scalefactor"].Multiply(hists_data["h_recoscalefactor"])
        
        hists_data["h_recoefficiency_short"] = hists_data["h_tracks_rereco_short"].Clone()
        hists_data["h_recoefficiency_short"].SetName("h_recoefficiency_short")
        hists_data["h_recoefficiency_short"].SetLineWidth(2)
        hists_data["h_recoefficiency_short"].Divide(hists_data["h_tracks_reco_short"])
        
        hists_mc["h_recoefficiency_short"] = hists_mc["h_tracks_rereco_short"].Clone()
        hists_mc["h_recoefficiency_short"].SetName("h_recoefficiency_short")
        hists_mc["h_recoefficiency_short"].SetLineWidth(2)
        hists_mc["h_recoefficiency_short"].Divide(hists_mc["h_tracks_reco_short"])
        
        hists_data["h_recoscalefactor_short"] = hists_data["h_recoefficiency_short"].Clone()
        hists_data["h_recoscalefactor_short"].SetName("h_recoscalefactor_short")
        hists_data["h_recoscalefactor_short"].SetLineWidth(2)
        hists_data["h_recoscalefactor_short"].Divide(hists_mc["h_recoefficiency_short"])
        
        hists_data["h_scalefactor_short"] = hists_data["h_tagscalefactor_short"].Clone()
        hists_data["h_scalefactor_short"].SetName("h_scalefactor_short")
        hists_data["h_scalefactor_short"].SetLineWidth(2)
        hists_data["h_scalefactor_short"].Multiply(hists_data["h_recoscalefactor_short"])
        
        hists_data["h_recoefficiency_long"] = hists_data["h_tracks_rereco_long"].Clone()
        hists_data["h_recoefficiency_long"].SetName("h_recoefficiency_long")
        hists_data["h_recoefficiency_long"].SetLineWidth(2)
        hists_data["h_recoefficiency_long"].Divide(hists_data["h_tracks_reco_long"])
        
        hists_mc["h_recoefficiency_long"] = hists_mc["h_tracks_rereco_long"].Clone()
        hists_mc["h_recoefficiency_long"].SetName("h_recoefficiency_long")
        hists_mc["h_recoefficiency_long"].SetLineWidth(2)
        hists_mc["h_recoefficiency_long"].Divide(hists_mc["h_tracks_reco_long"])
        
        hists_data["h_recoscalefactor_long"] = hists_data["h_recoefficiency_long"].Clone()
        hists_data["h_recoscalefactor_long"].SetName("h_recoscalefactor_long")
        hists_data["h_recoscalefactor_long"].SetLineWidth(2)
        hists_data["h_recoscalefactor_long"].Divide(hists_mc["h_recoefficiency_long"])
        
        hists_data["h_scalefactor_long"] = hists_data["h_tagscalefactor_long"].Clone()
        hists_data["h_scalefactor_long"].SetName("h_scalefactor_long")
        hists_data["h_scalefactor_long"].SetLineWidth(2)
        hists_data["h_scalefactor_long"].Multiply(hists_data["h_recoscalefactor_long"])
        
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
        canvas.SaveAs("plots%s/scalefactor%s%s.pdf" % (suffix, extralabel, category))
        
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
        canvas.SaveAs("plots%s/scalefactor_fit%s%s.pdf" % (suffix, extralabel, category))
        
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
        canvas.SaveAs("plots%s/scalefactor_fit_short%s.pdf" % (suffix, extralabel))
        
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
        canvas.SaveAs("plots%s/scalefactor_fit_long%s.pdf" % (suffix, extralabel))
    
    # draw pt:
    for variable in histolabels:
        if variable in ["h_muonPt", "h_muonEta", "h_muonPtCand", "h_muonEtaCand", "h_pfIso"] or "track_" in variable or "cutflow" in variable or "h_ptratio_layer" in variable or "h_tracks_algo" in variable:
            
            if muon_plots and "h_muon" not in variable:
                continue
            if not muon_plots and "h_muon" in variable:
                continue
            
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
            vartext = vartext.replace("h_tracks_algo", "track reconstruction algorithm")                 
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
                folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_66_noEdep_all_merged"
                input_files = glob.glob(folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq*root")
                base_cut = "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975 && tracks_nMissingMiddleHits==0 && abs(tracks_eta)<2.2 "
                                
                # insert signal pt and eta cuts:
                if "low" in suffix:
                    base_cut += " tracks_pt>15 && tracks_pt<40 "
                elif "medium" in suffix:
                    base_cut += " tracks_pt>40 && tracks_pt<70 "
                elif "high" in suffix:
                    base_cut += " tracks_pt>70 "
                if "Barrel" in suffix:
                    base_cut += " abs(tracks_eta)<1.479 "
                elif "Endcap" in suffix:
                    base_cut += " abs(tracks_eta)>1.479 "
                
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
            
            canvas.SaveAs("plots%s/%s%s%s.pdf" % (suffix, variable.replace("h_", ""), extralabel, category))



def allperiods(suffix, use_uncertainty_from_teff = False, lumi_weighting = 1):
        
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
                #"RunUL2017C",
              ]
    
    histolabels = [
                    "h_tracks_reco",                     
                    "h_tracks_rereco",                   
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
                    "h_tracks_algo",                           
                    #"track_is_pixel_track",              
                    #"track_dxyVtx",                      
                    #"track_dzVtx",                                     
                    #"track_trkRelIso",                   
                    #"track_nValidPixelHits",             
                    #"track_nValidTrackerHits",           
                    #"track_trackerLayersWithMeasurement",
                    #"track_ptErrOverPt2",                
                    "track_chi2perNdof",                 
                    #"track_mva",                         
                    "track_pt",                          
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
      
    # dicts to save the fit results:    
    fitresults = {}
    fitresults["fit_sf"] = {}
    fitresults["fit_uncert"] = {}
    fitresults["fit_sf_lumi"] = {}
    fitresults["fit_uncert_lumi"] = {}
    fitresults["fit_sf_lumisam"] = {}
    fitresults["fit_uncert_lumisam"] = {}
        
    for extra in [
                  "",
                  "_short",
                  "_long"
                 ]:    
                    
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
    
            #if extra == "":
            #    draw_2D_plots(hists[period], period, suffix, histolabels)
            #    plotdatamc(period, suffix, "_%s" % period.replace("Run", ""), histolabels)
            
            if "Run" not in period:
                continue
            
            if "Run2016" in period:
                mcperiod = "Summer16"
            elif "Run2017" in period:
                mcperiod = "Fall17"
            elif "Run2018" in period:
                mcperiod = "Autumn18"
            elif "RunUL2017C" in period:
                mcperiod = "Fall17"            
            
            print period
            
            # draw abs values:
            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
            legend.SetHeader(period)
            legend.SetTextSize(0.035)
            hists[period]["h_tracks_reco" + extra].Draw("hist e")
            hists[period]["h_tracks_reco" + extra].SetTitle(";remaining layers;tracks")
            #hists[period]["h_tracks_reco"].GetXaxis().SetRangeUser(0,11)
            hists[period]["h_tracks_rereco" + extra].Draw("hist e same")
            hists[period]["h_tracks_rereco" + extra].SetLineStyle(2)
            hists[period]["h_tracks_tagged" + extra].Draw("same hist e")
            hists[period]["h_tracks_tagged" + extra].SetLineStyle(2)
            hists[period]["h_tracks_tagged" + extra].SetLineColor(kRed)
            legend.AddEntry(hists[period]["h_tracks_reco" + extra], "tracks matched to muons")
            legend.AddEntry(hists[period]["h_tracks_rereco" + extra], "shortenend tracks")
            legend.AddEntry(hists[period]["h_tracks_tagged" + extra], "shortenend & tagged tracks")
            shared_utils.stamp()
            legend.Draw()
            canvas.SaveAs("plots%s/absval_%s%s.pdf" % (suffix, period, extra))  
            hists[period]["h_tracks_rereco" + extra].SetLineStyle(1)
            hists[period]["h_tracks_tagged" + extra].SetLineStyle(1)
            
            # tagging:
            
            hists[period]["h_tagefficiency"] = hists[period]["h_tracks_tagged" + extra].Clone()
            hists[period]["h_tagefficiency"].SetName("h_tagefficiency")
            hists[period]["h_tagefficiency"].SetLineWidth(2)
            hists[period]["h_tagefficiency"].Divide(hists[period]["h_tracks_rereco" + extra])
                    
            hists[mcperiod]["h_tagefficiency"] = hists[mcperiod]["h_tracks_tagged" + extra].Clone()
            hists[mcperiod]["h_tagefficiency"].SetName("h_tagefficiency")
            hists[mcperiod]["h_tagefficiency"].SetLineWidth(2)
            hists[mcperiod]["h_tagefficiency"].Divide(hists[mcperiod]["h_tracks_rereco" + extra])
            
            if use_uncertainty_from_teff:
                # update errors from TEfficiency:
                hists[period]["h_tagtefficiency"] = TEfficiency(hists[period]["h_tracks_tagged" + extra].Clone(), hists[period]["h_tracks_rereco" + extra].Clone())
                hists[period]["h_tagtefficiency"].SetStatisticOption(TEfficiency.kFCP)        
                hists[mcperiod]["h_tagtefficiency"] = TEfficiency(hists[mcperiod]["h_tracks_tagged" + extra].Clone(), hists[mcperiod]["h_tracks_rereco" + extra].Clone())
                hists[mcperiod]["h_tagtefficiency"].SetStatisticOption(TEfficiency.kFCP)        
                
                for i_period in [period, mcperiod]:
                    
                    canvas = shared_utils.mkcanvas()
                    hists[i_period]["h_tagefficiency"].Draw()
                    hists[i_period]["h_tagefficiency"].GetYaxis().SetRangeUser(0,1)
                    canvas.SaveAs("h_tagefficiency_%s.pdf" % i_period)
                    hists[i_period]["h_tagtefficiency"].SetLineColor(kTeal)
                    hists[i_period]["h_tagtefficiency"].Draw("same")
                    canvas.SaveAs("h_tagefficiency_%s.pdf" % i_period)
                    
                    for i in range(hists[i_period]["h_tagefficiency"].GetNbinsX()):
                                            
                        #print hists[i_period]["h_tagefficiency"].GetBinContent(i), hists[i_period]["h_tagtefficiency"].GetEfficiency(i)
                        #print hists[i_period]["h_tagefficiency"].GetBinError(i), hists[i_period]["h_tagtefficiency"].GetEfficiencyErrorLow(i), hists[i_period]["h_tagtefficiency"].GetEfficiencyErrorUp(i)
                        uncertainty_from_teff = math.sqrt(hists[i_period]["h_tagtefficiency"].GetEfficiencyErrorLow(i)**2 + hists[i_period]["h_tagtefficiency"].GetEfficiencyErrorUp(i)**2)
                        print "was", hists[i_period]["h_tagefficiency"].GetBinError(i), "now", uncertainty_from_teff
                                            
                        hists[i_period]["h_tagefficiency"].SetBinError(i, uncertainty_from_teff)
                        
                    canvas = shared_utils.mkcanvas()
                    hists[i_period]["h_tagefficiency"].Draw()
                    hists[i_period]["h_tagefficiency"].GetYaxis().SetRangeUser(0,1)
                    hists[i_period]["h_tagtefficiency"].SetLineColor(kTeal)
                    hists[i_period]["h_tagtefficiency"].Draw("same")
                    canvas.SaveAs("h_tagefficiency_%s_corrected.pdf" % i_period)
            
            hists[period]["h_tagscalefactor"] = hists[period]["h_tagefficiency"].Clone()
            hists[period]["h_tagscalefactor"].SetName("h_tagscalefactor")
            hists[period]["h_tagscalefactor"].SetLineWidth(2)
            hists[period]["h_tagscalefactor"].Divide(hists[mcperiod]["h_tagefficiency"])
            
            # reconstruction:
            
            hists[period]["h_recoefficiency"] = hists[period]["h_tracks_rereco" + extra].Clone()
            hists[period]["h_recoefficiency"].SetName("h_recoefficiency")
            hists[period]["h_recoefficiency"].SetLineWidth(2)
            hists[period]["h_recoefficiency"].Divide(hists[period]["h_tracks_reco"])
            
            hists[mcperiod]["h_recoefficiency"] = hists[mcperiod]["h_tracks_rereco" + extra].Clone()
            hists[mcperiod]["h_recoefficiency"].SetName("h_recoefficiency")
            hists[mcperiod]["h_recoefficiency"].SetLineWidth(2)
            hists[mcperiod]["h_recoefficiency"].Divide(hists[mcperiod]["h_tracks_reco"])
            
            if use_uncertainty_from_teff:
                # update errors from TEfficiency:
                hists[period]["h_recotefficiency"] = TEfficiency(hists[period]["h_tracks_rereco" + extra].Clone(), hists[period]["h_tracks_reco" + extra].Clone())
                hists[period]["h_recotefficiency"].SetStatisticOption(TEfficiency.kFCP)        
                hists[mcperiod]["h_recotefficiency"] = TEfficiency(hists[mcperiod]["h_tracks_rereco" + extra].Clone(), hists[mcperiod]["h_tracks_reco" + extra].Clone())
                hists[mcperiod]["h_recotefficiency"].SetStatisticOption(TEfficiency.kFCP)        
                
                for i_period in [period, mcperiod]:
                    
                    canvas = shared_utils.mkcanvas()
                    hists[i_period]["h_recoefficiency"].Draw()
                    hists[i_period]["h_recoefficiency"].GetYaxis().SetRangeUser(0,2)
                    canvas.SaveAs("h_recoefficiency_%s.pdf" % i_period)
                    hists[i_period]["h_recotefficiency"].SetLineColor(kTeal)
                    hists[i_period]["h_recotefficiency"].Draw("same")
                    canvas.SaveAs("h_recoefficiency_%s.pdf" % i_period)
                    
                    for i in range(hists[i_period]["h_recoefficiency"].GetNbinsX()):
                                            
                        #print hists[i_period]["h_recoefficiency"].GetBinContent(i), hists[i_period]["h_recotefficiency"].GetEfficiency(i)
                        #print hists[i_period]["h_recoefficiency"].GetBinError(i), hists[i_period]["h_recotefficiency"].GetEfficiencyErrorLow(i), hists[i_period]["h_recotefficiency"].GetEfficiencyErrorUp(i)
                        uncertainty_from_teff = math.sqrt(hists[i_period]["h_recotefficiency"].GetEfficiencyErrorLow(i)**2 + hists[i_period]["h_recotefficiency"].GetEfficiencyErrorUp(i)**2)
                        print "was", hists[i_period]["h_recoefficiency"].GetBinError(i), "now", uncertainty_from_teff
                                            
                        hists[i_period]["h_recoefficiency"].SetBinError(i, uncertainty_from_teff)
                        
                    canvas = shared_utils.mkcanvas()
                    hists[i_period]["h_recoefficiency"].Draw()
                    hists[i_period]["h_recoefficiency"].GetYaxis().SetRangeUser(0,2)
                    hists[i_period]["h_recotefficiency"].SetLineColor(kTeal)
                    hists[i_period]["h_recotefficiency"].Draw("same")
                    canvas.SaveAs("h_recoefficiency_%s_corrected.pdf" % i_period)
            
            hists[period]["h_recoscalefactor"] = hists[period]["h_recoefficiency"].Clone()
            hists[period]["h_recoscalefactor"].SetName("h_recoscalefactor")
            hists[period]["h_recoscalefactor"].SetLineWidth(2)
            hists[period]["h_recoscalefactor"].Divide(hists[mcperiod]["h_recoefficiency"])
                        
            # draw efficiency:
            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
            legend.SetHeader(period)
            legend.SetTextSize(0.04)
            hists[period]["h_recoefficiency"].Draw("hist e")
            hists[period]["h_tagefficiency"].SetLineColor(kRed)
            hists[period]["h_tagefficiency"].Draw("hist e same")
            legend.AddEntry(hists[period]["h_recoefficiency"], "reconstruction efficiency")
            legend.AddEntry(hists[period]["h_tagefficiency"], "tagging efficiency")
            hists[period]["h_recoefficiency"].SetTitle(";remaining layers;efficiency")
            #hists[period]["h_efficiency"].GetXaxis().SetRangeUser(0,11)
            hists[period]["h_recoefficiency"].GetYaxis().SetRangeUser(0,1)
            shared_utils.stamp()
            legend.Draw()
            canvas.SaveAs("plots%s/efficiency_%s.pdf" % (suffix, period))  
            
            
            # global scale factor
            
            #hists[period]["h_scalefactor"] = hists[period]["h_tagscalefactor"].Clone()
            #hists[period]["h_scalefactor"].SetName("h_scalefactor")
            #hists[period]["h_scalefactor"].SetLineWidth(2)
            #hists[period]["h_scalefactor"].Multiply(hists[period]["h_recoscalefactor"])
            
            numerator = hists[period]["h_tracks_tagged" + extra].Clone()
            denominator = hists[period]["h_tracks_rereco"].Clone()

            #if lumi_weighting:
                    #numerator.Scale(official_lumis[period]/numerator.Integral())
                    #denominator.Scale(official_lumis[period]/denominator.Integral())
    
            hists[period]["h_finaleff"] = numerator.Clone()
            hists[period]["h_finaleff"].SetName("h_finaleff")
            hists[period]["h_finaleff"].SetLineWidth(2)
            hists[period]["h_finaleff"].Divide(denominator)
            hists[period]["h_finaleff"] = update_uncertainties_from_teff(hists[period]["h_finaleff"], numerator, denominator)
            
            hists[mcperiod]["h_finaleff"] = hists[mcperiod]["h_tracks_tagged" + extra].Clone()
            hists[mcperiod]["h_finaleff"].SetName("h_finaleff")
            hists[mcperiod]["h_finaleff"].SetLineWidth(2)
            hists[mcperiod]["h_finaleff"].Divide(hists[mcperiod]["h_tracks_rereco"])
            hists[mcperiod]["h_finaleff"] = update_uncertainties_from_teff(hists[mcperiod]["h_finaleff"], hists[mcperiod]["h_tracks_tagged" + extra], hists[mcperiod]["h_tracks_rereco"])
            
            hists[period]["h_scalefactor"] = hists[period]["h_finaleff"].Clone()
            hists[period]["h_scalefactor"].SetName("h_scalefactor")
            hists[period]["h_scalefactor"].SetLineWidth(2)
            hists[period]["h_scalefactor"].Divide(hists[mcperiod]["h_finaleff"])
            
            # fit:
            
            g1 = TF1( 'g1', '[0]',  0,  20 )
            fit = hists[period]["h_scalefactor"].Fit(g1, "", "same", 0, 20)
            
            fitresults["fit_sf"][period + extra] = g1.GetParameter(0)
            fitresults["fit_uncert"][period + extra] = g1.GetParError(0)
        
        
        official_lumis = {
            "Run2016B": 5.8,
            "Run2016C": 2.6,
            "Run2016D": 4.2,
            "Run2016E": 4.0,
            "Run2016F": 3.1,
            "Run2016G": 7.5,
            "Run2016H": 8.6,
            "Run2017B": 4.8,
            "Run2017C": 9.7,
            "Run2017D": 4.3 ,
            "Run2017E": 9.3,
            "Run2017F": 13.5,
            "Run2018A": 14,
            "Run2018B": 7.1 ,
            "Run2018C": 6.94 ,
            "Run2018D": 31.93,
        }
        
        
        # lumiweighted approach #1, weighted mean:
                        
        for year in ["2016", "2017", "2018"]:  
        
            if "2016" in year:
                mcperiod = "Summer16"
            elif "2017" in year:
                mcperiod = "Fall17"
            elif "2018" in year:
                mcperiod = "Autumn18"
                
            for period in periods:
                                
                if year in period:
                    
                    numerator = hists[period]["h_tracks_tagged" + extra].Clone()
                    denominator = hists[period]["h_tracks_rereco"].Clone()
                    
                    hists[period]["h_finaleff"] = numerator
                    hists[period]["h_finaleff"].SetName("h_finaleff")
                    hists[period]["h_finaleff"].SetLineWidth(2)
                    hists[period]["h_finaleff"].Divide(denominator)
                    hists[period]["h_finaleff"] = update_uncertainties_from_teff(hists[period]["h_finaleff"], numerator, denominator)
                    
                    hists[mcperiod]["h_finaleff"] = hists[mcperiod]["h_tracks_tagged" + extra].Clone()
                    hists[mcperiod]["h_finaleff"].SetName("h_finaleff")
                    hists[mcperiod]["h_finaleff"].SetLineWidth(2)
                    hists[mcperiod]["h_finaleff"].Divide(hists[mcperiod]["h_tracks_rereco"])
                    hists[mcperiod]["h_finaleff"] = update_uncertainties_from_teff(hists[mcperiod]["h_finaleff"], hists[mcperiod]["h_tracks_tagged" + extra], hists[mcperiod]["h_tracks_rereco"])
                    
                    hists[period]["h_scalefactor"] = hists[period]["h_finaleff"].Clone()
                    hists[period]["h_scalefactor"].SetName("h_scalefactor")
                    hists[period]["h_scalefactor"].SetLineWidth(2)
                    hists[period]["h_scalefactor"].Divide(hists[mcperiod]["h_finaleff"])
                    
                    # fit:
                    
                    g1 = TF1( 'g1', '[0]',  0,  20 )
                    fit = hists[period]["h_scalefactor"].Fit(g1, "Q", "same", 0, 20)
                         
                    # draw fit:
                    canvas = shared_utils.mkcanvas()
                    shared_utils.histoStyler(hists[period]["h_scalefactor"])
                    hists[period]["h_scalefactor"].Draw("hist e")
                    hists[period]["h_scalefactor"].GetYaxis().SetRangeUser(0,2)
                    g1.SetLineWidth(2)
                    g1.Draw("same e")
                    canvas.Print("plots/fit_sf1_%s%s.pdf" % (year, extra))
                                        
                    # lumi-weighting:
                    
                    if year == "2016":
                        total_lumi = 35.9
                    if year == "2017":
                        total_lumi = 41.5
                    if year == "2018":
                        total_lumi = 59.7

                    if year + extra not in fitresults["fit_sf_lumi"]:
                        fitresults["fit_sf_lumi"][year + extra] = 0
                        fitresults["fit_uncert_lumi"][year + extra] = 0
                    fitresults["fit_sf_lumi"][year + extra] += g1.GetParameter(0) * official_lumis[period] / total_lumi
                    fitresults["fit_uncert_lumi"][year + extra] += (g1.GetParError(0) * official_lumis[period] / total_lumi)**2
                            
                        
            # take square root of uncertainty to finalize adding in quadrature:
            fitresults["fit_uncert_lumi"][year + extra] = math.sqrt(fitresults["fit_uncert_lumi"][year + extra])
            
            
        # lumiweighted approach #2, Sam:    
                        
        for year in ["2016", "2017", "2018"]:  
        
            if "Run2016" in period:
                mcperiod = "Summer16"
            elif "Run2017" in period:
                mcperiod = "Fall17"
            elif "Run2018" in period:
                mcperiod = "Autumn18"
        
            numerators = {}
            denominators = {}
        
            for i_period in periods:
                if year in i_period:                    
                    numerators[i_period] = hists[i_period]["h_tracks_tagged" + extra].Clone()
                    denominators[i_period] = hists[i_period]["h_tracks_rereco"].Clone()
                    numerators[i_period].Scale(official_lumis[i_period]/numerators[i_period].Integral())
                    denominators[i_period].Scale(official_lumis[i_period]/denominators[i_period].Integral())
            
            numerator_added = 0
            denominator_added = 0
            for i_period in numerators:
                if not numerator_added:
                    numerator_added = numerators[i_period].Clone()
                    denominator_added = denominators[i_period].Clone()
                else:
                    numerator_added.Add(numerators[i_period])
                    denominator_added.Add(denominators[i_period])            
            
            hists[period]["h_finaleff"] = numerator_added.Clone()
            hists[period]["h_finaleff"].SetName("h_finaleff")
            hists[period]["h_finaleff"].SetLineWidth(2)
            hists[period]["h_finaleff"].Divide(denominator_added)
            hists[period]["h_finaleff"] = update_uncertainties_from_teff(hists[period]["h_finaleff"], numerator_added, denominator_added)
            
            mc_numerator = hists[mcperiod]["h_tracks_tagged" + extra].Clone()
            mc_denominator = hists[mcperiod]["h_tracks_rereco"].Clone()
            mc_numerator.Scale(1.0/mc_numerator.Integral())
            mc_denominator.Scale(1.0/mc_denominator.Integral())
            hists[mcperiod]["h_mcfinaleff"] = mc_numerator
            hists[mcperiod]["h_mcfinaleff"].SetName("h_finaleff")
            hists[mcperiod]["h_mcfinaleff"].SetLineWidth(2)
            hists[mcperiod]["h_mcfinaleff"].Divide(mc_denominator)
            hists[mcperiod]["h_mcfinaleff"] = update_uncertainties_from_teff(hists[mcperiod]["h_mcfinaleff"], mc_numerator, mc_denominator)
            
            hists[period]["h_scalefactor"] = hists[period]["h_finaleff"].Clone()
            hists[period]["h_scalefactor"].SetName("h_scalefactor")
            hists[period]["h_scalefactor"].SetLineWidth(2)
            hists[period]["h_scalefactor"].Divide(hists[mcperiod]["h_mcfinaleff"])
            
            # fit:
            
            g1 = TF1( 'g1', '[0]',  0,  20 )
            fit = hists[period]["h_scalefactor"].Fit(g1, "", "same", 0, 20)
            
            fitresults["fit_sf_lumisam"][year + extra] = g1.GetParameter(0)
            #fitresults["fit_uncert_lumisam"][year + extra] = g1.GetParError(0)
            if "short" in extra:
                fitresults["fit_uncert_lumisam"][year + extra] = hists[period]["h_scalefactor"].GetBinError(4)
            else:
                fitresults["fit_uncert_lumisam"][year + extra] = hists[period]["h_scalefactor"].GetBinError(6)
            
            # draw fit:
            canvas = shared_utils.mkcanvas()
            shared_utils.histoStyler(hists[period]["h_scalefactor"])
            hists[period]["h_scalefactor"].Draw("hist e")
            hists[period]["h_scalefactor"].GetYaxis().SetRangeUser(0,2)
            g1.SetLineWidth(2)
            g1.Draw("same e")
            canvas.Print("plots/fit_sfsam_%s%s.pdf" % (year, extra))
            
        
                
        # draw plots with all run periods:
        
        for sftype in ["h_scalefactor", "h_recoscalefactor", "h_tagscalefactor"]:
        
            colors = [kBlack, kRed, kRed-6, kPink-2, kMagenta, kViolet, kBlue, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8, kOrange-10]
            
            for year in ["2016", "2017", "2018"]:    
            
                canvas = shared_utils.mkcanvas()
                legend = shared_utils.mklegend(x1=0.3, y1=0.2, x2=0.6, y2=0.35)
                for i, period in enumerate(periods):
                    
                    if year not in period: continue
                    
                    if i == 0:
                        hists[period][sftype].Draw("hist e")
                    else:
                        hists[period][sftype].Draw("hist e same")
                    hists[period][sftype].GetXaxis().SetRangeUser(3,21)
                    hists[period][sftype].GetYaxis().SetRangeUser(0,2)
                    
                    if sftype == "h_scalefactor":
                        hists[period][sftype].SetTitle(";remaining layers;scale factor")
                    if sftype == "h_recoscalefactor":
                        hists[period][sftype].SetTitle(";remaining layers;track reconstruction scale factor")
                    if sftype == "h_tagscalefactor":
                        hists[period][sftype].SetTitle(";remaining layers;track tagging scale factor")
                    
                    legend.AddEntry(hists[period][sftype], period)
                    hists[period][sftype].SetLineColor(colors.pop(0))
                    
                legend.Draw()
                shared_utils.stamp()
                
                pdffile = "plots%s/%s_%s%s.pdf" % (suffix, sftype, year, extra)
                
                if lumi_weighting:
                    pdffile = pdffile.replace(".pdf", "_lumiweighted.pdf")
                
                if use_uncertainty_from_teff:
                    pdffile = pdffile.replace(".pdf", "_teff.pdf")
                
                canvas.SaveAs(pdffile)
            
                if year == "Run":
                    colors = [kBlack, kRed, kRed-6, kPink-2, kMagenta, kViolet, kBlue, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8, kOrange-10]
    
    
    # draw short and long tracks SF for all run periods / years:
        
    for label in fitresults:
    
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.6, y1=0.7, x2=0.85, y2=0.85)
    
        if "_sf" not in label: continue
            
        if "lumi" in label:
            h_sf_short = TH1F("h_sf_short", "", 3, 0, 3)
            h_sf_long = TH1F("h_sf_long", "", 3, 0, 3)
        else:
            h_sf_short = TH1F("h_sf_short", "", 16, 0, 16)
            h_sf_long = TH1F("h_sf_long", "", 16, 0, 16)
        
        shared_utils.histoStyler(h_sf_short)
        shared_utils.histoStyler(h_sf_long)
        
        i_short = 0
        i_long = 0
        binlabels_short = []
        binlabels_long = []
        
        for i, period in enumerate(sorted(fitresults[label])):
            
            sf = fitresults[label][period]
            uncert = fitresults[label.replace("_sf", "_uncert")][period]
                
            if "short" in period:
                h_sf_short.SetBinContent(i_short + 1, sf)
                h_sf_short.SetBinError(i_short + 1, uncert)
                i_short +=1
                binlabels_short.append(period.replace("Run", "").replace("_short", "").replace("_long", ""))
                print "Adding", label, period, sf, uncert
            elif "long" in period:
                h_sf_long.SetBinContent(i_long + 1, sf)
                h_sf_long.SetBinError(i_long + 1, uncert)
                i_long += 1
                binlabels_long.append(period.replace("Run", "").replace("_short", "").replace("_long", ""))
                print "Adding", label, period, sf, uncert
                
        
        h_sf_short.SetLineColor(kRed)
        h_sf_short.Draw("hist e")
        h_sf_short.SetTitle(";;fitted scale factor")
        h_sf_short.GetYaxis().SetRangeUser(0.5,1.5)
        legend.AddEntry(h_sf_short, "short tracks")
        h_sf_long.SetLineColor(kBlue)
        h_sf_long.SetLineStyle(2)
        h_sf_long.Draw("hist e same")
        legend.AddEntry(h_sf_long, "long tracks")
            
        print binlabels_short
        print binlabels_long
            
        for i, i_binlabel in enumerate(binlabels_short):
            
            if binlabels_short[i] != binlabels_long[i]:
                print "whoa"
                quit()
            
            h_sf_short.GetXaxis().SetBinLabel(i + 1, i_binlabel)    
            h_sf_short.GetXaxis().SetTitleSize(0.04)
            h_sf_short.GetXaxis().SetLabelSize(0.04)   
        
        legend.Draw()
        
        shared_utils.stamp()
        
        pdfname = "plots%s/allperiods_sf_%s.pdf" % (suffix, label)            
        canvas.SaveAs(pdfname)
            
    
    
    
    
    
    
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "")
    (options, args) = parser.parse_args()

    os.system("mkdir -p plots%s" % options.suffix)
    allperiods(options.suffix)
