#!/bin/env python
import GridEngineTools
import os
import glob

# run hit removal tool and do second reconstruction
# comments @ Viktor Kutzner

period              = "Summer16"
#period              = "Run2016"
step_clustersurgeon = 1
step_reco           = 1
step_isoproducer    = 1
runmode             = "grid"

# set up CMSSW:
if not os.path.exists("CMSSW_8_0_22/src/shorttrack"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_22; cd CMSSW_8_0_22/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")
if not os.path.exists("CMSSW_8_0_21/src/shorttrack"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_21; cd CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")
if not os.path.exists("CMSSW_8_0_31/src/shorttrack"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_31; cd CMSSW_8_0_31/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")

if period == "Run2016":
    cmssw = "CMSSW_8_0_22"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco-v3/000/284/037/00000/*root"
elif period == "Summer16":
    cmssw = "CMSSW_8_0_21"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*root"
    #cmssw = "CMSSW_8_0_31"
    #inputpath = "/nfs/dust/cms/user/kutznerv/store/mc/RunIISummer16DR80/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RECO/PUPoissonAve23_80X_mcRun2_asymptotic_2016_TrancheIV_v8-v1/120000/*root"

# modify hit collections:
if step_clustersurgeon:
    commands = []
    for i, i_file in enumerate(glob.glob(inputpath)):
        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file://%s outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER/rCluster_%s_allSteps_%s.root" % (cmssw, i_file, period, period, i+1))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER" % period)
    status = GridEngineTools.runParallel(commands, runmode, confirm=True, use_sl6=True)
    if status != 0: quit(str(status))


# do rereco with modified hit collections:
if step_reco:
    commands = []
    for i_file in glob.glob("%s_HITREMOVER/*root" % period):
        o_file = i_file.replace("HITREMOVER", "RERECO").replace(".root", "")
        for step in range(1, 21):
            commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../%s outputFileName=../../%s step=%s MuonSeeds=1" % (cmssw, period, i_file, o_file, step))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_RERECO" % period)
    status = GridEngineTools.runParallel(commands, runmode, confirm=False, use_sl6=True)
    if status != 0: quit(str(status))


# do rereco with modified hit collections:
if step_isoproducer:
    
    commands = []
    for i_file in glob.glob("%s_RERECO/*root" % period):
        o_file = i_file.replace("RERECO", "ISOTRACKS")
        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../%s outputFile=../../%s" % (cmssw, i_file, o_file))
    
    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_ISOTRACKS" % period)
    status = GridEngineTools.runParallel(commands, runmode, confirm=False, use_sl6=True)
    if status != 0: quit(str(status))
