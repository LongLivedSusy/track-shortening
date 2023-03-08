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

def main(options):
    
    histofolder = options.histofolder
    suffix = options.suffix  
    plotfolder = "plots_%s" % options.suffix
    
    os.system("mkdir -p %s" % plotfolder)
             
    if options.mc_reweighted:
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
                "Run2016",
                "Run2017",
                "Run2018",
                "Summer16",
                "Fall17",
                "Autumn18",
                   ]        
    
    exact = "layers_remaining==track_trackerLayersWithMeasurement && "
    
    cuts = {
               "baseline": {
                             "base_cuts":    "layers_remaining>=3 && ",
                             "taggedextra":  "track_minDeltaR>1 && ",
                             "legendheader": "baseline",
                           },
               #"lowdxydz": {
               #              "base_cuts":    "layers_remaining>=3 && ",
               #              "taggedextra":  "track_dxyVtx<0.01 && track_dzVtx<0.01 && ",
               #              "legendheader": "lowdxydz",
               #            },
           }

    if not options.get_from_tree:
        cuts = {
               "baseline": {
                             "base_cuts":    "",
                             "taggedextra":  "",
                             "legendheader": "baseline",
                           },
               }

    for cut_label in cuts:

        if options.weightkinematic:
            cuts[cut_label]["base_cuts"] += " weight_kinematicMLP2>0 && "
        elif options.weighttrackprop:
            cuts[cut_label]["base_cuts"] += " weight_trackpropMLP2>0 && "        

        histolabels = {
                    "h_tracks_reco":            ["h_tracks_reco", cuts[cut_label]["base_cuts"] + "track_reco==1", 1, 1, 2],
                    "h_tracks_rereco":          ["h_tracks_rereco_exact", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_rereco==1 && track_is_pixel_track==1", 1, 1, 2],
                    "h_tracks_rereco_short":    ["h_tracks_rereco_exact_short", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_rereco==1 && track_is_pixel_track==1", 1, 1, 2],
                    "h_tracks_rereco_long":     ["h_tracks_rereco_exact_long", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_rereco==1 && track_is_pixel_track==0", 1, 1, 2],
                    "h_tracks_tagged":          ["h_tracks_tagged_exact", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_preselected==1 && track_mva>0.1 && track_pt>25 && track_is_pixel_track==1 && (track_matchedCaloEnergy<15 || track_matchedCaloEnergy/track_p<0.15)", 1, 1, 2],
                    "h_tracks_tagged_short":    ["h_tracks_tagged_exact_short", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_preselected==1 && track_mva>0.1 && track_pt>25 && track_is_pixel_track==1 && (track_matchedCaloEnergy<15 || track_matchedCaloEnergy/track_p<0.15)", 1, 1, 2],
                    "h_tracks_tagged_long":     ["h_tracks_tagged_exact_long", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_preselected==1 && track_mva>0.1 && track_pt>40 && track_is_pixel_track==0 && (track_matchedCaloEnergy<15 || track_matchedCaloEnergy/track_p<0.15)", 1, 1, 2],
                    #"h_tracks_tagged_short":    ["track_reco", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_preselected==1 && track_tagged==1 && track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_long":     ["track_reco", cuts[cut_label]["base_cuts"] + cuts[cut_label]["taggedextra"] + exact + " track_preselected==1 && track_tagged==1 && track_is_pixel_track==0", 1, 1, 2],
                    #h_tracks_tagged_short":    ["track_reco", base_cutstagged + "track_tagged==1 && track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_short":   ["track_reco", base_cutstagged + "track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_short":   ["track_reco", base_cuts + exact + " abs(track_dxyVtx)<0.005 && abs(track_dzVtx)<0.005 && track_tagged==1 && track_pt>25 && track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_short":   ["track_reco", base_cuts + exact + base_cutstagged + " track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_short":   ["track_reco", exo + " && track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_short":   ["track_reco", base_cuts + "track_pt>25 && track_dxyVtx<0.001 && track_dzVtx<0.001 && track_tagged==1 && track_is_pixel_track==1", 1, 1, 2],
                    #"h_tracks_tagged_short":   ["track_reco", "track_rereco==1 && track_is_pixel_track==1 && " + exo, 1, 1, 2],
                      }
        
        categories = [
                      "_long",
                      "_short",
                      "",
                     ]

        # get all histos:
        hists = {}
        for period in periods:

            if "Run201" in period and "rw" not in period:
                is_data = False
            else:
                is_data = True

            hists[period] = {}
            for label in histolabels:
                print period, label

                filename = "%s/histograms%s_%s.root" % (histofolder, suffix, period)

                if options.get_from_tree:
                    tree = TChain("Events")
                    tree.Add(filename)

                    # apply weights before getting the histograms from the tree:
                    treecuts = "(%s)" % histolabels[label][1]
                    if not is_data and options.weightkinematic:
                        treecuts += "*weight_kinematicMLP2/(1.0-weight_kinematicMLP2)"
                    if not is_data and options.weighttrackprop:
                        treecuts += "*weight_trackpropMLP2/(1.0-weight_trackpropMLP2)"
                    if options.mc_reweighted:
                        treecuts += "*weight_ptreweighting"                      

                    hists[period][label] = plotting.get_histogram_from_tree(tree, histolabels[label][0], cutstring=treecuts, nBinsX=histolabels[label][2], xmin=histolabels[label][3], xmax=histolabels[label][4])
                    hists[period][label].SetDirectory(0)
                    hists[period][label].SetLineWidth(2)
                else:
                    fin = TFile(filename, "open")
                    print "%s/histograms%s_%s.root" % (histofolder, suffix, period)
                    hists[period][label] = fin.Get("Histograms/" + label)
                    hists[period][label].SetDirectory(0)
                    hists[period][label].SetLineWidth(2)
                    fin.Close()

                shared_utils.histoStyler(hists[period][label])

                
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
            
        for category in categories:

            # first, get efficiencies:
            
            finaleff_global[category] = {}
            finaleff_reco[category] = {}
            finaleff_tag[category] = {}

            finaleff_global_num[category] = {}
            finaleff_reco_num[category] = {}
            finaleff_tag_num[category] = {}

            finaleff_global_denom[category] = {}
            finaleff_reco_denom[category] = {}
            finaleff_tag_denom[category] = {}
     
            for period in periods:
                            
                finaleff_global_num[category][period] = hists[period]["h_tracks_tagged" + category].Clone()
                finaleff_global_denom[category][period] = hists[period]["h_tracks_reco" + category].Clone()
                finaleff_global[category][period] = finaleff_global_num[category][period].Clone()
                finaleff_global[category][period].Divide(finaleff_global_denom[category][period])
                                      
                finaleff_reco_num[category][period] = hists[period]["h_tracks_rereco" + category].Clone()
                finaleff_reco_denom[category][period] = hists[period]["h_tracks_reco" + category].Clone()
                finaleff_reco[category][period] = finaleff_reco_num[category][period].Clone()
                finaleff_reco[category][period].Divide(finaleff_reco_denom[category][period])
               
                finaleff_tag_num[category][period] = hists[period]["h_tracks_tagged" + category].Clone()
                finaleff_tag_denom[category][period] = hists[period]["h_tracks_rereco" + category].Clone()
                finaleff_tag[category][period] = finaleff_tag_num[category][period].Clone()
                finaleff_tag[category][period].Divide(finaleff_tag_denom[category][period])

            # get SF:

            h_sf_global[category] = {}
            h_sf_reco[category] = {}
            h_sf_tag[category] = {}
            g1_global[category] = {}
            g1_reco[category] = {}
            g1_tag[category] = {}

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

                if not options.get_from_tree:

                    print "fitting global SF..."
                    g1_global[category][period] = TF1( 'g1_global', '[0]',  3,  20 )
                    h_sf_global[category][period] = finaleff_global[category][period].Clone()
                    h_sf_global[category][period].Divide(finaleff_global[category][mcperiod])
                    fit = h_sf_global[category][period].Clone().Fit(g1_global[category][period], "", "same", 3, 20)
                    fitresults["fit_sf"][period + category] = g1_global[category][period].GetParameter(0)
                    if "short" in category:
                        fitresults["fit_uncert"][period + category] = h_sf_global[category][period].GetBinError(4)
                    else:
                        fitresults["fit_uncert"][period + category] = h_sf_global[category][period].GetBinError(6)

                    print "fitting reco SF..."
                    g1_reco[category][period] = TF1( 'g1_reco', '[0]',  3,  20 )
                    h_sf_reco[category][period] = finaleff_reco[category][period].Clone()
                    h_sf_reco[category][period].Divide(finaleff_reco[category][mcperiod])
                    fit = h_sf_reco[category][period].Clone().Fit(g1_reco[category][period], "", "same", 3, 20)
                    fitresults["fit_sfreco"][period + category] = g1_reco[category][period].GetParameter(0)
                    if "short" in category:
                        fitresults["fit_uncertreco"][period + category] = h_sf_reco[category][period].GetBinError(4)
                    else:
                        fitresults["fit_uncertreco"][period + category] = h_sf_reco[category][period].GetBinError(6)
                    
                    print "fitting tagging SF..."
                    g1_tag[category][period] = TF1( 'g1_tag', '[0]',  3,  20 )
                    h_sf_tag[category][period] = finaleff_tag[category][period].Clone()
                    h_sf_tag[category][period].Divide(finaleff_tag[category][mcperiod])
                    fit = h_sf_tag[category][period].Clone().Fit(g1_tag[category][period], "", "same", 3, 20)
                    fitresults["fit_sftag"][period + category] = g1_tag[category][period].GetParameter(0)
                    if "short" in category:
                        fitresults["fit_uncerttag"][period + category] = h_sf_tag[category][period].GetBinError(4)
                    else:
                        fitresults["fit_uncerttag"][period + category] = h_sf_tag[category][period].GetBinError(6)

                else:

                    # using the tree:
                    h_sf_global[category][period] = finaleff_global[category][period].Clone()
                    h_sf_global[category][period].Divide(finaleff_global[category][mcperiod])
                    fitresults["fit_sf"][period + category] = h_sf_global[category][period].GetBinContent(1)
                    fitresults["fit_uncert"][period + category] = h_sf_global[category][period].GetBinError(1)
                    
                    h_sf_reco[category][period] = finaleff_reco[category][period].Clone()
                    h_sf_reco[category][period].Divide(finaleff_reco[category][mcperiod])
                    fitresults["fit_sfreco"][period + category] = h_sf_reco[category][period].GetBinContent(1)
                    fitresults["fit_uncertreco"][period + category] = h_sf_reco[category][period].GetBinError(1)

                    h_sf_tag[category][period] = finaleff_tag[category][period].Clone()
                    h_sf_tag[category][period].Divide(finaleff_tag[category][mcperiod])
                    fitresults["fit_sftag"][period + category] = h_sf_tag[category][period].GetBinContent(1)
                    fitresults["fit_uncerttag"][period + category] = h_sf_tag[category][period].GetBinError(1)


            # Lumi-weighting:
            if options.lumiweighted:

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

                for runyear in ["Run2016", "Run2017", "Run2018"]:

                    print "runyear", runyear

                    fitresults["fit_sf"][runyear + category] = 0
                    fitresults["fit_uncert"][runyear + category] = 0
                    fitresults["fit_sfreco"][runyear + category] = 0
                    fitresults["fit_uncertreco"][runyear + category] = 0
                    fitresults["fit_sftag"][runyear + category] = 0
                    fitresults["fit_uncerttag"][runyear + category] = 0
                    h_sf_global[category][runyear] = 0
                    h_sf_reco[category][runyear] = 0
                    h_sf_tag[category][runyear] = 0

                    sum_lumi = 0.0
            
                    for lumiyear in official_lumis:
                        if runyear in lumiyear:

                            sum_lumi += official_lumis[lumiyear]

                            fitresults["fit_sf"][runyear + category] += fitresults["fit_sf"][lumiyear + category] * official_lumis[lumiyear]
                            fitresults["fit_uncert"][runyear + category] += fitresults["fit_uncert"][lumiyear + category] * official_lumis[lumiyear]
                            fitresults["fit_sfreco"][runyear + category] += fitresults["fit_sfreco"][lumiyear + category] * official_lumis[lumiyear]
                            fitresults["fit_uncertreco"][runyear + category] += fitresults["fit_uncertreco"][lumiyear + category] * official_lumis[lumiyear]
                            fitresults["fit_sftag"][runyear + category] += fitresults["fit_sftag"][lumiyear + category] * official_lumis[lumiyear]
                            fitresults["fit_uncerttag"][runyear + category] += fitresults["fit_uncerttag"][lumiyear + category] * official_lumis[lumiyear]

                            #canvas = shared_utils.mkcanvas()
                            #h_sf_global[category][lumiyear].Draw("hist")
                            #canvas.Print("hi.pdf")
                            #quit()

                            h_tmp_global = h_sf_global[category][lumiyear].Clone()
                            h_tmp_global.Scale(official_lumis[lumiyear])
                            h_tmp_reco = h_sf_reco[category][lumiyear].Clone()
                            h_tmp_reco.Scale(official_lumis[lumiyear])
                            h_tmp_tag = h_sf_tag[category][lumiyear].Clone()
                            h_tmp_tag.Scale(official_lumis[lumiyear])

                            if not h_sf_global[category][runyear]:
                                print category, "adding", lumiyear, "to", runyear
                                h_sf_global[category][runyear] = h_tmp_global.Clone()
                                h_sf_reco[category][runyear] = h_tmp_reco.Clone()
                                h_sf_tag[category][runyear] = h_tmp_tag.Clone()
                            else:
                                print category, "adding", lumiyear, "to", runyear
                                h_sf_global[category][runyear].Add(h_tmp_global)
                                h_sf_reco[category][runyear].Add(h_tmp_reco)
                                h_sf_tag[category][runyear].Add(h_tmp_tag)

                    print runyear, sum_lumi

                    fitresults["fit_sf"][runyear + category] /= sum_lumi
                    fitresults["fit_uncert"][runyear + category] /= sum_lumi
                    fitresults["fit_sfreco"][runyear + category] /= sum_lumi
                    fitresults["fit_uncertreco"][runyear + category] /= sum_lumi
                    fitresults["fit_sftag"][runyear + category] /= sum_lumi
                    fitresults["fit_uncerttag"][runyear + category] /= sum_lumi
                    
                    h_sf_global[category][runyear].Scale(1.0/sum_lumi)
                    h_sf_reco[category][runyear].Scale(1.0/sum_lumi)
                    h_sf_tag[category][runyear].Scale(1.0/sum_lumi)

                    print "*** SF ", runyear, category, fitresults["fit_sf"][runyear + category], "+-", fitresults["fit_uncert"][runyear + category]

        # efficiencies:

        print "plot SF..."
        
        output_rootfile = TFile("%s/allperiods_sf_combined.root" % (plotfolder), "recreate")

        for category in [
                    "short",
                    "long",
                    "",
                    ]:

            canvas = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1=0.47, y1=0.65, x2=0.85, y2=0.85)
            legend.SetHeader("%s tracks %s" % (category, cuts[cut_label]["legendheader"]))
            legend.SetTextSize(0.035)
                
            h_sf_short = {}
            h_sf_long = {}
                
            for label in ["fit_sf", "fit_sfreco", "fit_sftag"]:
                
                if options.lumiweighted:
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

                    if options.lumiweighted:
                        if period.split("_")[0] == "Run2016" or period.split("_")[0] == "Run2017" or period.split("_")[0] == "Run2018":
                            pass
                        else:
                            continue


                    print category, period
                                        
                    if "short" in period:
                        h_sf_short[label].SetBinContent(i_short + 1, sf)
                        h_sf_short[label].SetBinError(i_short + 1, uncert)
                        i_short +=1
                        binlabels_short.append(period.replace("Run", "").replace("_short", "").replace("_long", ""))
                    elif "long" in period:
                        h_sf_long[label].SetBinContent(i_long + 1, sf)
                        h_sf_long[label].SetBinError(i_long + 1, uncert)
                        i_long += 1
                        binlabels_long.append(period.replace("Run", "").replace("_short", "").replace("_long", ""))
                        
                if category == "short":      
                    if label == "fit_sf":
                        h_sf_short[label].Draw("hist e")
                    else:
                        h_sf_short[label].Draw("hist e same")

                    if "corr" in suffix:
                        outhist = h_sf_short[label].Clone()
                        outhist.SetDirectory(0)
                        outhist.SetName(label + "_" + category)
                        outhist.Write()
                    
                    if "reco" in label:
                        h_sf_short[label].SetTitle(";;fitted track reconstruction scale factor")
                    elif "tag" in label:
                        h_sf_short[label].SetTitle(";;fitted track tagging scale factor")
                    else:
                        h_sf_short[label].SetTitle(";;fitted scale factor")
                    h_sf_short[label].GetYaxis().SetRangeUser(0.4, 1.6)
                else:
                    if label == "fit_sf":
                        h_sf_long[label].Draw("hist e")
                    else:
                        h_sf_long[label].Draw("hist e same")
                    
                    if "corr" not in suffix and category == "long":
                        outhist = h_sf_long[label].Clone()
                        outhist.SetDirectory(0)
                        outhist.SetName(label + "_" + category)
                        outhist.Write()
                    
                    if "reco" in label:
                        h_sf_long[label].SetTitle(";;fitted track reconstruction scale factor")
                    elif "tag" in label:
                        h_sf_long[label].SetTitle(";;fitted track tagging scale factor")
                    else:
                        h_sf_long[label].SetTitle(";;fitted scale factor")
                    h_sf_long[label].GetYaxis().SetRangeUser(0.4, 1.6)
                    
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
                               
                for i, i_binlabel in enumerate(binlabels_short):
                    h_sf_short[label].GetXaxis().SetBinLabel(i + 1, i_binlabel)    
                for i, i_binlabel in enumerate(binlabels_long):
                    h_sf_long[label].GetXaxis().SetBinLabel(i + 1, i_binlabel)    
                
                if options.lumiweighted:
                    h_sf_short[label].GetXaxis().SetLabelSize(0.09)
                    h_sf_short[label].GetXaxis().SetTitleSize(0.09)
                    h_sf_long[label].GetXaxis().SetLabelSize(0.09)
                    h_sf_long[label].GetXaxis().SetTitleSize(0.09)
                else:
                    h_sf_short[label].GetXaxis().SetTitleSize(0.045)
                    h_sf_short[label].GetXaxis().SetLabelSize(0.045)
                    h_sf_long[label].GetXaxis().SetTitleSize(0.045)
                    h_sf_long[label].GetXaxis().SetLabelSize(0.045)

                
            legend.Draw()
            
            shared_utils.stamp(WorkInProgress = True)
            
            pdfname = "%s/allperiods_sf_combined_%s_%s.pdf" % (plotfolder, category, cut_label)
            
            if options.get_from_tree:
                pdfname = pdfname.replace(".pdf", "_tree.pdf")                       
            if options.mc_reweighted:
                pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
            if options.lumiweighted:
                pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")
            if options.weightkinematic:
                pdfname = pdfname.replace(".pdf", "_weightkinematic.pdf")
            if options.weighttrackprop:
                pdfname = pdfname.replace(".pdf", "_weighttrackprop.pdf")
            
            canvas.SaveAs(pdfname)
            #canvas.SaveAs(pdfname.replace(".pdf", ".root"))
            
            #fout = TFile(pdfname.replace(".pdf", ".root"), "recreate")
            #canvas.Write()
            #h_sf_short.SetName("h_scalefactor_short")
            #h_sf_short.Write()
            #h_sf_long.SetName("h_scalefactor_long")
            #h_sf_long.Write()
            #fout.Close()
            
        
        output_rootfile.Close()
        
        if options.lumiweighted:
            #this_periods = finaleff_global_num[category].keys()
            this_periods = [
                             "Run2016",
                             "Run2017",
                             "Run2018",
                           ]
        else:
            this_periods = periods
        
        # plot underlying efficiencies:

        if not options.lumiweighted and not options.get_from_tree:
                for i_finaleff, finaleff in enumerate([finaleff_global, finaleff_reco, finaleff_tag]):
                    for year in ["2016", "2017", "2018"]:
                        for category in categories:
                            
                            canvas = shared_utils.mkcanvas()
                            legend = shared_utils.mklegend(x1=0.6, y1=0.6, x2=0.85, y2=0.85)
                            legend.SetHeader("%s tracks (%s)" % (category.replace("_", ""), year))
                            legend.SetTextSize(0.035)
                            
                            colors = [kBlack, 97, 94, 91, 86, 81, 70, 65, 61, 51]
                            
                            for i_period, period in enumerate(this_periods):
                                                        
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
                                        drawoption = "p e"
                                    else:
                                        drawoption = "hist e same"
                                    if period != mcperiod:
                                        finaleff[category][period].SetMarkerStyle(20)
                                        finaleff[category][period].SetMarkerColor(color)
                                                           
                                    finaleff[category][period].Draw(drawoption)
                                    finaleff[category][period].SetLineColor(color)
                                    finaleff[category][period].SetLineStyle(1)
                                    if i_finaleff == 0:
                                        finaleff[category][period].SetTitle(";number of remaining tracker layers;efficiency")
                                    elif i_finaleff == 1:
                                        finaleff[category][period].SetTitle(";number of remaining tracker layers;reconstruction efficiency")
                                    elif i_finaleff == 2:
                                        finaleff[category][period].SetTitle(";number of remaining tracker layers;tagging efficiency")
                                    finaleff[category][period].GetXaxis().SetRangeUser(0, 20)
                                    finaleff[category][period].GetYaxis().SetRangeUser(0.0, 1.1)
                                    legend.AddEntry(finaleff[category][period], period)
                                
                            legend.Draw()
                            shared_utils.stamp(WorkInProgress = True)
                    
                            if i_finaleff == 0:        
                                pdfname = "%s/underlying%s%s.pdf" % (plotfolder, category, year)
                            elif i_finaleff == 1:        
                                pdfname = "%s/underlying_reco%s%s.pdf" % (plotfolder, category, year)
                            elif i_finaleff == 2:        
                                pdfname = "%s/underlying_tag%s%s.pdf" % (plotfolder, category, year)

                            if options.get_from_tree:
                                pdfname = pdfname.replace(".pdf", "_tree.pdf")                       
                            if options.mc_reweighted:
                                pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
                            if options.lumiweighted:
                                pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")
                            
                            canvas.SaveAs(pdfname)
                    
                    
        # plot underlying SF:

        #if not options.lumiweighted and not options.get_from_tree:
        if not options.get_from_tree:
                for i_finaleff, finaleff in enumerate([finaleff_global, finaleff_reco, finaleff_tag]):

                    for category in categories:

                        if options.lumiweighted:
                            canvas = shared_utils.mkcanvas()
                            legend = shared_utils.mklegend(x1=0.7, y1=0.6, x2=0.85, y2=0.85)
                            legend.SetTextSize(0.035)
                            if category != "":
                                legend.SetHeader("%s tracks only" % category.replace("_", ""))
                            colors = [61, 97, 210]


                        for year in ["2016", "2017", "2018"]:

                            if not options.lumiweighted:
                                canvas = shared_utils.mkcanvas()
                                legend = shared_utils.mklegend(x1=0.6, y1=0.6, x2=0.85, y2=0.85)
                                legend.SetHeader("%s tracks (%s)" % (category.replace("_", ""), year))
                                legend.SetTextSize(0.035)                           
                                colors = [kBlack, 97, 94, 91, 86, 81, 70, 65, 61, 51]
                            
                            for i_period, period in enumerate(this_periods):
                                                        
                                if "rw" in period: continue
                                
                                if year == "2016":
                                    mcperiod = "Summer16"
                                elif year == "2017":
                                    mcperiod = "Fall17"
                                elif year == "2018":
                                    mcperiod = "Autumn18"
                                
                                if period == mcperiod or year in period:
                                
                                    color = colors.pop(0)
                                    if "Run" in period and "rw" not in period:
                                        if i_finaleff == 0: 
                                            h_sf_global[category][period].Draw("hist e same")
                                            h_sf_global[category][period].GetXaxis().SetRangeUser(0, 20)
                                            h_sf_global[category][period].GetYaxis().SetRangeUser(0.4, 1.6)
                                            h_sf_global[category][period].SetTitle(";number of remaining tracker layers;scale factor")
                                            h_sf_global[category][period].SetLineColor(color)
                                            h_sf_global[category][period].SetLineWidth(2)
                                            legend.AddEntry(h_sf_global[category][period], period)
                                            if period in g1_global[category] and not options.lumiweighted:
                                                g1_global[category][period].Draw("same")
                                                g1_global[category][period].SetLineColor(color)
                                                g1_global[category][period].SetLineWidth(2)
                                                legend.AddEntry(g1_global[category][period], period)
                                        elif i_finaleff == 1: 
                                            h_sf_reco[category][period].Draw("hist e same")
                                            h_sf_reco[category][period].GetXaxis().SetRangeUser(0, 20)
                                            h_sf_reco[category][period].GetYaxis().SetRangeUser(0.4, 1.6)
                                            h_sf_reco[category][period].SetTitle(";number of remaining tracker layers;reconstruction scale factor")
                                            h_sf_reco[category][period].SetLineColor(color)
                                            h_sf_reco[category][period].SetLineWidth(2)
                                            legend.AddEntry(h_sf_reco[category][period], period)
                                            if "period" in g1_reco[category] and not options.lumiweighted:
                                                g1_reco[category][period].Draw("hist same")
                                                g1_reco[category][period].SetLineColor(color)
                                                g1_reco[category][period].SetLineWidth(2)
                                                legend.AddEntry(g1_reco[category][period], period)
                                        elif i_finaleff == 2: 
                                            h_sf_tag[category][period].Draw("hist e same")
                                            h_sf_tag[category][period].GetXaxis().SetRangeUser(0, 20)
                                            h_sf_tag[category][period].GetYaxis().SetRangeUser(0.4, 1.6)
                                            h_sf_tag[category][period].SetTitle(";number of remaining tracker layers;tagging scale factor")
                                            h_sf_tag[category][period].SetLineColor(color)
                                            h_sf_tag[category][period].SetLineWidth(2)
                                            legend.AddEntry(h_sf_tag[category][period], period)
                                            if "period" in g1_tag[category] and not options.lumiweighted:
                                                g1_tag[category][period].Draw("same")
                                                g1_tag[category][period].SetLineColor(color)
                                                g1_tag[category][period].SetLineWidth(2)
                                                legend.AddEntry(g1_tag[category][period], period)
                                                                                
                            legend.Draw()
                            shared_utils.stamp(WorkInProgress = True)
                    
                            if i_finaleff == 0:        
                                pdfname = "%s/underlying_SF%s%s.pdf" % (plotfolder, category, year)
                            elif i_finaleff == 1:        
                                pdfname = "%s/underlying_SF_reco%s%s.pdf" % (plotfolder, category, year)
                            elif i_finaleff == 2:        
                                pdfname = "%s/underlying_SF_tag%s%s.pdf" % (plotfolder, category, year)

                            if options.get_from_tree:
                                pdfname = pdfname.replace(".pdf", "_tree.pdf")                       
                            if options.mc_reweighted:
                                pdfname = pdfname.replace(".pdf", "_mcreweighted.pdf")
                            if options.lumiweighted:
                                pdfname = pdfname.replace(".pdf", "_lumiweighted.pdf")

                            if not options.lumiweighted:                            
                                canvas.SaveAs(pdfname)

                        if options.lumiweighted:  
                            if i_finaleff == 0:        
                                pdfname = "%s/pooled_SF%s.pdf" % (plotfolder, category)
                            elif i_finaleff == 1:        
                                pdfname = "%s/pooled_SF_reco%s.pdf" % (plotfolder, category)
                            elif i_finaleff == 2:        
                                pdfname = "%s/pooled_SF_tag%s.pdf" % (plotfolder, category)                          
                            canvas.SaveAs(pdfname)

            
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "run13rw1")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")
    parser.add_option("--reweighted", dest = "mc_reweighted", action = "store_true")
    parser.add_option("--lumiweighted", dest = "lumiweighted", action = "store_true")
    parser.add_option("--tree", dest = "get_from_tree", action = "store_true")
    parser.add_option("--weightkinematic", dest = "weightkinematic", action = "store_true")
    parser.add_option("--weighttrackprop", dest = "weighttrackprop", action = "store_true")

    (options, args) = parser.parse_args()
    main(options)
        
