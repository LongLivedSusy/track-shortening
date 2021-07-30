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


def get_reweighting_factor(histofolder, plotfolder, suffix):
    
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
    
    histolabels = [
                "track_nValidPixelHits",
              ]
    
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
    
    means = {}        

    for period in periods:
        histo = hists[period]["track_nValidPixelHits"]
        g1 = TF1( 'g1', 'gaus',  2,  7 )
        fit = histo.Fit(g1, "", "same", 2, 7)
        mean = g1.GetParameter(1)
        sigma = g1.GetParError(2)
    
        means[period] = mean
        
    print "means", means
    
    reweighting_factors = {}
    for period in means:
        if "Run2016" in period:
            factor = means[period] / means["Run2016H"]
            reweighting_factors[period] = factor
        elif "Run2017" in period:
            factor = means[period] / means["Run2017B"]
            reweighting_factors[period] = factor
        elif "Run2018" in period:
            factor = means[period] / means["Run2018D"]
            reweighting_factors[period] = factor

    print "reweighting_factors", reweighting_factors


if __name__ == "__main__":

    print "Loading"

    parser = OptionParser()
    parser.add_option("--suffix", dest = "suffix", default = "")
    parser.add_option("--histofolder", dest = "histofolder", default = "histograms")

    (options, args) = parser.parse_args()
    
    plotfolder = "plots%s" % options.suffix
    get_reweighting_factor(options.histofolder, plotfolder, options.suffix)
