#!/bin/env python
import GridEngineTools
import os
import glob
import shared_utils
import plotting
from ROOT import *

os.system("mkdir -p plots")
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

histolabels = [
                "h_tracks_reco",                     
                "h_tracks_rereco",                   
                "h_tracks_reco_rebinned",                     
                "h_tracks_rereco_rebinned",                   
                "h_tracks_preselection",             
                "h_tracks_tagged",                   
                "h_tracks_tagged_rebinned",                   
                "h_layers2D",                        
                "h_shortbdt2D",                      
                "h_longbdt2D",                       
                "h_muonPt",                          
                "h_muonEta",                         
                "h_pfIso",                           
                "track_is_pixel_track",              
                "track_dxyVtx",                      
                "track_dzVtx",                                     
                "track_trkRelIso",                   
                "track_nValidPixelHits",             
                "track_nValidTrackerHits",           
                "track_trackerLayersWithMeasurement",
                "track_ptErrOverPt2",                
                "track_chi2perNdof",                 
                "track_mva",                         
                "track_pt",                          
                "track_trackQualityHighPurity",      
                "track_nMissingInnerHits",           
                "track_passPFCandVeto",              
                "track_nMissingOuterHits",           
                "track_matchedCaloEnergy",           
                "track_p",         
                "cutflow",
                "h_ptratio_layer3",
                "h_ptratio_layer4",
                "h_ptratio_layer5",
                "h_ptratio_layer6",
                "h_ptratio_layer7",
                "h_ptratio_layer8",
                "h_ptratio_layer9",
                "h_ptratio_layer10",
                "h_ptratio2D",
              ]

def submit():
    
    commands = []
    
    for period in ["Summer16", "Run2016"]: 
        for i in range(1, 21):
            commands.append("cd ~/cmssw/CMSSW_9_2_7_patch1/src/; eval `scramv1 runtime -sh`; cd -; python analyzer.py %s_ISOTRACKS/*_%s.root" % (period, i))

    GridEngineTools.runParallel(commands, "grid", condorDir="condor.analysis")
    for period in ["Summer16", "Run2016"]: 
        os.system("hadd -f histograms_%s.root histograms_%s_?.root histograms_%s_??.root && rm histograms_%s_?.root && rm histograms_%s_??.root" % (period, period, period, period, period))
        

def plot(period):

    # get histos:
    fin = TFile("histograms_%s.root" % period, "open")
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
    canvas.Print("plots/trackShortening_efficiency_%s.pdf" % period)  

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
    canvas.Print("plots/trackShortening_absval_%s.pdf" % period)  

    # draw other plots:
    for label in histolabels:
        if label in ["h_layers2D", "h_shortbdt2D", "h_longbdt2D", "h_ptratio2D"]:
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
                canvas.SetLogy(True)
                hists[label].Scale(1.0/hists[label].Integral())
                hists[label].GetYaxis().SetRangeUser(1e-4,1e1)
                hists[label].Draw("hist e")
                hists[label].SetTitle(";%s;normalized events" % label)
                            
            shared_utils.stamp()
            canvas.Print("plots/trackShortening_%s_%s.pdf" % (label.replace("h_", ""), period))  


def scalefactors():

    # get histos:
    hists_data = {}
    hists_mc = {}
    for label in histolabels:
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
    
    hists_data["h_tagefficiency_rebinned"] = hists_data["h_tracks_tagged_rebinned"].Clone()
    hists_data["h_tagefficiency_rebinned"].SetName("h_tagefficiency_rebinned")
    hists_data["h_tagefficiency_rebinned"].SetLineWidth(2)
    hists_data["h_tagefficiency_rebinned"].Divide(hists_data["h_tracks_rereco_rebinned"])
    
    hists_mc["h_tagefficiency_rebinned"] = hists_mc["h_tracks_tagged_rebinned"].Clone()
    hists_mc["h_tagefficiency_rebinned"].SetName("h_tagefficiency_rebinned")
    hists_mc["h_tagefficiency_rebinned"].SetLineWidth(2)
    hists_mc["h_tagefficiency_rebinned"].Divide(hists_mc["h_tracks_rereco_rebinned"])

    hists_data["h_scalefactor_rebinned"] = hists_data["h_tagefficiency_rebinned"].Clone()
    hists_data["h_scalefactor_rebinned"].SetName("h_scalefactor_rebinned")
    hists_data["h_scalefactor_rebinned"].SetLineWidth(2)
    hists_data["h_scalefactor_rebinned"].Divide(hists_mc["h_tagefficiency_rebinned"])
    
    # draw scale factor:
    canvas = shared_utils.mkcanvas()
    hists_data["h_scalefactor"].Draw("hist e")
    hists_data["h_scalefactor_rebinned"].SetLineColor(kRed)
    hists_data["h_scalefactor_rebinned"].Draw("hist e same")
    
    ErrorHistogram = hists_data["h_scalefactor_rebinned"].Clone('ErrorHistogram')
    ErrorHistogram.SetFillStyle(3244)
    ErrorHistogram.SetFillColor(kGray+1)
    ErrorHistogram.Draw('e2 sames')
    
    hists_data["h_scalefactor"].SetTitle(";remaining layers;scale factor")
    hists_data["h_scalefactor"].GetYaxis().SetRangeUser(0,2)
    shared_utils.stamp()
    canvas.Print("plots/trackShortening_scalefactor.pdf")
    
    # draw pt:
    for variable in histolabels:
        if variable in ["h_muonPt", "h_muonEta", "h_pfIso"] or "track_" in variable or "cutflow" in variable or "h_ptratio_layer" in variable:
            
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
            if "h_ptratio_layer" in variable:   
                vartext = "p_{T}^{#mu-matched track} / p_{T}^{shortened track}"
            
            if "track_" in variable:
                hists_data[variable].SetTitle(";%s;normalized number of tracks" % vartext)
            else:
                hists_data[variable].SetTitle(";%s;normalized number of events" % vartext)
            
            # if track variable, let's include the signal too!
            if "track_" in variable:
                continue
                folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_64_p15OptionalJetVeto_merged"
                input_files = glob.glob(folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq*root")
                base_cut = "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975 && tracks_nMissingMiddleHits==0"
                
                # alright, all set
                h_signal = plotting.get_histogram_from_file(input_files, "Events", variable.replace("track_", "tracks_"), cutstring=base_cut, nBinsX=hists_data[variable].GetNbinsX(), xmin=hists_data[variable].GetXaxis().GetXmin(), xmax=hists_data[variable].GetXaxis().GetXmax())
                shared_utils.histoStyler(h_signal)
                h_signal.SetLineWidth(2)
                h_signal.SetLineColor(kBlue)
                if h_signal.Integral()>0:
                    h_signal.Scale(1.0/h_signal.Integral())
                h_signal.Draw("hist e same")
                
            shared_utils.stamp()
            
            #if "h_ptratio_layer3" in variable:
            #                    
            #    legend = shared_utils.mklegend(x1=0.55, y1=0.7, x2=0.9, y2=0.9)
            #    legend.AddEntry(hists_data[variable], "SingleMuon Data")
            #    legend.AddEntry(hists_mc[variable], "DYJetsToLL MC")
            #    legend.AddEntry(hists_data["h_ptratio_layer3"], "3 layers")
            #    colors = [kRed, kBlue, kTeal, kGreen]
            #    for i_layer in [4,5,10]:
            #        color = colors.pop(0)
            #        hists_mc["h_ptratio_layer%s" % i_layer].SetLineColor(color)
            #        hists_data["h_ptratio_layer%s" % i_layer].SetMarkerColor(color)
            #        hists_data["h_ptratio_layer%s" % i_layer].Scale(1.0/hists_data["h_ptratio_layer%s" % i_layer].Integral())
            #        hists_mc["h_ptratio_layer%s" % i_layer].Scale(1.0/hists_mc["h_ptratio_layer%s" % i_layer].Integral())
            #        
            #        hists_mc["h_ptratio_layer%s" % i_layer].Draw("hist e same")
            #        hists_data["h_ptratio_layer%s" % i_layer].SetMarkerStyle(20)
            #        hists_data["h_ptratio_layer%s" % i_layer].Draw("p same")
            #        legend.AddEntry(hists_mc["h_ptratio_layer%s" % i_layer], "%s layers" % i_layer)
                    
            
            if "track_" in variable or "h_muonPt" in variable or "h_pfIso" in variable:
                legend = shared_utils.mklegend(x1=0.55, y1=0.7, x2=0.9, y2=0.9)
                legend.AddEntry(hists_data[variable], "SingleMuon Data")
                legend.AddEntry(hists_mc[variable], "DYJetsToLL MC")
                if "track_" in variable:
                    legend.AddEntry(h_signal, "Signal")
                legend.Draw()
                
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
            
            canvas.Print("plots/trackShortening_%s.pdf" % variable.replace("h_", ""))
        
#submit()
for period in ["Summer16", "Run2016"]: 
    plot(period)
scalefactors()
