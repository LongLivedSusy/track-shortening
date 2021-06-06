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


def quickdraw(datahists, mchist, pdfout, mclabel = "", title = "", ymax = 9999, ymin = 9999, legendheader = ""):
    
    colors = [kBlack, kRed, kRed-6, kPink-2, kMagenta, kViolet, kBlue, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8, kOrange-10]
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1=0.6, y1=0.65, x2=0.9, y2=0.9)

    for i, datahist in enumerate(datahists):
        if i == 0:
            datahists[datahist].Draw("hist e0")
            datahists[datahist].SetTitle(title)
            if ymin != 9999:
                datahists[datahist].GetYaxis().SetRangeUser(ymin, ymax)
        else:
            datahists[datahist].Draw("hist e0 same")
        datahists[datahist].SetLineColor(colors.pop(0))
        legend.AddEntry(datahists[datahist], datahist)
        
    if mchist:
        mchist.Draw("hist e0 same")
        mchist.SetLineColor(kBlack)
        mchist.SetLineStyle(2)
        legend.AddEntry(mchist, mclabel)

    legend.SetHeader(legendheader)
    legend.Draw()
    canvas.SaveAs(pdfout)
    

def draw_2D_plots(hists, period, plotfolder, suffix, histolabels):

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
            canvas.SaveAs("%s/%s_%s.pdf" % (plotfolder, label.replace("h_", ""), period))  


def plotdatamc(histofolder, dataperiod, plotfolder, suffix, extralabel, histolabels, muon_plots = False, category = "", normalize = True):
    
    if "Run2016" in dataperiod:
        mcperiod = "Summer16"
    elif "Run2017" in dataperiod:
        mcperiod = "Fall17"
    elif "RunUL2017C" in dataperiod:
        mcperiod = "Fall17"
    elif "Run2018" in dataperiod:
        mcperiod = "Autumn18"
    else:
        mcperiod = "Fall17"
        
    if muon_plots:
        dataperiod += "_1"
        mcperiod += "_1"
    
    # get histos:
    hists_data = {}
    hists_mc = {}
    for label in histolabels:
        fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, dataperiod), "open")
        hists_data[label] = fin.Get(label + category)
        hists_data[label].SetDirectory(0)
        hists_data[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_data[label])
        fin.Close()
        
        fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, mcperiod), "open")
        hists_mc[label] = fin.Get(label + category)
        hists_mc[label].SetDirectory(0)
        hists_mc[label].SetLineWidth(2)
        shared_utils.histoStyler(hists_mc[label])
        fin.Close()
        
    for variable in histolabels:
        if variable in [
                        "h_muonPt",
                        "h_muonEta",
                        "h_muonPtCand",
                        "h_muonEtaCand",
                        "h_pfIso",
                        "h_mismatch"
                       ] or "track_" in variable or "cutflow" in variable or "h_ptratio_layer" in variable or "h_tracks_algo" in variable:
            
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
            if normalize:
                if "cutflow" not in variable:
                    if hists_data[variable].Integral():
                        hists_data[variable].Scale(1.0/hists_data[variable].Integral())
                    if hists_mc[variable].Integral():
                        hists_mc[variable].Scale(1.0/hists_mc[variable].Integral())
                else:
                    hists_data[variable].Scale(1.0/hists_data[variable].GetBinContent(1))
                    hists_mc[variable].Scale(1.0/hists_mc[variable].GetBinContent(1))
                
            if normalize:
                hists_data[variable].GetYaxis().SetRangeUser(1e-4,1e1)
            else:
                hists_data[variable].GetYaxis().SetRangeUser(1e-4,1e8)
                
                
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
            if True and "track_" in variable:
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
                if h_signal.Integral()>0 and normalize:
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
            
            if "cutflow" in variable:
                
                legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.5, y2=0.4)
                legend.SetTextSize(0.035)
                if "short" in variable:
                    legend.SetHeader("short tracks (%s)" % extralabel.replace("_", ""))
                elif "long" in variable:
                    legend.SetHeader("long tracks (%s)" % extralabel.replace("_", ""))
                else:
                    legend.SetHeader("%s" % extralabel.replace("_", ""))
                legend.AddEntry(hists_data[variable], "SingleMuon Data")
                legend.AddEntry(hists_mc[variable], "DYJetsToLL MC")
                legend.Draw()
                
                hists_data[variable].GetXaxis().SetTitleSize(0.04)
                hists_data[variable].GetXaxis().SetLabelSize(0.04)   
                
                canvas.SetLogy(False)
                
                binlabels = {
                              0: "#mu-matched tracks",
                              1: "p_{T}>25 (40) GeV",
                              2: "high purity",
                              3: "|eta|<2.0",
                              4: "#Delta p_{T}/p_{T}^{2}<10/GeV",
                              5: "dz<0.1 cm",
                              6: "relIso<0.2",
                              7: "tracker layer #geq2",
                              8: "tracker hits #geq2",
                              9: "no miss. inner hits",
                              10: "pixel hits #geq2",
                              11: "PF cand. veto",
                              12: "missing outer hits",
                              13: "BDT> 0.1 (0.1)",
                              14: "E_{dep}<15 or E_{dep}/p<0.15",
                }
                
                if "Run2016" not in dataperiod and "Summer16" not in dataperiod:
                    binlabels[13] = "BDT> 0.12 (0.15)"

                for i in binlabels:
                    hists_data[variable].GetXaxis().SetBinLabel(i + 1, binlabels[i]);
                    hists_mc[variable].GetXaxis().SetBinLabel(i + 1, binlabels[i]);
            
                hists_data[variable].GetXaxis().SetRangeUser(0,16)
                hists_data[variable].GetYaxis().SetRangeUser(0,1)
                hists_data[variable].SetTitle(";;fraction of remaining shortened tracks")
            
            canvas.SaveAs("%s/%s%s%s.pdf" % (plotfolder, variable.replace("h_", ""), extralabel, category))



def allperiods(histofolder, plotfolder, suffix, use_uncertainty_from_teff = False, lumi_weighting = 1, use_exact_layer_matching = False, ul_plots = False):
    
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
              
    if ul_plots:
        periods.append("RunUL2017C")
    
    histolabels = [
                    "h_tracks_reco",
                    "h_tracks_reco_short",                     
                    "h_tracks_reco_long",                     
                    "h_tracks_rereco",                   
                    "h_tracks_rereco_short",                   
                    "h_tracks_rereco_long",                   
                    "h_tracks_tagged",                   
                    "h_tracks_tagged_short",                   
                    "h_tracks_tagged_long",
                    "h_tracks_reco_rebinned",                     
                    "h_tracks_reco_rebinned_short",                     
                    "h_tracks_reco_rebinned_long",                     
                    "h_tracks_rereco_rebinned",                   
                    "h_tracks_rereco_rebinned_short",                   
                    "h_tracks_rereco_rebinned_long",                   
                    "h_tracks_tagged_rebinned",                   
                    "h_tracks_tagged_rebinned_short",                   
                    "h_tracks_tagged_rebinned_long",
                    "h_layers2D",                        
                    "h_shortbdt2D",                      
                    "h_longbdt2D",                       
                    "h_muonPt",                          
                    "h_muonEta",                   
                    "h_muonPtCand",                          
                    "h_muonEtaCand",                         
                    "h_pfIso",
                    "h_tracks_algo",
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
                    "cutflow_short",
                    "cutflow_long",
                    "h_ptratio",
                    "h_ptratio2D",
                    #"h_chi2ndof2D",
                    "h_mismatch",
                  ]
              
    # add layer-dependent track variable histograms:
    for label in list(histolabels):
        if "track_" in label or "h_ptratio" in label:
            for i in range(3,9):
                histolabels.append(label + "_layer%s" % i)
    
    # get all histos
    #######################################################################
    
    hists = {}
    for period in periods:
        hists[period] = {}
        for label in histolabels:
            fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, period), "open")                       
            
            if use_exact_layer_matching:
                mylabel = label.replace("rereco", "rereco_exact").replace("tagged", "tagged_exact")
            else:
                mylabel = label
                        
            hists[period][label] = fin.Get(mylabel)
            hists[period][label].SetDirectory(0)
            hists[period][label].SetLineWidth(2)
            shared_utils.histoStyler(hists[period][label])
            fin.Close()
            
    # dicts to save the fit results:    
    fitresults = {}
    fitresults["fit_sf"] = {}
    fitresults["fit_uncert"] = {}
    fitresults["fit_sf_lumiweighted"] = {}
    fitresults["fit_uncert_lumiweighted"] = {}
    
    fitresults["fit_sfreco"] = {}
    fitresults["fit_uncertreco"] = {}
    fitresults["fit_sfreco_lumiweighted"] = {}
    fitresults["fit_uncertreco_lumiweighted"] = {}
    fitresults["fit_sftag"] = {}
    fitresults["fit_uncerttag"] = {}
    fitresults["fit_sftag_lumiweighted"] = {}
    fitresults["fit_uncerttag_lumiweighted"] = {}
    
    sel_layers = [3, 4, 5, 7, 10]
    efflayer = {}
    for layer in sel_layers:
        efflayer[layer] = {}
        efflayer[layer]["tag_value"] = {}
        efflayer[layer]["reco_value"] = {}
        efflayer[layer]["tag_unc"] = {}
        efflayer[layer]["reco_unc"] = {}
        efflayer[layer]["tag_value_lumiweighted"] = {}
        efflayer[layer]["reco_value_lumiweighted"] = {}
        efflayer[layer]["tag_unc_lumiweighted"] = {}
        efflayer[layer]["reco_unc_lumiweighted"] = {}
    
    effcat = {}
    for cat in ["short", "long"]:
        effcat[cat] = {}
        effcat[cat]["tag_value"] = {}
        effcat[cat]["reco_value"] = {}
        effcat[cat]["tag_unc"] = {}
        effcat[cat]["reco_unc"] = {}
        effcat[cat]["tag_value_lumiweighted"] = {}
        effcat[cat]["reco_value_lumiweighted"] = {}
        effcat[cat]["tag_unc_lumiweighted"] = {}
        effcat[cat]["reco_unc_lumiweighted"] = {}
        
    # plot all categories
    #######################################################################
    
    for category in [
                  "",
                  "_short",
                  "_long"
                 ]:
                                                     
        # FIXME
        for period in periods:
            hists[period]["h_tracks_reco_short"] = hists[period]["h_tracks_reco"].Clone()
            hists[period]["h_tracks_reco_long"] = hists[period]["h_tracks_reco"].Clone()
        
        for period in periods:
                
            if category == "":
                draw_2D_plots(hists[period], period, plotfolder, suffix, histolabels)
            if "Run2017F" in period:
                plotdatamc(histofolder, period, plotfolder, suffix, "_%s%s" % (period.replace("Run", ""), category), histolabels)
                plotdatamc(histofolder, period, plotfolder, suffix, "_%s" % period.replace("Run", ""), histolabels, muon_plots = True)
                        
            # draw abs values:
            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
            headertext = period
            if category == "_short":
                headertext += ", short tracks"
            if category == "_long":
                headertext += ", long tracks"
            legend.SetHeader(headertext)
            legend.SetTextSize(0.035)
            hists[period]["h_tracks_reco" + category].Draw("hist e")
            hists[period]["h_tracks_reco" + category].SetTitle(";remaining layers;tracks")
            hists[period]["h_tracks_rereco" + category].Draw("hist e same")
            hists[period]["h_tracks_rereco" + category].SetLineStyle(2)
            hists[period]["h_tracks_tagged" + category].Draw("same hist e")
            hists[period]["h_tracks_tagged" + category].SetLineStyle(2)
            hists[period]["h_tracks_tagged" + category].SetLineColor(kRed)
            legend.AddEntry(hists[period]["h_tracks_reco" + category], "tracks matched to muons")
            legend.AddEntry(hists[period]["h_tracks_rereco" + category], "shortenend tracks")
            legend.AddEntry(hists[period]["h_tracks_tagged" + category], "shortenend & tagged tracks")
            shared_utils.stamp()
            legend.Draw()
            canvas.SaveAs("%s/absval_%s%s.pdf" % (plotfolder, period, category))  
            hists[period]["h_tracks_rereco" + category].SetLineStyle(1)
            hists[period]["h_tracks_tagged" + category].SetLineStyle(1)
                                                    
            # tagging and reconstruction efficiency:
            
            hists[period]["h_tagefficiency"] = hists[period]["h_tracks_tagged" + category].Clone()
            hists[period]["h_tagefficiency"].SetName("h_tagefficiency")
            hists[period]["h_tagefficiency"].SetLineWidth(2)
            hists[period]["h_tagefficiency"].Divide(hists[period]["h_tracks_rereco" + category])
            update_uncertainties_from_teff(hists[period]["h_tagefficiency"], hists[period]["h_tracks_tagged" + category], hists[period]["h_tracks_rereco" + category])
            
            hists[period]["h_recoefficiency"] = hists[period]["h_tracks_rereco" + category].Clone()
            hists[period]["h_recoefficiency"].SetName("h_recoefficiency")
            hists[period]["h_recoefficiency"].SetLineWidth(2)
            hists[period]["h_recoefficiency"].Divide(hists[period]["h_tracks_reco" + category])
            update_uncertainties_from_teff(hists[period]["h_recoefficiency"], hists[period]["h_tracks_rereco" + category], hists[period]["h_tracks_reco" + category])
            
            # single bin:
            hists[period]["h_tagefficiency_rebinned"] = hists[period]["h_tracks_tagged_rebinned" + category].Clone()
            hists[period]["h_tagefficiency_rebinned"].SetName("h_tagefficiency_rebinned")
            hists[period]["h_tagefficiency_rebinned"].SetLineWidth(2)
            hists[period]["h_tagefficiency_rebinned"].Divide(hists[period]["h_tracks_rereco_rebinned" + category])
            update_uncertainties_from_teff(hists[period]["h_tagefficiency_rebinned"], hists[period]["h_tracks_tagged_rebinned" + category], hists[period]["h_tracks_rereco_rebinned" + category])
            
            hists[period]["h_recoefficiency_rebinned"] = hists[period]["h_tracks_rereco_rebinned" + category].Clone()
            hists[period]["h_recoefficiency_rebinned"].SetName("h_recoefficiency_rebinned")
            hists[period]["h_recoefficiency_rebinned"].SetLineWidth(2)
            hists[period]["h_recoefficiency_rebinned"].Divide(hists[period]["h_tracks_reco_rebinned" + category])
            update_uncertainties_from_teff(hists[period]["h_recoefficiency_rebinned"], hists[period]["h_tracks_rereco_rebinned" + category], hists[period]["h_tracks_reco_rebinned" + category])
            
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
            canvas.SaveAs("%s/efficiency_%s%s.pdf" % (plotfolder, period, category))  
            
            # save efficiencies for time-dep. plot:
            for layer in sel_layers:
                efflayer[layer]["tag_value"][period + category] = hists[period]["h_tagefficiency"].GetBinContent(layer + 1)
                efflayer[layer]["reco_value"][period + category] = hists[period]["h_recoefficiency"].GetBinContent(layer + 1)
                efflayer[layer]["tag_unc"][period + category] = hists[period]["h_tagefficiency"].GetBinError(layer + 1)
                efflayer[layer]["reco_unc"][period + category] = hists[period]["h_recoefficiency"].GetBinError(layer + 1)
            
            if category != "":
                                
                effcat[category.replace("_", "")]["tag_value"][period] = hists[period]["h_tagefficiency_rebinned"].GetBinContent(1)
                effcat[category.replace("_", "")]["reco_value"][period] = hists[period]["h_recoefficiency_rebinned"].GetBinContent(1)
                effcat[category.replace("_", "")]["tag_unc"][period] = hists[period]["h_tagefficiency_rebinned"].GetBinError(1)
                effcat[category.replace("_", "")]["reco_unc"][period] = hists[period]["h_recoefficiency_rebinned"].GetBinError(1)
            
            if "Run2016" in period:
                mcperiod = "Summer16"
            elif "Run2017" in period:
                mcperiod = "Fall17"
            elif "Run2018" in period:
                mcperiod = "Autumn18"
            elif "RunUL2017C" in period:
                mcperiod = "Fall17"            
            else:
                continue
                
            # tagging scale factor:
            
            hists[mcperiod]["h_tagefficiency"] = hists[mcperiod]["h_tracks_tagged" + category].Clone()
            hists[mcperiod]["h_tagefficiency"].SetName("h_tagefficiency")
            hists[mcperiod]["h_tagefficiency"].SetLineWidth(2)
            hists[mcperiod]["h_tagefficiency"].Divide(hists[mcperiod]["h_tracks_rereco" + category])
            update_uncertainties_from_teff(hists[mcperiod]["h_tagefficiency"], hists[mcperiod]["h_tracks_tagged" + category], hists[mcperiod]["h_tracks_rereco" + category])
                        
            hists[period]["h_tagscalefactor"] = hists[period]["h_tagefficiency"].Clone()
            hists[period]["h_tagscalefactor"].SetName("h_tagscalefactor")
            hists[period]["h_tagscalefactor"].SetLineWidth(2)
            hists[period]["h_tagscalefactor"].Divide(hists[mcperiod]["h_tagefficiency"])
            
            g1 = TF1( 'g1', '[0]',  3,  20 )
            fit = hists[period]["h_tagscalefactor"].Fit(g1, "", "same", 3, 20)
            hint = hists[period]["h_tagscalefactor"].Clone()
            TVirtualFitter.GetFitter().GetConfidenceIntervals(hint)
            fitresults["fit_sftag"][period + category] = g1.GetParameter(0)
            fitresults["fit_uncerttag"][period + category] = g1.GetParError(0)

            ## draw fit:
            #canvas = shared_utils.mkcanvas()
            #shared_utils.histoStyler(hists[period]["h_tagscalefactor"])
            #hists[period]["h_tagscalefactor"].Draw("hist e0")
            #hists[period]["h_tagscalefactor"].GetYaxis().SetRangeUser(0,2)
            #hists[period]["h_tagscalefactor"].SetTitle(";tracker layers with measurement;global scale factor")
            #hint.SetLineColor(17)
            #hint.SetFillColor(17)
            #hint.SetFillStyle(3244)
            #hint.Draw("e3 same")
            #g1.SetLineWidth(2)
            #g1.Draw("same e0")
            #latex = TLatex()
            #latex.SetTextFont(42)
            #latex.SetNDC()
            #latex.SetTextSize(0.04)
            #latex.DrawLatex(0.72, 0.8, category.replace("_", "") + " tracks")
            #canvas.SaveAs("plots%s/fit_global_%s%s.pdf" % (options.suffix, period, category))
            

            # reconstruction scale factor:
            
            hists[mcperiod]["h_recoefficiency"] = hists[mcperiod]["h_tracks_rereco" + category].Clone()
            hists[mcperiod]["h_recoefficiency"].SetName("h_recoefficiency")
            hists[mcperiod]["h_recoefficiency"].SetLineWidth(2)
            hists[mcperiod]["h_recoefficiency"].Divide(hists[mcperiod]["h_tracks_reco" + category])
            update_uncertainties_from_teff(hists[mcperiod]["h_recoefficiency"], hists[mcperiod]["h_tracks_rereco" + category], hists[mcperiod]["h_tracks_reco" + category])
            
            hists[period]["h_recoscalefactor"] = hists[period]["h_recoefficiency"].Clone()
            hists[period]["h_recoscalefactor"].SetName("h_recoscalefactor")
            hists[period]["h_recoscalefactor"].SetLineWidth(2)
            hists[period]["h_recoscalefactor"].Divide(hists[mcperiod]["h_recoefficiency"])
                        
            g1 = TF1( 'g1', '[0]',  3,  20 )
            fit = hists[period]["h_recoscalefactor"].Fit(g1, "", "same", 3, 20)
            fitresults["fit_sfreco"][period + category] = g1.GetParameter(0)
            #fitresults["fit_uncertreco"][period + category] = g1.GetParError(0)
            
            if "short" in category:
                fitresults["fit_uncertreco"][period + category] = hists[period]["h_recoscalefactor"].GetBinError(4)
            else:
                fitresults["fit_uncertreco"][period + category] = hists[period]["h_recoscalefactor"].GetBinError(6)
            

            # global scale factor:
                        
            hists[period]["h_finaleff"] = hists[period]["h_tracks_tagged" + category].Clone()
            hists[period]["h_finaleff"].SetName("h_finaleff")
            hists[period]["h_finaleff"].SetLineWidth(2)
            hists[period]["h_finaleff"].Divide(hists[period]["h_tracks_reco" + category])
            #update_uncertainties_from_teff(hists[period]["h_finaleff"], hists[period]["h_tracks_tagged" + category], hists[period]["h_tracks_reco" + category])
            
            hists[mcperiod]["h_mcfinaleff"] = hists[mcperiod]["h_tracks_tagged" + category].Clone()
            hists[mcperiod]["h_mcfinaleff"].SetName("h_mcfinaleff")
            hists[mcperiod]["h_mcfinaleff"].SetLineWidth(2)
            hists[mcperiod]["h_mcfinaleff"].Divide(hists[mcperiod]["h_tracks_reco" + category])
            #update_uncertainties_from_teff(hists[mcperiod]["h_mcfinaleff"], hists[mcperiod]["h_tracks_tagged" + category], hists[mcperiod]["h_tracks_reco" + category])
            
            hists[period]["h_scalefactor"] = hists[period]["h_finaleff"].Clone()
            hists[period]["h_scalefactor"].SetName("h_scalefactor")
            hists[period]["h_scalefactor"].SetLineWidth(2)
            hists[period]["h_scalefactor"].Divide(hists[mcperiod]["h_mcfinaleff"])
                        
            g1 = TF1( 'g1', '[0]',  3,  20 )
            fit = hists[period]["h_scalefactor"].Fit(g1, "", "same", 3, 20)
            hint = hists[period]["h_scalefactor"].Clone()
            TVirtualFitter.GetFitter().GetConfidenceIntervals(hint)
            fitresults["fit_sf"][period + category] = g1.GetParameter(0)
            #fitresults["fit_uncert"][period + category] = g1.GetParError(0)
            
            if "short" in category:
                fitresults["fit_uncert"][period + category] = hists[period]["h_scalefactor"].GetBinError(4)
            else:
                fitresults["fit_uncert"][period + category] = hists[period]["h_scalefactor"].GetBinError(6)
                
            
            # draw fit:
            canvas = shared_utils.mkcanvas()
            shared_utils.histoStyler(hists[period]["h_scalefactor"])
            hists[period]["h_scalefactor"].Draw("hist e0")
            hists[period]["h_scalefactor"].GetYaxis().SetRangeUser(0,2)
            hists[period]["h_scalefactor"].SetTitle(";tracker layers with measurement;scale factor")
            hint.SetLineColor(17)
            hint.SetFillColor(17)
            hint.SetFillStyle(3244)
            hint.Draw("e3 same")
            g1.SetLineWidth(2)
            g1.Draw("same e0")
            latex = TLatex()
            latex.SetTextFont(42)
            latex.SetNDC()
            latex.SetTextSize(0.04)
            latex.DrawLatex(0.72, 0.8, category.replace("_", "") + " tracks")
            canvas.SaveAs("plots%s/sffit_global_%s%s.pdf" % (options.suffix, period, category))
            
        
        
        # draw UL efficiency ratio:
        if ul_plots and category == "":
            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.4, y1=0.2, x2=0.9, y2=0.4)
            legend.SetHeader("Pre-UL / UL (Run2017C)")
            legend.SetTextSize(0.04)
            ratio_reco = hists["Run2017C"]["h_recoefficiency"].Clone()
            ratio_reco.Divide(hists["RunUL2017C"]["h_recoefficiency"])
            ratio_reco.Draw("hist e")
            ratio_reco.SetTitle(";tracker layers with measurement;#epsilon (Pre-UL) / #epsilon (UL)")
            ratio_reco.GetXaxis().SetRangeUser(3,20)
            ratio_reco.GetYaxis().SetRangeUser(0,2)
            ratio_tag = hists["Run2017C"]["h_tagefficiency"].Clone()
            ratio_tag.Divide(hists["RunUL2017C"]["h_tagefficiency"])
            ratio_tag.Draw("hist e same")
            legend.AddEntry(ratio_reco, "reconstruction efficiency")
            legend.AddEntry(ratio_tag, "tagging efficiency")
            shared_utils.stamp()
            legend.Draw()
            canvas.SaveAs("%s/preul-ul.pdf" % (plotfolder))  
        
        
        # Lumi-weighting:
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
            
        for sf_type in ["global", "reco", "tag"]:
                
            for year in ["2016", "2017", "2018"]:  
                            
                if "2016" in year:
                    mcperiod = "Summer16"
                elif "2017" in year:
                    mcperiod = "Fall17"
                elif "2018" in year:
                    mcperiod = "Autumn18"
                else:
                    continue
                
                numerator_added = 0
                denominator_added = 0
                numerator_rebinned_added = 0
                denominator_rebinned_added = 0
                
                for rebinned in [False, True]:
            
                    if rebinned:
                        xcategory = "_rebinned" + category
                    else:
                        xcategory = category
            
                    numerators = {}
                    denominators = {}
                    
                    for i, i_period in enumerate(periods):
                    
                        if year in i_period:
                            if sf_type == "global":
                                numerators[i_period] = hists[i_period]["h_tracks_tagged" + xcategory].Clone()
                                denominators[i_period] = hists[i_period]["h_tracks_reco" + xcategory].Clone()
                            elif sf_type == "reco":
                                numerators[i_period] = hists[i_period]["h_tracks_rereco" + xcategory].Clone()
                                denominators[i_period] = hists[i_period]["h_tracks_reco" + xcategory].Clone()
                            elif sf_type == "tag":
                                numerators[i_period] = hists[i_period]["h_tracks_tagged" + xcategory].Clone()
                                denominators[i_period] = hists[i_period]["h_tracks_rereco" + xcategory].Clone()
                            numerators[i_period].Scale(official_lumis[i_period]/denominators[i_period].Integral())
                            denominators[i_period].Scale(official_lumis[i_period]/denominators[i_period].Integral())            
                                                        
                    if not rebinned:
                        for i_period in numerators:
                            if not numerator_added:
                                numerator_added = numerators[i_period].Clone()
                                denominator_added = denominators[i_period].Clone()
                            else:
                                numerator_added.Add(numerators[i_period])
                                denominator_added.Add(denominators[i_period])   
                
                    else:
                        for i_period in numerators:
                            if not numerator_rebinned_added:
                                numerator_rebinned_added = numerators[i_period].Clone()
                                denominator_rebinned_added = denominators[i_period].Clone()
                            else:
                                numerator_rebinned_added.Add(numerators[i_period])
                                denominator_rebinned_added.Add(denominators[i_period])   
                
                h_finaleff = numerator_added.Clone()
                h_finaleff.SetName("h_finaleff")
                h_finaleff.SetLineWidth(2)
                h_finaleff.Divide(denominator_added)

                h_finaleff_rebinned = numerator_rebinned_added.Clone()
                h_finaleff_rebinned.SetName("h_finaleff_rebinned")
                h_finaleff_rebinned.SetLineWidth(2)
                h_finaleff_rebinned.Divide(denominator_rebinned_added)
                
                if sf_type == "global":
                    mc_numerator = hists[mcperiod]["h_tracks_tagged" + category].Clone()
                    mc_denominator = hists[mcperiod]["h_tracks_reco" + category].Clone()
                    mc_numerator_rebinned = hists[mcperiod]["h_tracks_tagged_rebinned" + category].Clone()
                    mc_denominator_rebinned = hists[mcperiod]["h_tracks_reco_rebinned" + category].Clone()
                elif sf_type == "reco":
                    mc_numerator = hists[mcperiod]["h_tracks_rereco" + category].Clone()
                    mc_denominator = hists[mcperiod]["h_tracks_reco" + category].Clone()
                    mc_numerator_rebinned = hists[mcperiod]["h_tracks_rereco_rebinned" + category].Clone()
                    mc_denominator_rebinned = hists[mcperiod]["h_tracks_reco_rebinned" + category].Clone()
                elif sf_type == "tag":
                    mc_numerator = hists[mcperiod]["h_tracks_tagged" + category].Clone()
                    mc_denominator = hists[mcperiod]["h_tracks_rereco" + category].Clone()
                    mc_numerator_rebinned = hists[mcperiod]["h_tracks_tagged_rebinned" + category].Clone()
                    mc_denominator_rebinned = hists[mcperiod]["h_tracks_rereco_rebinned" + category].Clone()
                mc_numerator.Scale(1.0/mc_denominator.Integral())
                mc_denominator.Scale(1.0/mc_denominator.Integral())
                mc_numerator_rebinned.Scale(1.0/mc_denominator_rebinned.Integral())
                mc_denominator_rebinned.Scale(1.0/mc_denominator_rebinned.Integral())
                               
                h_mcfinaleff = mc_numerator.Clone()
                h_mcfinaleff.SetName("h_mcfinaleff")
                h_mcfinaleff.SetLineWidth(2)
                h_mcfinaleff.Divide(mc_denominator)
                            
                h_mcfinaleff_rebinned = mc_numerator_rebinned.Clone()
                h_mcfinaleff_rebinned.SetName("h_mcfinaleff_rebinned")
                h_mcfinaleff_rebinned.SetLineWidth(2)
                h_mcfinaleff_rebinned.Divide(mc_denominator_rebinned)
                            
                # lumi-weighted scale factors:
                                
                #update_uncertainties_from_teff(hists[period]["h_finaleff"], numerator_added, denominator_added)
                #update_uncertainties_from_teff(hists[mcperiod]["h_mcfinaleff"], mc_numerator, mc_denominator)
                
                quickdraw({"Data": h_finaleff}, hists[mcperiod]["h_mcfinaleff"], "plots%s/ratios-after-teff" % options.suffix + category + year + ".pdf", mclabel = "MC", title = "# tagged / # reco;layers;ratio", ymin = 0, ymax = 3)
                            
                h_scalefactor = h_finaleff.Clone()
                h_scalefactor.SetName("h_scalefactor")
                h_scalefactor.SetLineWidth(2)
                h_scalefactor.Divide(h_mcfinaleff)            
                
                quickdraw({"SF, with TEfficiency": h_scalefactor}, False, "plots%s/sf-teff" % options.suffix + category + year + ".pdf", title = ";layers;SF", ymin = 0, ymax = 2)
                
                # fit:
                g1 = TF1( 'g1', '[0]',  3,  20 )
                fit = h_scalefactor.Fit(g1, "", "same", 3, 20)
                hint = h_scalefactor.Clone()
                TVirtualFitter.GetFitter().GetConfidenceIntervals(hint)
                
                fitresults["fit_sf%s_lumiweighted" % sf_type.replace("global", "")][year + category] = g1.GetParameter(0)
                if "short" in category:
                    fitresults["fit_uncert%s_lumiweighted" % sf_type.replace("global", "")][year + category] = h_scalefactor.GetBinError(4)
                elif "long" in category:
                    fitresults["fit_uncert%s_lumiweighted" % sf_type.replace("global", "")][year + category] = h_scalefactor.GetBinError(6)
                else:
                    fitresults["fit_uncert%s_lumiweighted" % sf_type.replace("global", "")][year + category] = h_scalefactor.GetBinError(6)
                
                # draw fit:
                canvas = shared_utils.mkcanvas()
                shared_utils.histoStyler(h_scalefactor)
                h_scalefactor.Draw("hist e0")
                h_scalefactor.GetYaxis().SetRangeUser(0,2)
                
                hint.SetLineColor(17)
                hint.SetFillColor(17)
                hint.SetFillStyle(3244)
                hint.Draw("e3 same")
                
                g1.SetLineWidth(2)
                g1.Draw("same e0")
                
                legend = shared_utils.mklegend(x1=0.6, y1=0.65, x2=0.9, y2=0.9)
                legend.SetHeader(category.replace("_", "") + " tracks")
                legend.Draw()
                canvas.SaveAs("plots%s/fit_%s_%s%s.pdf" % (options.suffix, sf_type, year, category))
            
                # lumi-weighted efficiencies:
                if category == "" and sf_type != "global":
                    for layer in sel_layers:
                        efflayer[layer]["%s_value_lumiweighted" % sf_type][year + category] = h_finaleff.GetBinContent(layer + 1)
                        efflayer[layer]["%s_unc_lumiweighted" % sf_type][year + category] = h_finaleff.GetBinError(layer + 1)
                        efflayer[layer]["%s_value_lumiweighted" % sf_type][mcperiod + category] = h_mcfinaleff.GetBinContent(layer + 1)
                        efflayer[layer]["%s_unc_lumiweighted" % sf_type][mcperiod + category] = h_mcfinaleff.GetBinError(layer + 1)
                
                if category != "" and sf_type != "global":
                                        
                    effcat[category.replace("_", "")]["%s_value_lumiweighted" % sf_type][year] = h_finaleff_rebinned.GetBinContent(1)
                    effcat[category.replace("_", "")]["%s_unc_lumiweighted" % sf_type][year] = h_finaleff_rebinned.GetBinError(1)
                    effcat[category.replace("_", "")]["%s_value_lumiweighted" % sf_type][mcperiod] = h_mcfinaleff_rebinned.GetBinContent(1)
                    effcat[category.replace("_", "")]["%s_unc_lumiweighted" % sf_type][mcperiod] = h_mcfinaleff_rebinned.GetBinError(1)
                
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
                
                pdffile = "%s/%s_%s%s.pdf" % (plotfolder, sftype, year, category)
                
                if lumi_weighting:
                    pdffile = pdffile.replace(".pdf", "_lumiweighted.pdf")
                
                if use_uncertainty_from_teff:
                    pdffile = pdffile.replace(".pdf", "_teff.pdf")
                
                canvas.SaveAs(pdffile)
            
                if year == "Run":
                    colors = [kBlack, kRed, kRed-6, kPink-2, kMagenta, kViolet, kBlue, kAzure+9, kCyan, kTeal-1, kGreen, kGreen+2, kSpring+9, kYellow-3, kOrange, kOrange-8, kOrange-10]
        
    
    # draw short and long tracks SF for all run periods / years:
    #######################################################################
    
    for label in fitresults:
    
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.6, y1=0.7, x2=0.85, y2=0.85)
        #FIXME
        legend.SetHeader(suffix)
    
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
        if "reco" in label:
            h_sf_short.SetTitle(";;fitted track reconstruction scale factor")
        elif "tag" in label:
            h_sf_short.SetTitle(";;fitted track tagging scale factor")
        else:
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
                print "binlabels"
                quit()
            
            h_sf_short.GetXaxis().SetBinLabel(i + 1, i_binlabel)    
        
        if "lumi" not in label:
            h_sf_short.GetXaxis().SetTitleSize(0.04)
            h_sf_short.GetXaxis().SetLabelSize(0.04)   
        else:
            print "lumilumi"
            #h_sf_short.GetXaxis().SetTitleSize(1.2)
            h_sf_short.GetXaxis().SetLabelSize(0.1)
        
        legend.Draw()
        
        shared_utils.stamp()
        
        pdfname = "%s/allperiods_sf_%s.pdf" % (plotfolder, label)
        
        if use_exact_layer_matching:
            pdfname = pdfname.replace(".pdf", "_exact.pdf")
                
        canvas.SaveAs(pdfname)

        fout = TFile(pdfname.replace(".pdf", ".root"), "recreate")
        canvas.Write()
        h_sf_short.SetName("h_scalefactor_short")
        h_sf_short.Write()
        h_sf_long.SetName("h_scalefactor_long")
        h_sf_long.Write()
        fout.Close()
    
    efflayer[0] = effcat["short"]
    
    
    # draw efficiencies:  
    #######################################################################

    for layer in efflayer:
        for label in efflayer[layer]:
            
            if "short" in label or "long" in label: continue
            
            if "tag_value" not in label: continue
            
            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.5, y1=0.2, x2=0.85, y2=0.35)
            
            if "lumi" in label:
                h_sf_tag = TH1F("h_sf_tag", "", 3, 0, 3)
                h_sf_reco = TH1F("h_sf_reco", "", 3, 0, 3)
                h_sf_tag_mc = TH1F("h_sf_tag_mc", "", 3, 0, 3)
                h_sf_reco_mc = TH1F("h_sf_reco_mc", "", 3, 0, 3)
                shared_utils.histoStyler(h_sf_tag_mc)
                shared_utils.histoStyler(h_sf_reco_mc)
            else:
                h_sf_tag = TH1F("h_sf_tag", "", 20, 0, 20)
                h_sf_reco = TH1F("h_sf_reco", "", 20, 0, 20)
            
            shared_utils.histoStyler(h_sf_tag)
            shared_utils.histoStyler(h_sf_reco)
            
            i_tag = 0
            i_reco = 0
            binlabels_tag = []
            binlabels_reco = []
            
            if "lumi" not in label:
                period_labels = ["Summer16", "Fall17", "Autumn18"]
                for i, period in enumerate(sorted(efflayer[layer][label])):
                    if "Run201" not in period: continue
                    if "short" in period or "long" in period: continue
                    period_labels.append(period)
            else:
                period_labels = ["2016", "2017", "2018"]
            
            for i, period in enumerate(period_labels):

                tag_sf = efflayer[layer][label][period]
                tag_uncert = efflayer[layer][label.replace("_value", "_unc")][period]
                h_sf_tag.SetBinContent(i_tag + 1, tag_sf)
                h_sf_tag.SetBinError(i_tag + 1, tag_uncert)                
                binlabels_tag.append(period.replace("Run", ""))
                
                reco_sf = efflayer[layer][label.replace("tag", "reco")][period]
                reco_uncert = efflayer[layer][label.replace("tag", "reco").replace("_value", "_unc")][period]
                h_sf_reco.SetBinContent(i_reco + 1, reco_sf)
                h_sf_reco.SetBinError(i_reco + 1, reco_uncert)
                binlabels_reco.append(period.replace("Run", ""))
                
                if "lumi" in label:
                    
                    if "2016" in period:
                        mcperiod = "Summer16"
                    elif "2017" in period:
                        mcperiod = "Fall17"
                    elif "2018" in period:
                        mcperiod = "Autumn18"
                        
                    tag_sf = efflayer[layer][label][mcperiod]
                    tag_uncert = efflayer[layer][label.replace("_value", "_unc")][mcperiod]
                    h_sf_tag_mc.SetBinContent(i_tag + 1, tag_sf)
                    h_sf_tag_mc.SetBinError(i_tag + 1, tag_uncert)
                
                    reco_sf = efflayer[layer][label.replace("tag", "reco")][mcperiod]
                    reco_uncert = efflayer[layer][label.replace("tag", "reco").replace("_value", "_unc")][mcperiod]
                    h_sf_reco_mc.SetBinContent(i_reco + 1, reco_sf)
                    h_sf_reco_mc.SetBinError(i_reco + 1, reco_uncert)
                    
                i_tag +=1
                i_reco += 1
                           
            h_sf_tag.SetLineColor(kRed)
            h_sf_tag.Draw("hist e")
            h_sf_tag.SetTitle(";;efficiency")
            h_sf_tag.GetYaxis().SetRangeUser(0,1)
            legend.AddEntry(h_sf_tag, "tagging efficiency")
            h_sf_reco.SetLineColor(kBlue)
            #h_sf_reco.SetLineStyle(2)
            h_sf_reco.Draw("hist e same")
            legend.AddEntry(h_sf_reco, "reconstruction efficiency")
            
            
            if "lumi" in label:
                h_sf_reco_mc.Draw("hist e same")
                h_sf_reco_mc.SetLineColor(kBlue)
                h_sf_reco_mc.SetLineStyle(2)
                legend.AddEntry(h_sf_reco_mc, "reconstruction efficiency (MC)")
                h_sf_tag_mc.Draw("hist e same")
                h_sf_tag_mc.SetLineColor(kRed)
                h_sf_tag_mc.SetLineStyle(2)
                legend.AddEntry(h_sf_tag_mc, "tagging efficiency (MC)")
                 
            for i, i_binlabel in enumerate(binlabels_tag):
                
                if binlabels_tag[i] != binlabels_reco[i]:
                    print "whoa"
                    quit()
                
                h_sf_tag.GetXaxis().SetBinLabel(i + 1, i_binlabel)    
            
            if layer == 0:
                legend.SetHeader("pixel-only tracks")
            else:
                legend.SetHeader("%s layers" % layer)
            legend.Draw()
            
            if "lumi" not in label:
                h_sf_tag.GetXaxis().SetTitleSize(0.04)
                h_sf_tag.GetXaxis().SetLabelSize(0.04)   
            else:
                print "lumilumi"
                h_sf_tag.GetXaxis().SetTitleSize(0.25)
                #h_sf_tag.GetXaxis().SetLabelSize(0.5)
                #h_sf_tag.GetYaxis().SetLabelSize(h_sf_tag.GetXaxis().GetLabelSize())
            shared_utils.stamp()
            
            pdfname = "%s/allperiods_eff_%s.pdf" % (plotfolder, layer)
            
            if use_exact_layer_matching:
                pdfname = pdfname.replace(".pdf", "_exact.pdf")
            if "lumi" in label:
                pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")
            
            canvas.SaveAs(pdfname)

    
if __name__ == "__main__":

    print "Loading"

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")

    (options, args) = parser.parse_args()
    
    plotfolder = "plots%s" % options.suffix
    os.system("mkdir -p %s" % plotfolder)
    
    allperiods(options.histofolder, plotfolder, options.suffix)
