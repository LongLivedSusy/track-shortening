#!/bin/env python
import sys
import os
import glob

files = [
    "/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/120F91C9-F69F-E611-8164-02163E0125BE.root",
    "/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/5AA45327-B89F-E611-8CD1-02163E01392B.root",
    "/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/301/531/00000/2C1BE3BA-6C88-E711-B8B8-02163E01A1FA.root",
    "/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/301/531/00000/D6DD8A94-6A88-E711-ACBA-02163E01292F.root",
    "/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/301/530/00000/D67FF528-6A88-E711-A589-02163E0137FF.root",
    "/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/301/531/00000/1ECD14F3-6888-E711-B1EF-02163E0137FF.root",
    "/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/068/00000/369422FC-6B9F-E611-B26C-02163E0127F5.root",
    "/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/036/00000/BC7FF20E-639F-E611-9A06-FA163E6C68D0.root",
    "/store/data/Run2018C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/319/950/00000/04A930A3-F28D-E811-A2B8-FA163E11135C.root",
    "/store/data/Run2018C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/319/950/00000/4C23DD9F-DC8D-E811-BFA1-02163E01A057.root",
    "/store/data/Run2018C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/319/950/00000/4C179610-CE8D-E811-8CA8-FA163E42C016.root",
    "/store/data/Run2018C/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/319/950/00000/02B186B7-C38D-E811-B2CA-FA163E463595.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/58034BE9-8757-E911-9401-0025905B85EC.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/864EDE79-7757-E911-AC5C-0CC47A74524E.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/887775D2-FD56-E911-A1C5-AC1F6BAC7C78.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/EC8BA36B-E656-E911-B3BD-0CC47A7C354C.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/5419FCAC-ED56-E911-B7D4-0CC47A4D7654.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/1463FF0A-BF56-E911-8FB0-0025905AA9CC.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/2818D153-C256-E911-86C8-0CC47A4C8E96.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/98708252-C256-E911-A3B1-0CC47A7C35C8.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/527E28AC-BE56-E911-80F7-0CC47A7C34C4.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/148FACC1-BB56-E911-9A2B-AC1F6BAC7D10.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/0A1EA198-BB56-E911-974A-0CC47A7C35F4.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/508ED292-BB56-E911-A034-AC1F6BAC7D16.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/34D755A6-BB56-E911-9EED-AC1F6BAC7C78.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/12679F8D-B856-E911-9219-0CC47A78A3EE.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/F0D832A7-BB56-E911-9FBB-0CC47A7C35A4.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/26228A7B-BB56-E911-8DBA-0CC47A74524E.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/B2085C9D-9156-E911-B797-0025905B8582.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/CCF5D19B-8956-E911-8582-0025905B85D6.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/C69F199C-8956-E911-9E50-0025905A606A.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/DCF80480-9156-E911-B2E9-AC1F6BAC7D1A.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/607F2C9C-8956-E911-98A3-0025905A60D6.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/E46FA178-9156-E911-8C9E-0CC47A4C8EC8.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/A0669075-8956-E911-B019-0CC47A4C8EE8.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/1ECDC35D-8956-E911-9C17-0CC47A4C8E14.root",
    "/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/70AF8783-8956-E911-BC3C-AC1F6BAC7D18.root",
]

for ifile in files:
    
    print ifile
    folder = "/".join(ifile.split("/")[:-1])
    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/%s" % folder)

    if os.path.exists("/nfs/dust/cms/user/kutznerv/%s/%s" % (folder, ifile.split("/")[-1])):
        print "already there"
        continue
    
    os.system("cp /pnfs/desy.de/cms/tier2/%s ~/dust/%s/" % (ifile, folder))