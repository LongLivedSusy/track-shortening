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

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "MCReweighting")
    parser.add_option("--mcsuffix", dest = "mcsuffix", default = "")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")
    parser.add_option("--reweighted", dest = "mc_reweighted", action = "store_true")

    (options, args) = parser.parse_args()
    
    histofolder = options.histofolder
    suffix = options.suffix
    
    plotfolder = "plots%s_new" % options.suffix
    if options.mcsuffix != "":
        plotfolder = plotfolder.replace("_new", "_%s_new" % options.mcsuffix)
    
    os.system("mkdir -p %s" % plotfolder)

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
              
    if options.mc_reweighted:
        periods += [
                "Summer16rwRun2016B",
                "Summer16rwRun2016C",
                "Summer16rwRun2016D",
                "Summer16rwRun2016E",
                "Summer16rwRun2016F",
                "Summer16rwRun2016G",
                "Summer16rwRun2016H",
                "Fall17rwRun2017B",
                "Fall17rwRun2017C",
                "Fall17rwRun2017D",
                "Fall17rwRun2017E",
                "Fall17rwRun2017F",
                "Autumn18rwRun2018A",
                "Autumn18rwRun2018B",
                "Autumn18rwRun2018C",
                "Autumn18rwRun2018D",
              ]
    
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
                  ]
    
    # get all histos:
    hists = {}
    for period in periods:
        hists[period] = {}
        for label in histolabels:
            if options.mcsuffix != "":
                if "Run201" in period and "rw" not in period:
                    fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, period), "open")
                else:
                    fin = TFile("%s/histograms%s_%s.root" % (histofolder, options.mcsuffix, period), "open")                                           
            else:
                fin = TFile("%s/histograms%s_%s.root" % (histofolder, suffix, period), "open")                       
            hists[period][label] = fin.Get(label)
            hists[period][label].SetDirectory(0)
            hists[period][label].SetLineWidth(2)
            shared_utils.histoStyler(hists[period][label])
            fin.Close()
            
    # denom. fix:
    for period in periods:
        hists[period]["h_tracks_reco_short"] = hists[period]["h_tracks_reco"].Clone()
        hists[period]["h_tracks_reco_long"] = hists[period]["h_tracks_reco"].Clone()
    
    # global SF:
    fitresults = {}
    fitresults["fit_sf"] = {}
    fitresults["fit_uncert"] = {}
    fitresults["fit_sfreco"] = {}
    fitresults["fit_uncertreco"] = {}
    fitresults["fit_sftag"] = {}
    fitresults["fit_uncerttag"] = {}
        
    for category in ["_short", "_long"]:
            
        finaleff_global = {}
        finaleff_reco = {}
        finaleff_tag = {}

        for period in periods:
            
            print category, period
            
            finaleff_global[period] = hists[period]["h_tracks_tagged" + category].Clone()
            finaleff_global[period].Divide(hists[period]["h_tracks_reco" + category])
                                    
            finaleff_reco[period] = hists[period]["h_tracks_rereco" + category].Clone()
            finaleff_reco[period].Divide(hists[period]["h_tracks_reco" + category])

            finaleff_tag[period] = hists[period]["h_tracks_tagged" + category].Clone()
            finaleff_tag[period].Divide(hists[period]["h_tracks_rereco" + category])
            
                    
        h_sf_global = {}
        h_sf_reco = {}
        h_sf_tag = {}
                    
        for period in periods:
        
            print category, period
        
            if "rw" in period: continue
            if "Run201" not in period: continue
            
            if not options.mc_reweighted:
                if "Run2016" in period:
                    mcperiod = "Summer16"
                elif "Run2017" in period:
                    mcperiod = "Fall17"
                elif "Run2018" in period:
                    mcperiod = "Autumn18"
            else:
                if "Run2016" in period:
                    mcperiod = "Summer16rw" + period 
                elif "Run2017" in period:
                    mcperiod = "Fall17rw" + period
                elif "Run2018" in period: 
                    mcperiod = "Autumn18rw" + period
            
            g1 = TF1( 'g1', '[0]',  3,  20 )
            
            h_sf_global[period] = finaleff_global[period].Clone()
            h_sf_global[period].Divide(finaleff_global[mcperiod])
            fit = h_sf_global[period].Fit(g1, "Q", "same", 3, 20)
            fitresults["fit_sf"][period + category] = g1.GetParameter(0)
            if "short" in category:
                fitresults["fit_uncert"][period + category] = h_sf_global[period].GetBinError(4)
            else:
                fitresults["fit_uncert"][period + category] = h_sf_global[period].GetBinError(6)
            
            h_sf_reco[period] = finaleff_reco[period].Clone()
            h_sf_reco[period].Divide(finaleff_reco[mcperiod])
            fit = h_sf_reco[period].Fit(g1, "Q", "same", 3, 20)
            fitresults["fit_sfreco"][period + category] = g1.GetParameter(0)
            if "short" in category:
                fitresults["fit_uncertreco"][period + category] = h_sf_reco[period].GetBinError(4)
            else:
                fitresults["fit_uncertreco"][period + category] = h_sf_reco[period].GetBinError(6)
            
            h_sf_tag[period] = finaleff_tag[period].Clone()
            h_sf_tag[period].Divide(finaleff_tag[mcperiod])
            fit = h_sf_tag[period].Fit(g1, "Q", "same", 3, 20)
            fitresults["fit_sftag"][period + category] = g1.GetParameter(0)
            if "short" in category:
                fitresults["fit_uncerttag"][period + category] = h_sf_tag[period].GetBinError(4)
            else:
                fitresults["fit_uncerttag"][period + category] = h_sf_tag[period].GetBinError(6)
            
        
        # plot efficiencies:
        for i, i_hist in h_sf_global:
            if i == 0:
                i_hist.Draw("hist")
            else:
                i_hist.Draw("hist same")
                        

    # plot:
    
    for label in ["fit_sf", "fit_sfreco", "fit_sftag"]:
    
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.6, y1=0.7, x2=0.85, y2=0.85)
            
        #h_sf_short = TH1F("h_sf_short", "", 3, 0, 3)
        #h_sf_long = TH1F("h_sf_long", "", 3, 0, 3)
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
        h_sf_short.GetYaxis().SetRangeUser(0.25,1.5)
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
        
        if options.mc_reweighted:
            pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
                     
        canvas.SaveAs(pdfname)
        
        #fout = TFile(pdfname.replace(".pdf", ".root"), "recreate")
        #canvas.Write()
        #h_sf_short.SetName("h_scalefactor_short")
        #h_sf_short.Write()
        #h_sf_long.SetName("h_scalefactor_long")
        #h_sf_long.Write()
        #fout.Close()
                             