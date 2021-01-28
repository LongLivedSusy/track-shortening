#!/bin/env python
import GridEngineTools
import os
import glob
from optparse import OptionParser

# run hit removal tool and do second reconstruction
# comments @ Viktor Kutzner

parser = OptionParser()
parser.add_option("--period", dest = "period", default = "Run2016")
parser.add_option("--step", dest = "step", default = 0)
parser.add_option("--ultralegacy", dest = "ultralegacy", action = "store_true")
parser.add_option("--confirm", dest = "confirm", action = "store_true")
(options, args) = parser.parse_args()

runmode             = "grid"
period              = options.period
use_sl6             = True

if int(options.step) == 0:
    step_clustersurgeon = 1
    step_reco           = 1
elif int(options.step) == 1:
    step_clustersurgeon = 1
    step_reco           = 0
elif int(options.step) == 2:
    step_clustersurgeon = 0
    step_reco           = 1

def runSL6(command):
    singularity_wrapper = "singularity exec --contain --bind /afs:/afs --bind /nfs:/nfs --bind /pnfs:/pnfs --bind /cvmfs:/cvmfs --bind /var/lib/condor:/var/lib/condor --bind /tmp:/tmp --pwd . ~/dust/slc6_latest.sif sh -c 'source /cvmfs/cms.cern.ch/cmsset_default.sh; $CMD'"
    os.system(singularity_wrapper.replace("$CMD", command))

if period == "Run2016":
    # this is the prompt reco
    cmssw = "CMSSW_8_0_22"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco*/*/*/*/*/*"
elif period == "Run2016B":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016B/SingleMuon/RAW-RECO/ZMu-07Aug17_ver2-v1/*/*"
elif period == "Run2016C":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016C/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016D":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016D/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016E":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016E/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016F":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016F/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016G":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016G/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016H":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"    
elif period == "Run2017B":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017B/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017C":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017D":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017D/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017E":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017E/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017F":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017F/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2018A":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2018A/SingleMuon/RAW-RECO/ZMu-17Sep2018-v2/*/*"    
elif period == "Run2018B":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-17Sep2018-v1/*/*"    
elif period == "Run2018C":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2018C/SingleMuon/RAW-RECO/ZMu-17Sep2018-v1/*/*"    
elif period == "Run2018D":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/*/*/*/*/*"    
elif period == "Summer16":
    cmssw = "CMSSW_8_0_21"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*"
elif period == "Fall17":
    cmssw = "CMSSW_9_4_0" #CMSSW_9_4_0_patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17_RECO/*"
else:
    quit("which period?")
    
# override settings when running on UL
if options.ultralegacy:
    cmssw = "CMSSW_10_6_2"
    #inputpath = "/nfs/dust/cms/user/kutznerv/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-09Aug2019_UL2017-v1/*/*.root"
    use_sl6 = False
    suffix = "UL"
else:
    suffix = ""
    
# set up CMSSW:
if not os.path.exists("%s/src/shorttrack" % cmssw):
    if use_sl6:
        runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))
    else:
        if cmssw == "CMSSW_10_6_2":
            os.system("export SCRAM_ARCH=slc7_amd64_gcc820; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; cp -r ../../shorttrack shorttrack; cp ../../CMSSW_10_6_2_support/src/shorttrack/TrackRefitting/plugins/RClusterProducer.cc shorttrack/TrackRefitting/plugins/; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))
        else:
            os.system("export SCRAM_ARCH=slc7_amd64_gcc820; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))

# modify hit collections:
if step_clustersurgeon:
    commands = []
    for i, i_file in enumerate(glob.glob(inputpath)):
        outfile = i_file.split("/")[-1].replace(".root", "")
        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file://%s outputFile=/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER%s/rCluster_%s_%s_allSteps_%s.root" % (cmssw, i_file, period, suffix, outfile, period, i+1))
        
        #if options.ultralegacy:
        #    commands[-1] = commands[-1] + " ultralegacy=1"

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER%s" % (period, suffix))
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=options.confirm, use_sl6=use_sl6)


# do rereco with modified hit collections and remove input:
if step_reco:
    
    commands = []
    for i_file in glob.glob("%s_HITREMOVER%s/*root" % (period, suffix)):
        o_file = i_file.replace("HITREMOVER%s" % suffix, "RERECO%s" % suffix).replace(".root", "")
        for step in range(1, 21):
            if use_sl6:
                commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s%s.py inputFiles=file://../../%s outputFileName=../../%s step=%s MuonSeeds=1" % (cmssw, period, suffix, i_file, o_file, step))
            else:
                commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s%s.py inputFiles=file://../../../../%s outputFileName=../../../../%s step=%s MuonSeeds=1" % (cmssw, period, suffix, i_file, o_file, step))
                

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_RERECO%s" % (period, suffix))
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s" % period, confirm=options.confirm, use_sl6=use_sl6)
