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

def main(options, lumiweighted):
    
    histofolder = options.histofolder
    suffix = options.suffix
    
    plotfolder = "plots%s_new2" % options.suffix
    if options.mcsuffix != "":
        plotfolder = plotfolder.replace("_new2", "_%s_new2" % options.mcsuffix)
    
    os.system("mkdir -p %s" % plotfolder)

    periods = [
                #"Run2016B",
                #"Run2016C",
                #"Run2016D",
                #"Run2016E",
                #"Run2016F",
                #"Run2016G",
                #"Run2016H",
                "Run2017B",
                "Run2017C",
                "Run2017D",
                "Run2017E",
                "Run2017F",
                #"Run2018A",
                #"Run2018B",
                #"Run2018C",
                #"Run2018D",
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
    else:
        periods += [
                #"Summer16",
                "Fall17",
                #"Autumn18",
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
                #"h_tracks_reco_rebinned",                     
                #"h_tracks_reco_rebinned_short",
                #"h_tracks_reco_rebinned_long",
                #"h_tracks_rereco_rebinned",
                #"h_tracks_rereco_rebinned_short",
                #"h_tracks_rereco_rebinned_long",
                #"h_tracks_tagged_rebinned",                   
                #"h_tracks_tagged_rebinned_short",                
                #"h_tracks_tagged_rebinned_long",
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

    # calculated histograms:
    finaleff_global = {}
    finaleff_reco = {}
    finaleff_tag = {}

    finaleff_global_num = {}
    finaleff_reco_num = {}
    finaleff_tag_num = {}
    finaleff_global_denom = {}
    finaleff_reco_denom = {}
    finaleff_tag_denom = {}

    h_sf_global = {}
    h_sf_reco = {}
    h_sf_tag = {}
    g1_global = {}
    g1_reco = {}
    g1_tag = {}
    
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
    
    for category in ["_short", "_long"]:
            
        finaleff_global[category] = {}
        finaleff_reco[category] = {}
        finaleff_tag[category] = {}

        if lumiweighted:
            #finaleff_global_num[category] =   {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            #finaleff_reco_num[category] =     {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            #finaleff_tag_num[category] =      {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            #finaleff_global_denom[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            #finaleff_reco_denom[category] =   {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            #finaleff_tag_denom[category] =    {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            finaleff_global_num[category] =   {"Run2017": False, "Fall17": False}
            finaleff_reco_num[category] =     {"Run2017": False, "Fall17": False}
            finaleff_tag_num[category] =      {"Run2017": False, "Fall17": False}
            finaleff_global_denom[category] = {"Run2017": False, "Fall17": False}
            finaleff_reco_denom[category] =   {"Run2017": False, "Fall17": False}
            finaleff_tag_denom[category] =    {"Run2017": False, "Fall17": False}
        
        def fill_num_denom(i_finaleff, i_year, i_category, i_value):
            if not i_finaleff[i_category][i_year]:
                i_finaleff[i_category][i_year] = i_value
            else:
                i_finaleff[i_category][i_year].Add(i_value)
            
    
        for period in periods:
            
            print category, period
            
            if "Run201" in period and "rw" not in period:
                if "Run2016" in period: year = "Run2016"
                if "Run2017" in period: year = "Run2017"
                if "Run2018" in period: year = "Run2018"
            else:
                if "Summer16" in period: year = "Summer16"
                if "Fall17" in period:   year = "Fall17"
                if "Autumn18" in period: year = "Autumn18"
            
            ########################
            
            num = finaleff_global[category][period] = hists[period]["h_tracks_tagged" + category].Clone()
            denom = hists[period]["h_tracks_reco" + category].Clone()
            if lumiweighted:
                if "Run201" in period and "rw" not in period:
                    scalefactor = official_lumis[period]
                else:
                    scalefactor = 1.0
                if denom.Integral()>0:
                    num.Scale(scalefactor/denom.Integral())
                    denom.Scale(scalefactor/denom.Integral())                
                fill_num_denom(finaleff_global_num, year, category, num)
                fill_num_denom(finaleff_global_denom, year, category, denom)
            
            finaleff_global[category][period] = num.Clone()
            finaleff_global[category][period].Divide(denom)
                                  
            ########################
                                    
            num = finaleff_reco[category][period] = hists[period]["h_tracks_rereco" + category].Clone()
            denom = hists[period]["h_tracks_reco" + category].Clone()
            if lumiweighted:
                if "Run201" in period and "rw" not in period:
                    scalefactor = official_lumis[period]
                else:
                    scalefactor = 1.0
                if denom.Integral()>0:
                    num.Scale(scalefactor/denom.Integral())
                    denom.Scale(scalefactor/denom.Integral())
                fill_num_denom(finaleff_reco_num, year, category, num)
                fill_num_denom(finaleff_reco_denom, year, category, denom)
            
            finaleff_reco[category][period] = num.Clone()
            finaleff_reco[category][period].Divide(denom)

            ########################
            
            num = finaleff_tag[category][period] = hists[period]["h_tracks_tagged" + category].Clone()
            denom = hists[period]["h_tracks_rereco" + category].Clone()
            if lumiweighted:
                if "Run201" in period and "rw" not in period:
                    scalefactor = official_lumis[period]
                else:
                    scalefactor = 1.0
                if denom.Integral()>0:
                    num.Scale(scalefactor/denom.Integral())
                    denom.Scale(scalefactor/denom.Integral())
                fill_num_denom(finaleff_tag_num, year, category, num)
                fill_num_denom(finaleff_tag_denom, year, category, denom)
            
            finaleff_tag[category][period] = num.Clone()
            finaleff_tag[category][period].Divide(denom)
                    
        h_sf_global[category] = {}
        h_sf_reco[category] = {}
        h_sf_tag[category] = {}
        g1_global[category] = {}
        g1_reco[category] = {}
        g1_tag[category] = {}

        # lumiweighting: add numerators and denumerators:
        if lumiweighted:
            
            # reset
            finaleff_global[category] = {}
            finaleff_reco[category] = {}
            finaleff_tag[category] = {}
                        
            for period in finaleff_global_num[category].keys():
                finaleff_global[category][period] = finaleff_global_num[category][period].Clone()
                finaleff_global[category][period].Divide(finaleff_global_denom[category][period].Clone())
                
                finaleff_reco[category][period] = finaleff_reco_num[category][period].Clone()
                finaleff_reco[category][period].Divide(finaleff_reco_denom[category][period].Clone())
                
                finaleff_tag[category][period] = finaleff_tag_num[category][period].Clone()
                finaleff_tag[category][period].Divide(finaleff_tag_denom[category][period].Clone())
        
        
        if lumiweighted:
            this_periods = finaleff_global_num[category].keys()
        else:
            this_periods = periods
        
        for period in this_periods:
        
            print category, period
        
            if "rw" in period: continue
            if "Run201" not in period: continue
            
            if not options.mc_reweighted or lumiweighted:
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
            
            g1_global[category][period] = TF1( 'g1_global', '[0]',  3,  20 )
            h_sf_global[category][period] = finaleff_global[category][period].Clone()
            h_sf_global[category][period].Divide(finaleff_global[category][mcperiod])
            fit = h_sf_global[category][period].Fit(g1_global[category][period], "Q", "same", 3, 20)
            fitresults["fit_sf"][period + category] = g1_global[category][period].GetParameter(0)
            if "short" in category:
                fitresults["fit_uncert"][period + category] = h_sf_global[category][period].GetBinError(4)
            else:
                fitresults["fit_uncert"][period + category] = h_sf_global[category][period].GetBinError(6)
            
            g1_reco[category][period] = TF1( 'g1_reco', '[0]',  3,  20 )
            h_sf_reco[category][period] = finaleff_reco[category][period].Clone()
            h_sf_reco[category][period].Divide(finaleff_reco[category][mcperiod])
            fit = h_sf_reco[category][period].Fit(g1_reco[category][period], "Q", "same", 3, 20)
            fitresults["fit_sfreco"][period + category] = g1_reco[category][period].GetParameter(0)
            if "short" in category:
                fitresults["fit_uncertreco"][period + category] = h_sf_reco[category][period].GetBinError(4)
            else:
                fitresults["fit_uncertreco"][period + category] = h_sf_reco[category][period].GetBinError(6)
            
            g1_tag[category][period] = TF1( 'g1_tag', '[0]',  3,  20 )
            h_sf_tag[category][period] = finaleff_tag[category][period].Clone()
            h_sf_tag[category][period].Divide(finaleff_tag[category][mcperiod])
            fit = h_sf_tag[category][period].Fit(g1_tag[category][period], "Q", "same", 3, 20)
            fitresults["fit_sftag"][period + category] = g1_tag[category][period].GetParameter(0)
            if "short" in category:
                fitresults["fit_uncerttag"][period + category] = h_sf_tag[category][period].GetBinError(4)
            else:
                fitresults["fit_uncerttag"][period + category] = h_sf_tag[category][period].GetBinError(6)
                            

    # plot SF:

    for category in ["short", "long"]:

        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.47, y1=0.65, x2=0.85, y2=0.85)
        legend.SetHeader("%s tracks" % category)
        legend.SetTextSize(0.035)
            
        h_sf_short = {}
        h_sf_long = {}
            
        for label in ["fit_sf", "fit_sfreco", "fit_sftag"]:
            
            if lumiweighted:
                h_sf_short[label] = TH1F("h_sf_short[label]", "", 3, 0, 3)
                h_sf_long[label] = TH1F("h_sf_long[label]", "", 3, 0, 3)
            else:
                h_sf_short[label] = TH1F("h_sf_short[label]", "", 16, 0, 16)
                h_sf_long[label] = TH1F("h_sf_long[label]", "", 16, 0, 16)
        
            shared_utils.histoStyler(h_sf_short[label])
            shared_utils.histoStyler(h_sf_long[label])    
            
            i_short = 0
            i_long = 0
            binlabels_short = []
            binlabels_long = []
            
            for i, period in enumerate(sorted(fitresults[label])):
                
                sf = fitresults[label][period]
                uncert = fitresults[label.replace("_sf", "_uncert")][period]
                                    
                if "short" in period:
                    h_sf_short[label].SetBinContent(i_short + 1, sf)
                    h_sf_short[label].SetBinError(i_short + 1, uncert)
                    i_short +=1
                    binlabels_short.append(period.replace("Run", "").replace("_short", "").replace("_long", ""))
                    print "Adding", label, period, sf, uncert
                elif "long" in period:
                    h_sf_long[label].SetBinContent(i_long + 1, sf)
                    h_sf_long[label].SetBinError(i_long + 1, uncert)
                    i_long += 1
                    binlabels_long.append(period.replace("Run", "").replace("_short", "").replace("_long", ""))
                    print "Adding", label, period, sf, uncert
                    
            if category == "short":      
                if label == "fit_sf":
                    h_sf_short[label].Draw("hist e")
                else:
                    h_sf_short[label].Draw("hist e same")
                
                if "reco" in label:
                    h_sf_short[label].SetTitle(";;fitted track reconstruction scale factor")
                elif "tag" in label:
                    h_sf_short[label].SetTitle(";;fitted track tagging scale factor")
                else:
                    h_sf_short[label].SetTitle(";;fitted scale factor")
                h_sf_short[label].GetYaxis().SetRangeUser(0.0, 2.0)
            else:
                if label == "fit_sf":
                    h_sf_long[label].Draw("hist e")
                else:
                    h_sf_long[label].Draw("hist e same")
                
                if "reco" in label:
                    h_sf_long[label].SetTitle(";;fitted track reconstruction scale factor")
                elif "tag" in label:
                    h_sf_long[label].SetTitle(";;fitted track tagging scale factor")
                else:
                    h_sf_long[label].SetTitle(";;fitted scale factor")
                h_sf_long[label].GetYaxis().SetRangeUser(0.0, 2.0)
                
            if label == "fit_sf":
                #h_sf_short[label].SetLineStyle(1)
                #h_sf_long[label].SetLineStyle(1)
                h_sf_short[label].SetLineWidth(3)
                h_sf_long[label].SetLineWidth(3)
                h_sf_short[label].SetLineColor(kRed)            
                h_sf_long[label].SetLineColor(kBlue)
                if category == "short": legend.AddEntry(h_sf_short[label], "combined SF")
                else: legend.AddEntry(h_sf_long[label], "combined SF")
            if label == "fit_sfreco":
                #h_sf_short[label].SetLineStyle(2)
                #h_sf_long[label].SetLineStyle(2)
                h_sf_short[label].SetLineColor(97)            
                h_sf_long[label].SetLineColor(62)
                if category == "short": legend.AddEntry(h_sf_short[label], "reconstruction SF")
                else: legend.AddEntry(h_sf_long[label], "reconstruction SF")
            elif label == "fit_sftag":
                h_sf_short[label].SetLineStyle(2)
                h_sf_long[label].SetLineStyle(2)
                h_sf_short[label].SetLineColor(97)            
                h_sf_long[label].SetLineColor(62)
                if category == "short": legend.AddEntry(h_sf_short[label], "tagging SF")
                else: legend.AddEntry(h_sf_long[label], "tagging SF")
                
            print binlabels_short
            print binlabels_long
            
            for i, i_binlabel in enumerate(binlabels_short):
                h_sf_short[label].GetXaxis().SetBinLabel(i + 1, i_binlabel)    
            for i, i_binlabel in enumerate(binlabels_long):
                h_sf_long[label].GetXaxis().SetBinLabel(i + 1, i_binlabel)    
            
            if "lumi" not in label:
                h_sf_short[label].GetXaxis().SetTitleSize(0.04)
                h_sf_short[label].GetXaxis().SetLabelSize(0.04)   
            else:
                print "lumilumi"
                h_sf_short[label].GetXaxis().SetLabelSize(0.09)
            
        legend.Draw()
        
        shared_utils.stamp()
        
        pdfname = "%s/allperiods_sf_combined_%s.pdf" % (plotfolder, category)
        
        if options.mc_reweighted:
            pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
        if lumiweighted:
            pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")
        
        canvas.SaveAs(pdfname)
        
        #fout = TFile(pdfname.replace(".pdf", ".root"), "recreate")
        #canvas.Write()
        #h_sf_short.SetName("h_scalefactor_short")
        #h_sf_short.Write()
        #h_sf_long.SetName("h_scalefactor_long")
        #h_sf_long.Write()
        #fout.Close()
        
    
    # plot underlying efficiencies and SFs:
       
    for i_finaleff, finaleff in enumerate([finaleff_global, finaleff_reco, finaleff_tag]):
     
        for year in ["2016", "2017", "2018"]:
        
            for category in ["_short", "_long"]:
                
                canvas = shared_utils.mkcanvas()
                legend = shared_utils.mklegend(x1=0.6, y1=0.6, x2=0.85, y2=0.85)
                legend.SetHeader("%s tracks (%s)" % (category.replace("_", ""), year))
                legend.SetTextSize(0.035)
                
                #colors = range(209,270)[::2]
                #colors = ["kBlack", "kRed", "kOrange", "kBlue", "kAzure", "kTeal", "kGreen", "kGreen"+2, ] 
                colors = [kBlack, 97, 94, 91, 86, 81, 70, 65, 61, 51]
                
                for i_period, period in enumerate(this_periods):
                    
                    #if "Run" in period:
                    #    if "B" not in period: continue
                    
                    if "rw" in period: continue
                    
                    if year == "2016":
                        mcperiod = "Summer16"
                    elif year == "2017":
                        mcperiod = "Fall17"
                    elif year == "2018":
                        mcperiod = "Autumn18"
                    
                    if period == mcperiod or year in period:
                    
                        #color = colors.pop(0)
                        color = kBlack
                        
                        if i_period == 0:
                            #drawoption = "hist e"
                            drawoption = "p e"
                        else:
                            drawoption = "hist e same"

                        if period != mcperiod:
                            finaleff[category][period].SetMarkerStyle(20)
                        
                        print finaleff
                        print finaleff[category].keys()
                        
                        finaleff[category][period].Draw(drawoption)
                        finaleff[category][period].SetLineColor(color)
                        finaleff[category][period].SetLineStyle(1)
                        finaleff[category][period].SetTitle(";number of remaining tracker layers;efficiency, scale factor")
                        finaleff[category][period].GetXaxis().SetRangeUser(0, 20)
                        finaleff[category][period].GetYaxis().SetRangeUser(0, 2.0)
                        
                        legend.AddEntry(finaleff[category][period], period)
                        
                        if "Run" in period and "rw" not in period:
                                 
                            color = kBlue
                                 
                            if i_finaleff == 0: 
                                h_sf_global[category][period].Draw("e same")
                                h_sf_global[category][period].SetLineColor(color)
                                h_sf_global[category][period].SetLineWidth(2)
                                g1_global[category][period].Draw("same")
                                g1_global[category][period].SetLineColor(color)
                                g1_global[category][period].SetLineWidth(2)
                                legend.AddEntry(g1_global[category][period], "scale factor")
                            elif i_finaleff == 1: 
                                h_sf_reco[category][period].Draw("e same")
                                h_sf_reco[category][period].SetLineColor(color)
                                h_sf_reco[category][period].SetLineWidth(2)
                                g1_reco[category][period].Draw("same")
                                g1_reco[category][period].SetLineColor(color)
                                g1_reco[category][period].SetLineWidth(2)
                                legend.AddEntry(g1_reco[category][period], "scale factor")
                            elif i_finaleff == 2: 
                                h_sf_tag[category][period].Draw("e same")
                                h_sf_tag[category][period].SetLineColor(color)
                                h_sf_tag[category][period].SetLineWidth(2)
                                g1_tag[category][period].Draw("same")
                                g1_tag[category][period].SetLineColor(color)
                                g1_tag[category][period].SetLineWidth(2)
                                legend.AddEntry(g1_tag[category][period], "scale factor")
                                
                    
                legend.Draw()
                shared_utils.stamp()
        
                if i_finaleff == 0:        
                    pdfname = "%s/underlying%s%s.pdf" % (plotfolder, category, year)
                elif i_finaleff == 1:        
                    pdfname = "%s/underlying_reco%s%s.pdf" % (plotfolder, category, year)
                elif i_finaleff == 2:        
                    pdfname = "%s/underlying_tag%s%s.pdf" % (plotfolder, category, year)
                
                if options.mc_reweighted:
                    pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
                if lumiweighted:
                    pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")
                
                canvas.SaveAs(pdfname)
        
        
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "MCReweighted")
    parser.add_option("--mcsuffix", dest = "mcsuffix", default = "")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")
    parser.add_option("--reweighted", dest = "mc_reweighted", action = "store_true")

    (options, args) = parser.parse_args()

    for lumiweighted in [False, True]:
                
        main(options, lumiweighted)
        
