#!/bin/env python
import GridEngineTools
import os
import glob

# run hit removal tool and do second reconstruction
# comments @ Viktor Kutzner

#period              = "Summer16"
period              = "Run2016E"
step_clustersurgeon = 1
step_reco           = 1
step_isoproducer    = 1
runmode             = "grid"

def runSL6(command):
    singularity_wrapper = "singularity exec --contain --bind /afs:/afs --bind /nfs:/nfs --bind /pnfs:/pnfs --bind /cvmfs:/cvmfs --bind /var/lib/condor:/var/lib/condor --bind /tmp:/tmp --pwd . ~/dust/slc6_latest.sif sh -c 'source /cvmfs/cms.cern.ch/cmsset_default.sh; $CMD'"
    os.system(singularity_wrapper.replace("$CMD", command))

# set up CMSSW:
if not os.path.exists("CMSSW_8_0_22/src/shorttrack"):
    runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_22; cd CMSSW_8_0_22/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")
if not os.path.exists("CMSSW_8_0_21/src/shorttrack"):
    runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_21; cd CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")
if not os.path.exists("CMSSW_8_0_29/src/shorttrack"):
    runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_29; cd CMSSW_8_0_29/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")
if not os.path.exists("CMSSW_8_0_31/src/shorttrack"):
    runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW CMSSW_8_0_31; cd CMSSW_8_0_31/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10")

if period == "Run2016":
    # this is the prompt reco
    cmssw = "CMSSW_8_0_22"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco*/*/*/*/*/*.root"
elif period == "Run2016B":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016B/SingleMuon/RAW-RECO/ZMu-07Aug17_ver2-v1/*/*root"
elif period == "Run2016E":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016E/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*root"
elif period == "Run2016H":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*root"    
elif period == "Summer16":
    cmssw = "CMSSW_8_0_21"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*root"

# modify hit collections:
if step_clustersurgeon:
    commands = []
    for i, i_file in enumerate(glob.glob(inputpath)):
        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file://%s outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER/rCluster_%s_allSteps_%s.root" % (cmssw, i_file, period, period, i+1))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER" % period)
    os.system("rm condor.%s/*" % period)
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=False, use_sl6=True)
    #if status != 0: quit(str(status))


# do rereco with modified hit collections:
if step_reco:
    commands = []
    for i_file in glob.glob("%s_HITREMOVER/*root" % period):
        o_file = i_file.replace("HITREMOVER", "RERECO").replace(".root", "")
        for step in range(1, 21):
            if "2016" in period:
                year = "2016"
            elif "2017" in period:
                year = "2017"
            elif "2018" in period:
                year = "2018"
            else:
                year = period
            commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../%s outputFileName=../../%s step=%s MuonSeeds=1" % (cmssw, year, i_file, o_file, step))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_RERECO" % period)
    os.system("rm condor.%s/*" % period)
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=False, use_sl6=True)
    #if status != 0: quit(str(status))


# do rereco with modified hit collections:
if step_isoproducer:
    
    commands = []
    for i_file in glob.glob("%s_RERECO/*root" % period):
        o_file = i_file.replace("RERECO", "ISOTRACKS").replace(".root", "")
        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cmsRun shorttrack/DisappearingTrack/python/isotrackproducer_cfi.py inputFiles=file://../../%s outputFile=../../%s" % (cmssw, i_file, o_file))
    
    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_ISOTRACKS" % period)
    os.system("rm condor.%s/*" % period)
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=False, use_sl6=True)
    #if status != 0: quit(str(status))
