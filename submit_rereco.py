#!/bin/env python
import GridEngineTools
import os

# run hit removal tool and do second reconstruction
# comments @ Viktor Kutzner

period              = "Summer16"
#period              = "Run2016"
step_clustersurgeon = 0
step_reco           = 0
step_isoproducer    = 1
runmode             = "grid"

# set up CMSSW:
if not os.path.exists("CMSSW_8_0_22/src/shorttrack"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; cmsrel CMSSW_8_0_22; cd CMSSW_8_0_22/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")
if not os.path.exists("CMSSW_8_0_21/src/shorttrack"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; cmsrel CMSSW_8_0_21; cd CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")

# modify hit collections:
if step_clustersurgeon:
    commands = {}
    commands["Run2016"] = [
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_22/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/120F91C9-F69F-E611-8164-02163E0125BE.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Run2016_allSteps_1.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_22/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/5AA45327-B89F-E611-8CD1-02163E01392B.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Run2016_allSteps_2.root",
        ]
    commands["Summer16"] = [   
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/020E9AFE-C78E-E511-8A53-F01FAFD1C83F.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_1.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/0C9A1EE9-C78E-E511-AADF-F01FAFE5CEFA.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_2.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/1E8C10A5-E88E-E511-B54A-F01FAFD9D090.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_3.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/24BAB5FD-E38E-E511-9CDD-F01FAFD9027E.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_4.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/447850F8-E38E-E511-AF09-F01FAFD9027E.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_5.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/B2DB96FE-E38E-E511-9739-F01FAFE0F396.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_6.root",
        "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file:///nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/CC8A54FA-E38E-E511-8641-F01FAFD9C64C.root outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/rCluster_Summer16_allSteps_7.root",
    ]

    GridEngineTools.runParallel(commands[period], runmode, use_sl6=True, confirm=False)
    os.system("hadd -f rCluster_%s_allSteps.root rCluster_%s_allSteps_*.root && rm rCluster_%s_allSteps_*.root" % (period, period, period))


# do rereco with modified hit collections:
if step_reco:
    
    if period == "Run2016":
        cmssw = "CMSSW_8_0_22"
    elif period == "Summer16":
        cmssw = "CMSSW_8_0_21"    
        
    commands = [
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=1 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=2 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=3 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=4 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=5 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=6 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=7 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=8 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=9 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=10 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=11 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=12 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=13 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=14 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=15 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=16 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=17 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=18 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=19 MuonSeeds=1" % (cmssw, period, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../rCluster_%s_allSteps.root outputFileName=../../reRECO_%s step=20 MuonSeeds=1" % (cmssw, period, period, period),
    ]
    
    GridEngineTools.runParallel(commands, runmode, use_sl6=True, confirm=False)


# do rereco with modified hit collections:
if step_isoproducer:
    
    if period == "Run2016":
        cmssw = "CMSSW_8_0_22"
    elif period == "Summer16":
        cmssw = "CMSSW_8_0_21"    
        
    commands = [
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_1.root outputFile=../../reRECO_%s_trackInfo_1.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_2.root outputFile=../../reRECO_%s_trackInfo_2.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_3.root outputFile=../../reRECO_%s_trackInfo_3.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_4.root outputFile=../../reRECO_%s_trackInfo_4.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_5.root outputFile=../../reRECO_%s_trackInfo_5.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_6.root outputFile=../../reRECO_%s_trackInfo_6.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_7.root outputFile=../../reRECO_%s_trackInfo_7.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_8.root outputFile=../../reRECO_%s_trackInfo_8.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_9.root outputFile=../../reRECO_%s_trackInfo_9.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_10.root outputFile=../../reRECO_%s_trackInfo_10.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_11.root outputFile=../../reRECO_%s_trackInfo_11.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_12.root outputFile=../../reRECO_%s_trackInfo_12.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_13.root outputFile=../../reRECO_%s_trackInfo_13.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_14.root outputFile=../../reRECO_%s_trackInfo_14.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_15.root outputFile=../../reRECO_%s_trackInfo_15.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_16.root outputFile=../../reRECO_%s_trackInfo_16.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_17.root outputFile=../../reRECO_%s_trackInfo_17.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_18.root outputFile=../../reRECO_%s_trackInfo_18.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_19.root outputFile=../../reRECO_%s_trackInfo_19.root" % (cmssw, period, period),
        "cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../reRECO_%s_20.root outputFile=../../reRECO_%s_trackInfo_20.root" % (cmssw, period, period),
    ]
    
    GridEngineTools.runParallel(commands, runmode, use_sl6=True, confirm=False)
