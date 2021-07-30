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
    parser.add_option("--lumiweighted", dest = "lumiweighted", action = "store_true")
    parser.add_option("--all", dest = "all", action = "store_true")

    (options, args) = parser.parse_args()

    if options.all:
        os.system("./plot-reweighting-scalefactors-and-efficiencies.py --suffix ShortsRedefinedV3 --lumiweighted &")
        os.system("./plot-reweighting-scalefactors-and-efficiencies.py --suffix ShortsBaselineV3 --lumiweighted &")
        os.system("./plot-reweighting-scalefactors-and-efficiencies.py --suffix ShortsCombinedV3 --lumiweighted &")
        os.system("./plot-reweighting-scalefactors-and-efficiencies.py --suffix ShortsRedefinedV3 &")
        os.system("./plot-reweighting-scalefactors-and-efficiencies.py --suffix ShortsBaselineV3 &")
        os.system("./plot-reweighting-scalefactors-and-efficiencies.py --suffix ShortsCombinedV3 &")
        quit()

    histofolder = options.histofolder
    suffix = options.suffix
    
    plotfolder = "plots%s_new2" % options.suffix
    if options.mcsuffix != "":
        plotfolder = plotfolder.replace("_new2", "_%s_new2" % options.mcsuffix)
    
    os.system("mkdir -p %s" % plotfolder)

    periods = [
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
    else:
        periods += [
                "Summer16",
                "Fall17",
                "Autumn18",
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

        if options.lumiweighted:
            finaleff_global_num[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            finaleff_reco_num[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            finaleff_tag_num[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            finaleff_global_denom[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            finaleff_reco_denom[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
            finaleff_tag_denom[category] = {"Run2016": False, "Run2017": False, "Run2018": False, "Summer16": False, "Fall17": False, "Autumn18": False}
        
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
            if options.lumiweighted:
                if "Run201" in period and "rw" not in period:
                    scalefactor = official_lumis[period]
                else:
                    scalefactor = 1.0
                num.Scale(scalefactor/denom.Integral())
                denom.Scale(scalefactor/denom.Integral())                
                fill_num_denom(finaleff_global_num, year, category, num)
                fill_num_denom(finaleff_global_denom, year, category, denom)
            
            finaleff_global[category][period] = num.Clone()
            finaleff_global[category][period].Divide(denom)
                                  
            ########################
                                    
            num = finaleff_reco[category][period] = hists[period]["h_tracks_rereco" + category].Clone()
            denom = hists[period]["h_tracks_reco" + category].Clone()
            if options.lumiweighted:
                if "Run201" in period and "rw" not in period:
                    scalefactor = official_lumis[period]
                else:
                    scalefactor = 1.0
                num.Scale(scalefactor/denom.Integral())
                denom.Scale(scalefactor/denom.Integral())
                fill_num_denom(finaleff_reco_num, year, category, num)
                fill_num_denom(finaleff_reco_denom, year, category, denom)
            
            finaleff_reco[category][period] = num.Clone()
            finaleff_reco[category][period].Divide(denom)

            ########################
            
            num = finaleff_tag[category][period] = hists[period]["h_tracks_tagged" + category].Clone()
            denom = hists[period]["h_tracks_rereco" + category].Clone()
            if options.lumiweighted:
                if "Run201" in period and "rw" not in period:
                    scalefactor = official_lumis[period]
                else:
                    scalefactor = 1.0
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
        if options.lumiweighted:
            
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
        
        
        if options.lumiweighted:
            this_periods = finaleff_global_num[category].keys()
        else:
            this_periods = periods
        
        for period in this_periods:
        
            print category, period
        
            if "rw" in period: continue
            if "Run201" not in period: continue
            
            if not options.mc_reweighted or options.lumiweighted:
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
    
    for label in ["fit_sf", "fit_sfreco", "fit_sftag"]:
    
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.6, y1=0.7, x2=0.85, y2=0.85)
        legend.SetTextSize(0.035)
        legend.SetHeader(suffix)
        
        if options.lumiweighted:
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
            h_sf_short.GetXaxis().SetTitleSize(0.5)
            h_sf_short.GetXaxis().SetLabelSize(0.09)
        
        legend.Draw()
        
        shared_utils.stamp()
        
        pdfname = "%s/allperiods_sf_%s.pdf" % (plotfolder, label)
        
        if options.mc_reweighted:
            pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
        if options.lumiweighted:
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
                
                    color = colors.pop(0)
                    
                    if i_period == 0:
                        drawoption = "hist e"
                    else:
                        drawoption = "hist e same"
                    
                    print finaleff_global
                    print finaleff_global[category].keys()
                    
                    finaleff_global[category][period].Draw(drawoption)
                    finaleff_global[category][period].SetLineColor(color)
                    finaleff_global[category][period].SetLineStyle(1)
                    finaleff_global[category][period].SetTitle(";number of remaining tracker layers;efficiency, scale factor")
                    finaleff_global[category][period].GetXaxis().SetRangeUser(0,20)
                    finaleff_global[category][period].GetYaxis().SetRangeUser(0,1.5)
                    
                    legend.AddEntry(finaleff_global[category][period], period)
                    
                    if "Run" in period and "rw" not in period:
                                                
                        h_sf_global[category][period].Draw("e same")
                        h_sf_global[category][period].SetLineColor(color)
                        h_sf_global[category][period].SetLineWidth(3)

                        g1_global[category][period].Draw("same")
                        g1_global[category][period].SetLineColor(color)
                        g1_global[category][period].SetLineWidth(3)
                
            legend.Draw()
            shared_utils.stamp()

            pdfname = "%s/underlying%s%s.pdf" % (plotfolder, category, year)
            if options.mc_reweighted:
                pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
            if options.lumiweighted:
                pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")
            
            canvas.SaveAs(pdfname)
        
        
                             