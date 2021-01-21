#!/bin/env python
import GridEngineTools
import os
import glob
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--period", dest = "period", default = "Run2016")
(options, args) = parser.parse_args()

# run hit removal tool and do second reconstruction
# comments @ Viktor Kutzner

period              = options.period
step_clustersurgeon = 0
step_reco           = 1
runmode             = "grid"
confirm             = 0

def runSL6(command):
    singularity_wrapper = "singularity exec --contain --bind /afs:/afs --bind /nfs:/nfs --bind /pnfs:/pnfs --bind /cvmfs:/cvmfs --bind /var/lib/condor:/var/lib/condor --bind /tmp:/tmp --pwd . ~/dust/slc6_latest.sif sh -c 'source /cvmfs/cms.cern.ch/cmsset_default.sh; $CMD'"
    os.system(singularity_wrapper.replace("$CMD", command))

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
elif period == "Run2017B":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017B/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/6000*/*root"    
elif period == "Run2017F":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017F/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/60000/*root"    
elif period == "Run2018A":
    cmssw = "CMSSW_10_2_4_patch1"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2018A/SingleMuon/RAW-RECO/ZMu-17Sep2018-v2/10000*/*root"    
elif period == "Run2018D":
    cmssw = "CMSSW_10_2_5_patch1"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/321/2*/*/*root"    
elif period == "Summer16":
    cmssw = "CMSSW_8_0_21"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*root"
elif period == "Fall17":
    cmssw = "CMSSW_9_4_0" #TODO: _patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17_RECO/*root"
else:
    quit("which period?")
    
# set up CMSSW:
if not os.path.exists("%s/src/shorttrack" % cmssw):
    runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))

# modify hit collections:
if step_clustersurgeon:
    commands = []
    for i, i_file in enumerate(glob.glob(inputpath)):
        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file://%s outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER/rCluster_%s_allSteps_%s.root" % (cmssw, i_file, period, period, i+1))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER" % period)
    os.system("rm condor.%s/*" % period)
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=confirm, use_sl6=True)
    #if status != 0: quit(str(status))


# do rereco with modified hit collections:
if step_reco:
    commands = []
    for i_file in glob.glob("%s_HITREMOVER/*root" % period):
        o_file = i_file.replace("HITREMOVER", "RERECO").replace(".root", "")
        for step in range(1, 21):
            commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py inputFiles=file://../../%s outputFileName=../../%s step=%s MuonSeeds=1" % (cmssw, period, i_file, o_file, step))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_RERECO" % period)
    os.system("rm condor.%s/*" % period)
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=confirm, use_sl6=True)
    #if status != 0: quit(str(status))
