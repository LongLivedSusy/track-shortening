#!/bin/env python
import GridEngineTools
import os

# run hit removal tool and do second reconstruction
# comments @ Viktor Kutzner

period              = "Summer16"
step_clustersurgeon = True
step_reco           = False

# set up CMSSW:
if not os.path.exists("CMSSW_8_0_22"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; cmsrel CMSSW_8_0_22; cd CMSSW_8_0_22/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10; cd -")
if not os.path.exists("CMSSW_8_0_31"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; cmsrel CMSSW_8_0_31; cd CMSSW_8_0_31/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10; cd -")

# modify hit collections:
if step_clustersurgeon:
    commands = []
    commands["Run2016"] = [
        "cd CMSSW_8_0_22/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/120F91C9-F69F-E611-8164-02163E0125BE.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Run2016_allSteps_1.root; cd -",
        "cd CMSSW_8_0_22/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/5AA45327-B89F-E611-8CD1-02163E01392B.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Run2016_allSteps_2.root; cd -",
        ]
    commands["Summer16"] = [   
        "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO/24BAB5FD-E38E-E511-9CDD-F01FAFD9027E-local.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_1.root; cd -",
    ]

    GridEngineTools.runParallel(commands[period], "grid", use_sl6=True, confirm=False)
    os.system("hadd -f rCluster_%s_allSteps.root rCluster_%s_allSteps_*.root && rCluster_%s_allSteps_*.root" % (period, period, period))


# do rereco with modified hit collections:
if step_reco:
    commands = [
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=1 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=2 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=3 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=4 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=5 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=6 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=7 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=8 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=9 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=10 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=11 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=12 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=13 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=14 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=15 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=16 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=17 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=18 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=19 MuonSeeds=1" % (period, period, period),
        "cmsRun python/reRECO_%s.py inputFiles=file://rCluster_%s_allSteps.root outputFileName=reRECO_%s step=20 MuonSeeds=1" % (period, period, period),
    ]
    
    GridEngineTools.runParallel(commands, "grid", use_sl6=True, confirm=False)
