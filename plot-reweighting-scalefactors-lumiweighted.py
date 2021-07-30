#!/bin/env python
import os
import glob
import shared_utils
import math
from ROOT import *
from optparse import OptionParser

def histoadd(dictentry, histogram):
    if dictentry == 0:
        dictentry = histogram.Clone()
    else:
        dictentry.Add(histogram)
    return dictentry
    
        
if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    parser = OptionParser()

    #parser.add_option("--suffix", dest = "suffix", default = "EquXsecMay")
    #parser.add_option("--histofolder", dest = "histofolder", default = "histograms_oldtag")
    
    parser.add_option("--suffix", dest = "suffix", default = "MCReweighting")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")

    (options, args) = parser.parse_args()
    
    histofolder = options.histofolder
    suffix = options.suffix
    
    plotfolder = "plots%s_new" % options.suffix
    os.system("mkdir -p %s" % plotfolder)

    mc_reweighted = False   

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
              
    if mc_reweighted:
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
    
    fitresults = {}
    fitresults["fit_sf"] = {}
    fitresults["fit_uncert"] = {}
    fitresults["fit_sfreco"] = {}
    fitresults["fit_uncertreco"] = {}
    fitresults["fit_sftag"] = {}
    fitresults["fit_uncerttag"] = {}
    
    # global SF:
    for category in ["_short", "_long"]:
        
        # get numerators, denominators:
        global_numerators = {}
        global_denominators = {}
        reco_numerators = {}
        reco_denominators = {}
        tag_numerators = {}
        tag_denominators = {}
                
        for period in periods:
            global_numerators[period] = hists[period]["h_tracks_tagged" + category].Clone()
            global_denominators[period] = hists[period]["h_tracks_reco" + category].Clone()
            reco_numerators[period] = hists[period]["h_tracks_rereco" + category].Clone()
            reco_denominators[period] = hists[period]["h_tracks_reco" + category].Clone()
            tag_numerators[period] = hists[period]["h_tracks_tagged" + category].Clone()
            tag_denominators[period] = hists[period]["h_tracks_rereco" + category].Clone()
        
            #scale global:
            if "rw" not in period and "Run201" in period:
                global_numerators[period].Scale(official_lumis[period]/global_denominators[period].Integral())
                global_denominators[period].Scale(official_lumis[period]/global_denominators[period].Integral())
            else:
                global_numerators[period].Scale(1.0/global_denominators[period].Integral())
                global_denominators[period].Scale(1.0/global_denominators[period].Integral())

            #scale reco:
            if "rw" not in period and "Run201" in period:
                reco_numerators[period].Scale(official_lumis[period]/reco_denominators[period].Integral())
                reco_denominators[period].Scale(official_lumis[period]/reco_denominators[period].Integral())
            else:
                reco_numerators[period].Scale(1.0/reco_denominators[period].Integral())
                reco_denominators[period].Scale(1.0/reco_denominators[period].Integral())

            #scale tag:
            if "rw" not in period and "Run201" in period:
                tag_numerators[period].Scale(official_lumis[period]/tag_denominators[period].Integral())
                tag_denominators[period].Scale(official_lumis[period]/tag_denominators[period].Integral())
            else:
                tag_numerators[period].Scale(1.0/tag_denominators[period].Integral())
                tag_denominators[period].Scale(1.0/tag_denominators[period].Integral())
        
        data_global_numerators_added = {"2016": 0, "2017": 0, "2018": 0}
        data_global_denominators_added = {"2016": 0, "2017": 0, "2018": 0}
        data_reco_numerators_added = {"2016": 0, "2017": 0, "2018": 0}
        data_reco_denominators_added = {"2016": 0, "2017": 0, "2018": 0}
        data_tag_numerators_added = {"2016": 0, "2017": 0, "2018": 0}
        data_tag_denominators_added = {"2016": 0, "2017": 0, "2018": 0}
        
        mc_global_numerators_added = {"2016": 0, "2017": 0, "2018": 0}
        mc_global_denominators_added = {"2016": 0, "2017": 0, "2018": 0}
        mc_reco_numerators_added = {"2016": 0, "2017": 0, "2018": 0}
        mc_reco_denominators_added = {"2016": 0, "2017": 0, "2018": 0}
        mc_tag_numerators_added = {"2016": 0, "2017": 0, "2018": 0}
        mc_tag_denominators_added = {"2016": 0, "2017": 0, "2018": 0}
        
        # now, add Data:
        for period in periods:
            for year in ["2016", "2017", "2018"]:
                if year in period and "rw" not in period and "Run201" in period:
                    data_global_numerators_added[year] = histoadd(data_global_numerators_added[year], global_numerators[period])
                    data_global_denominators_added[year] = histoadd(data_global_denominators_added[year], global_denominators[period])
                    data_reco_numerators_added[year] = histoadd(data_reco_numerators_added[year], reco_numerators[period])
                    data_reco_denominators_added[year] = histoadd(data_reco_denominators_added[year], reco_denominators[period])
                    data_tag_numerators_added[year] = histoadd(data_tag_numerators_added[year], tag_numerators[period])
                    data_tag_denominators_added[year] = histoadd(data_tag_denominators_added[year], tag_denominators[period])
        
        # now, add reweighted MC:
        if mc_reweighted:
            for period in periods:
                for year in ["2016", "2017", "2018"]:
                    if year in period and "rw" in period:
                        mc_global_numerators_added[year] = histoadd(mc_global_numerators_added[year], global_numerators[period])
                        mc_global_denominators_added[year] = histoadd(mc_global_denominators_added[year], global_denominators[period])
                        mc_reco_numerators_added[year] = histoadd(mc_reco_numerators_added[year], reco_numerators[period])
                        mc_reco_denominators_added[year] = histoadd(mc_reco_denominators_added[year], reco_denominators[period])
                        mc_tag_numerators_added[year] = histoadd(mc_tag_numerators_added[year], tag_numerators[period])
                        mc_tag_denominators_added[year] = histoadd(mc_tag_denominators_added[year], tag_denominators[period])
        else:
            for year in ["2016", "2017", "2018"]:
                if year == "2016": period == "Summer16"
                if year == "2017": period == "Fall17"
                if year == "2018": period == "Autumn18"
                mc_global_numerators_added[year] = global_numerators[period].Clone()
                mc_global_denominators_added[year] = global_denominators[period].Clone()
                mc_reco_numerators_added[year] = reco_numerators[period].Clone()
                mc_reco_denominators_added[year] = reco_denominators[period].Clone()
                mc_tag_numerators_added[year] = tag_numerators[period].Clone()
                mc_tag_denominators_added[year] = tag_denominators[period].Clone()
    
        # do ratios:
        data_ratio_global = {}
        data_ratio_reco = {}
        data_ratio_tag = {}
        mc_ratio_global = {}
        mc_ratio_reco = {}
        mc_ratio_tag = {}
        
        for year in ["2016", "2017", "2018"]:
            data_ratio_global[year] = data_global_numerators_added[year].Clone()
            data_ratio_global[year].Divide(data_global_denominators_added[year])
            data_ratio_reco[year] = data_reco_numerators_added[year].Clone()
            data_ratio_reco[year].Divide(data_reco_denominators_added[year])
            data_ratio_tag[year] = data_tag_numerators_added[year].Clone()
            data_ratio_tag[year].Divide(data_tag_denominators_added[year])
            mc_ratio_global[year] = mc_global_numerators_added[year].Clone()
            mc_ratio_global[year].Divide(mc_global_denominators_added[year])
            mc_ratio_reco[year] = mc_reco_numerators_added[year].Clone()
            mc_ratio_reco[year].Divide(mc_reco_denominators_added[year])
            mc_ratio_tag[year] = mc_tag_numerators_added[year].Clone()
            mc_ratio_tag[year].Divide(mc_tag_denominators_added[year])
        
    
        # scale factors:
        h_sf_global = {}
        h_sf_reco = {}
        h_sf_tag = {}
        sf_global = {}
        sf_reco = {}
        sf_tag = {}
        
        for year in ["2016", "2017", "2018"]:
            h_sf_global[year] = data_ratio_global[year].Clone()
            h_sf_reco[year] = data_ratio_reco[year].Clone()
            h_sf_tag[year] = data_ratio_tag[year].Clone()

            h_sf_global[year].Divide(mc_ratio_global[year])
            h_sf_reco[year].Divide(mc_ratio_reco[year])
            h_sf_tag[year].Divide(mc_ratio_tag[year])

        # fit:
        for year in ["2016", "2017", "2018"]:
            
            g1 = TF1( 'g1', '[0]',  3,  20 )
            fit = h_sf_global[year].Fit(g1, "Q", "same", 3, 20)
            sf_global[year] = g1.GetParameter(0)
            fitresults["fit_sf"][year + category] = g1.GetParameter(0)
            fitresults["fit_uncert"][year + category] = 0.1
            
                
            g1 = TF1( 'g1', '[0]',  3,  20 )
            fit = h_sf_reco[year].Fit(g1, "Q", "same", 3, 20)
            sf_reco[year] = g1.GetParameter(0)
            fitresults["fit_sfreco"][year + category] = g1.GetParameter(0)
            fitresults["fit_uncertreco"][year + category] = 0.1
            
            g1 = TF1( 'g1', '[0]',  3,  20 )
            fit = h_sf_tag[year].Fit(g1, "Q", "same", 3, 20)
            sf_tag[year] = g1.GetParameter(0)
            fitresults["fit_sftag"][year + category] = g1.GetParameter(0)
            fitresults["fit_uncerttag"][year + category] = 0.1
            
            
        print "*** %s tracks ***" % category
        print "sf_global", sf_global
        print "sf_reco", sf_reco
        print "sf_tag", sf_tag
        
        
        
    # plot:
    
    for label in ["fit_sf", "fit_sfreco", "fit_sftag"]:
    
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.6, y1=0.7, x2=0.85, y2=0.85)
        legend.SetHeader(suffix)
        
        h_sf_short = TH1F("h_sf_short", "", 3, 0, 3)
        h_sf_long = TH1F("h_sf_long", "", 3, 0, 3)
        #h_sf_short = TH1F("h_sf_short", "", 16, 0, 16)
        #h_sf_long = TH1F("h_sf_long", "", 16, 0, 16)
        
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
        
        #if "lumi" not in label:
        #    h_sf_short.GetXaxis().SetTitleSize(0.04)
        #    h_sf_short.GetXaxis().SetLabelSize(0.04)   
        #else:
        #    print "lumilumi"
        #    #h_sf_short.GetXaxis().SetTitleSize(1.2)
        #    h_sf_short.GetXaxis().SetLabelSize(0.1)
        h_sf_short.GetXaxis().SetLabelSize(0.09)
        
        legend.Draw()
        
        shared_utils.stamp()
        
        pdfname = "%s/allperiods_sf_%s_lumiweighted.pdf" % (plotfolder, label)
        
        if mc_reweighted:
            pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
        
        canvas.SaveAs(pdfname)
        
        fout = TFile(pdfname.replace(".pdf", ".root"), "recreate")
        canvas.Write()
        h_sf_short.SetName("h_scalefactor_short")
        h_sf_short.Write()
        h_sf_long.SetName("h_scalefactor_long")
        h_sf_long.Write()
        fout.Close()
    