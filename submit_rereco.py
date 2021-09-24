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
parser.add_option("--confirm", dest = "confirm", action = "store_true")
parser.add_option("--recompile", dest = "recompile", action = "store_true")
(options, args) = parser.parse_args()

runmode             = "grid"
period              = options.period
use_sl6             = True

if int(options.step) == 0:
    step_clustersurgeon = 1
    step_hadd           = 0
    step_reco           = 1
elif int(options.step) == 1:
    step_clustersurgeon = 1
    step_hadd           = 0
    step_reco           = 0
elif int(options.step) == 2:
    step_clustersurgeon = 0
    step_hadd           = 1
    step_reco           = 0
elif int(options.step) == 3:
    step_clustersurgeon = 0
    step_hadd           = 0
    step_reco           = 1


def runSL6(command):
    singularity_wrapper = "singularity exec --contain --bind /afs:/afs --bind /nfs:/nfs --bind /pnfs:/pnfs --bind /cvmfs:/cvmfs --bind /var/lib/condor:/var/lib/condor --bind /tmp:/tmp --pwd . ~/dust/slc6_latest.sif sh -c 'source /cvmfs/cms.cern.ch/cmsset_default.sh; $CMD'"
    os.system(singularity_wrapper.replace("$CMD", command))


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if period == "Run2016":
    # this is the prompt reco
    cmssw = "CMSSW_8_0_22"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-PromptReco*/*/*/*/*/*"
elif period == "Run2016B":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016B/SingleMuon/RAW-RECO/ZMu-07Aug17_ver2-v1/*/*"
elif period == "Run2016C":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016C/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016D":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016D/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016E":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016E/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016F":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016F/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016G":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016G/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"
elif period == "Run2016H":
    cmssw = "CMSSW_8_0_29"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2016H/SingleMuon/RAW-RECO/ZMu-07Aug17-v1/*/*"    
elif period == "Run2017B":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017B/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017C":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"
elif period == "Run2017D":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017D/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017E":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017E/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2017F":
    cmssw = "CMSSW_9_4_0"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017F/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"    
elif period == "Run2018A":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2018A/SingleMuon/RAW-RECO/ZMu-17Sep2018-v2/*/*"    
elif period == "Run2018B":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-17Sep2018-v1/*/*"    
elif period == "Run2018C":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2018C/SingleMuon/RAW-RECO/ZMu-17Sep2018-v1/*/*"    
elif period == "Run2018D":
    cmssw = "CMSSW_10_2_7" #CMSSW_10_2_4_patch1
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/*/*/*/*/*"    
elif period == "Summer16":
    cmssw = "CMSSW_8_0_21"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*"
elif period == "Fall17":
    cmssw = "CMSSW_9_4_0" #CMSSW_9_4_0_patch1
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17_RECO/*"
elif period == "Autumn18":
    cmssw = "CMSSW_10_2_7" #"CMSSW_10_2_5"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Autumn18_RECO/*"
elif period == "Fall17UL":
    cmssw = "CMSSW_10_6_2"
    inputpath = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17UL_RECO/*"
    use_sl6 = False
elif period == "RunUL2017C":
    cmssw = "CMSSW_10_6_2"
    #inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-17Nov2017-v1/*/*"
    inputpath = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-09Aug2019_UL2017-v1/*/*"
    use_sl6 = False
else:
    quit("which period?")
        

# set up CMSSW:
if not os.path.exists("%s/src/shorttrack" % cmssw):
    if use_sl6:
        runSL6("export SCRAM_ARCH=slc6_amd64_gcc530; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))
    else:
        if cmssw == "CMSSW_10_6_2":
            os.system("export SCRAM_ARCH=slc7_amd64_gcc820; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; cp -r ../../shorttrack shorttrack; cp ../../CMSSW_10_6_2_support/src/shorttrack/TrackRefitting/plugins/RClusterProducer.cc shorttrack/TrackRefitting/plugins/; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))
        else:
            os.system("export SCRAM_ARCH=slc7_amd64_gcc820; scramv1 project CMSSW %s; cd %s/src; eval `scramv1 runtime -sh`; ln -s ../../shorttrack shorttrack; cd shorttrack; chmod +x ./setup.sh; ./setup.sh; cd ..; scram b -j10" % (cmssw, cmssw))


if options.recompile:
    for cmssw in [
        "CMSSW_8_0_21",
        "CMSSW_8_0_22",
        "CMSSW_8_0_29",
        "CMSSW_9_4_0",
        "CMSSW_10_2_7",
                 ]:
                 
        runSL6("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; scram b -j20" % cmssw)
    
    print "non-UL cmssw releases recompiled!"
    quit()
    

# modify hit collections:
if step_clustersurgeon:
    commands = []
    for i, i_file in enumerate(glob.glob(inputpath)):
        outfile = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER/rCluster_%s_%s_allSteps_%s.root" % (period, i_file.split("/")[-1].replace(".root", ""), period, i+1)

        # check if already there:
        if os.path.exists(outfile):
            print "Exists:", outfile
            continue

        commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/ClusterSurgeon.py inputFiles=file://%s outputFile=%s" % (cmssw, i_file, outfile))

        # limit number of RECO input files...
        if period == "RunUL2017C" and i > 4:
            break
        
    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_HITREMOVER" % (period))
    if len(commands)>0:
        status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s_step1" % period, confirm=options.confirm, use_sl6=use_sl6)


#if step_hadd:
#
#    # do this if number of files reaches more than 200 files
#    
#    if len(glob.glob("%s_HITREMOVER/*root" % (period)))>200:
#        
#        commands = []
#        files = glob.glob("%s_HITREMOVER/*root" % (period))
#        for i, i_chunk in enumerate(chunks(files, 10)):
#            command = "hadd -f %s_HITREMOVER/chunk_%s.root " % (period, i)
#            for i_file in i_chunk:
#                command += i_file + " "
#            command += " && rm "
#            for i_file in i_chunk:
#                command += i_file + " "
#                
#            commands.append(command)
#                                
#        status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s_step2" % period, confirm=options.confirm)
            
            
# do rereco with modified hit collections and remove input:
if step_reco:
    
    commands = []
    
    files = glob.glob("%s_HITREMOVER/*root" % (period))
    for i, i_chunk in enumerate(chunks(files, 1)):
    #for i, i_chunk in enumerate(chunks(files, 10)):
    
        o_file = i_chunk[0].replace("HITREMOVER", "RERECO").replace(".root", "")
        
        # check if already there:
        if os.path.exists(o_file):
            print "Exists:", outfile
            continue
        
        inputFiles = ""
        
        for i_file in i_chunk:
            if use_sl6:
                inputFiles += "inputFiles=file://../../%s " % i_file
            else:
                inputFiles += "inputFiles=file://../../../../%s " % i_file
            
        for step in range(1, 21):
            if use_sl6:
                commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py %s outputFileName=../../%s step=%s MuonSeeds=1" % (cmssw, period, inputFiles, o_file, step))
            else:
                commands.append("cd ~/dust/shorttrack/track-shortening/%s/src/; eval `scramv1 runtime -sh`; cd shorttrack/TrackRefitting/; cmsRun python/reRECO_%s.py %s outputFileName=../../../../%s step=%s MuonSeeds=1" % (cmssw, period, inputFiles, o_file, step))

    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/%s_RERECO" % (period))
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.%s_step3" % period, confirm=options.confirm, use_sl6=use_sl6)

    ## test for invalid files:
    #invalid_files = []
    #all_rereco_files_valid = True    
    #for arg in glob.glob("%s*RERECO/*root" % period):
    #    test = TFile(arg)
    #    if (test.IsZombie() or test.TestBit(TFile.kRecovered)):
    #        all_rereco_files_valid = False
    #        invalid_files.append(arg)
    #    test.Close()
    #
    #if all_rereco_files_valid:
    #    print "Will now delete input files after successful run..." 
    #    os.system("rm %s_HITREMOVER/*root" % period)
    #
    #if len(invalid_files)>0:
    #    print "invalid_files: %s" % invalid_files

    #if len(glob.glob("%s_RERECO/*root" % period)) > 20:
    #    os.system("rm %s_HITREMOVER/*root" % period)
