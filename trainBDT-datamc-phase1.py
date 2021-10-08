#!/usr/bin/env python
import glob
from ROOT import *
from optparse import OptionParser
import os

def train(configuration, n_ntuple_files_sg = -1, n_ntuple_files_bg = -1):
       
    TMVA.Tools.Instance()
                
    fout = TFile("output_phase1_%s.root" % configuration, "recreate")
    
    factory = TMVA.Factory("TMVAClassification", fout,
                                ":".join([    "!V",
                                              "!Silent",
                                              "Color",
                                              "DrawProgressBar",
                                              "Transformations=I;D;P;G,D",
                                              "AnalysisType=Classification"]
                                         ))
                                         
    dataloader = TMVA.DataLoader("dataset")

    if configuration == "A":
        dataloader.AddVariable("track_pt", "F")
        dataloader.AddVariable("track_ptErrOverPt2", "F")
        dataloader.AddVariable("track_eta", "F")
        dataloader.AddVariable("track_phi", "F")
    elif configuration == "B":
        dataloader.AddVariable("track_dxyVtx", "F")
        dataloader.AddVariable("track_dzVtx", "F")
        dataloader.AddVariable("track_trkRelIso", "F")
        dataloader.AddVariable("track_nValidPixelHits", "I")
        dataloader.AddVariable("track_ptErrOverPt2", "F")
        dataloader.AddVariable("track_chi2perNdof", "F")

    periods = {
            #"Run2016B": 5.8,
            #"Run2016C": 2.6,
            #"Run2016D": 4.2,
            #"Run2016E": 4.0,
            #"Run2016F": 3.1,
            #"Run2016G": 7.5,
            #"Run2016H": 8.6,
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

    total_lumi_phase1 = 0
    total_lumi_2017 = 0
    total_lumi_2018 = 0
    for period in periods:
        total_lumi_phase1 += periods[period]
        if "2017" in period:
            total_lumi_2017 += periods[period]
        if "2018" in period:
            total_lumi_2018 += periods[period]
    
    tree_data = {}
    for period in periods:
        tree_data[period] = TChain("Events")
        tree_data[period].Add("histograms/histogramsrun16AllShorts_%s.root" % period)
        weight = periods[period] / total_lumi_phase1
        print period, weight
        dataloader.AddSignalTree(tree_data[period], weight)

    tree_fall17 = TChain("Events")
    tree_fall17.Add("histograms/histogramsrun16AllShorts_Fall17.root")
    weight = total_lumi_2017 / (total_lumi_2017 + total_lumi_2018)
    print "Fall17", weight
    dataloader.AddBackgroundTree(tree_fall17, weight)

    tree_aut18 = TChain("Events")
    tree_aut18.Add("histograms/histogramsrun16AllShorts_Autumn18.root")
    weight = total_lumi_2018 / (total_lumi_2017 + total_lumi_2018)
    print "Aut18", weight
    dataloader.AddBackgroundTree(tree_aut18, weight)
       
    cuts = "track_is_pixel_track==1 && track_preselected==1 && muon_dxy<0.1 && muon_dz<0.1"

    sigCut = TCut(cuts)
    bgCut = TCut(cuts)
        
    dataloader.PrepareTrainingAndTestTree(sigCut, 
                                       bgCut, 
                                       ":".join(["nTrain_Signal=0",
                                                 "nTrain_Background=0",
                                                 "SplitMode=Random",
                                                 "NormMode=NumEvents",
                                                 "!V"
                                                 ]))

    method = factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT1_%s" % configuration,
                                ":".join([ "!H",
                                           "!V",
                                           "NTrees=200",
                                           "MaxDepth=4",
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5",
                                           "SeparationType=GiniIndex",
                                           "PruneMethod=NoPruning",
                                           ]))

    method = factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT2_%s" % configuration,
                                ":".join([ "!H",
                                           "!V",
                                           "NTrees=400",
                                           "MaxDepth=4",
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5",
                                           "SeparationType=GiniIndex",
                                           "PruneMethod=NoPruning",
                                           ]))

    method = factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT3_%s" % configuration,
                                ":".join([ "!H",
                                           "!V",
                                           "NTrees=600",
                                           "MaxDepth=6",
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5",
                                           "SeparationType=GiniIndex",
                                           "PruneMethod=NoPruning",
                                           ]))

    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP1_%s" % configuration, "!V:NCycles=200:HiddenLayers=N+1,N:TestRate=5")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP2_%s" % configuration, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=200:HiddenLayers=N+5:TestRate=5:!UseRegulator")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP3_%s" % configuration, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+1:TestRate=5:!UseRegulator")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP4_%s" % configuration, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP5_%s" % configuration, "H:!V:NeuronType=sigmoid:VarTransform=N:NCycles=200:HiddenLayers=N+5:TestRate=5:!UseRegulator")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP6_%s" % configuration, "H:!V:NeuronType=sigmoid:VarTransform=N:NCycles=200:HiddenLayers=N+2:TestRate=5:!UseRegulator")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP7_%s" % configuration, "H:!V:NeuronType=sigmoid:VarTransform=N:NCycles=200:HiddenLayers=N+5:TestRate=5:!UseRegulator:EstimatorType=linear")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP8_%s" % configuration, "H:!V:NeuronType=sigmoid:VarTransform=N:NCycles=200:HiddenLayers=N+5:TestRate=5:!UseRegulator:EstimatorType=sigmoid")
    method = factory.BookMethod(dataloader, TMVA.Types.kMLP, "MLP9_%s" % configuration, "H:!V:NeuronType=sigmoid:VarTransform=N:NCycles=200:HiddenLayers=N+5:TestRate=5:!UseRegulator:EstimatorType=tanh")

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()

    if len(args) == 0:
        os.system("./trainBDT-datamc-phase1.py A &")
        os.system("./trainBDT-datamc-phase1.py B &")
    else:
        train(args[0])

