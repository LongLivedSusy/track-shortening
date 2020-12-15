#!/bin/env python
import GridEngineTools
import os

# modify hit collections:

period = "Summer16"


commands = []

commands["Run2016"] = [
    "cd CMSSW_8_0_22/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/120F91C9-F69F-E611-8164-02163E0125BE.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Run2016_allSteps_1.root; cd -",
    "cd CMSSW_8_0_22/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/5AA45327-B89F-E611-8CD1-02163E01392B.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Run2016_allSteps_2.root; cd -",
    ]
commands["Summer16"] = [   
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/020E9AFE-C78E-E511-8A53-F01FAFD1C83F.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_1.root; cd -",
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/0C9A1EE9-C78E-E511-AADF-F01FAFE5CEFA.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_2.root; cd -",
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/1E8C10A5-E88E-E511-B54A-F01FAFD9D090.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_3.root; cd -",
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/24BAB5FD-E38E-E511-9CDD-F01FAFD9027E.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_4.root; cd -",
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/447850F8-E38E-E511-AF09-F01FAFD9027E.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_5.root; cd -",
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/B2DB96FE-E38E-E511-9739-F01FAFE0F396.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_6.root; cd -",
    "cd CMSSW_8_0_31/src/shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/mcgen/Summer16_RECO_small/CC8A54FA-E38E-E511-8641-F01FAFD9C64C.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_7.root; cd -",
]

GridEngineTools.runParallel(commands[period], "grid", use_sl6=True, confirm=False)
os.system("hadd -f rCluster_%s_allSteps.root rCluster_%s_allSteps_*.root && rCluster_%s_allSteps_*.root" % (period, period, period))

quit()

# do rereco with modified hit collections:

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

GridEngineTools.runParallel(commands, "grid", confirm=False)
