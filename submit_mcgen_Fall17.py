#!/bin/env python
import GridEngineTools
import os
import glob

# generate Fall17 MC, all steps
# comments @ Viktor Kutzner

# select steps:
step_gensim = 0
step_digi   = 1
step_reco   = 1
step_digi_and_reco = 0
step_rereco = 1
overwrite   = 0
ultralegacy = 0
runmode     = "grid"
confirm     = 0
use_sl6     = 1

# TODO: was patch1, here without:

# set up CMSSW:
if not os.path.exists("CMSSW_9_4_0"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc630; scramv1 project CMSSW CMSSW_9_4_0; cd CMSSW_9_4_0/src; eval `scramv1 runtime -sh`; scram b -j10")
if not os.path.exists("CMSSW_9_4_0_patch1"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc630; scramv1 project CMSSW CMSSW_9_4_0_patch1; cd CMSSW_9_4_0_patch1/src; eval `scramv1 runtime -sh`; scram b -j10")

# generate Fall17 GEN-SIM:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/MUO-RunIIFall17wmLHEGS-00002
if step_gensim:
        
    example_command = r"""tdir=$(mktemp -d /tmp/foo.XXXXXXXXX); cd $tdir; export SCRAM_ARCH=slc6_amd64_gcc630; scramv1 project CMSSW CMSSW_9_3_1; cd CMSSW_9_3_1/src; eval `scramv1 runtime -sh`; curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/MUO-RunIIFall17wmLHEGS-00002 --retry 3 --create-dirs -o Configuration/GenProduction/python/MUO-RunIIFall17wmLHEGS-00002-fragment.py; scram b; cmsDriver.py Configuration/GenProduction/python/MUO-RunIIFall17wmLHEGS-00002-fragment.py --python_filename MUO-RunIIFall17wmLHEGS-00002_1_$SEED_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:$OUTFILE --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=$SEED\\nprocess.source.numberEventsInLuminosityBlock="cms.untracked.uint32(227)" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2017 --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall17wmLHEGS-00002_report.xml MUO-RunIIFall17wmLHEGS-00002_1_$SEED_cfg.py"""
    
    outdir = "Fall17_GENSIM"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    #for i in range(1,200):
    for i in range(200,400):
        outfile = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/" + outdir + "/seed_%s.root" % i
        if not overwrite and os.path.exists(outfile): continue
        this_command = example_command.replace("$OUTFILE", outfile).replace("$NEV", "200").replace("$SEED", str(i))
        commands.append(this_command)
    
    os.system("rm condor.fall17gen1/*")
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.fall17gen1", confirm=confirm, use_sl6=use_sl6)
    #if status != 0: quit(str(status))


# generate Fall17 DIGI:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/MUO-RunIIFall17DRPremix-00026
if step_digi:
    
    example_command = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_9_4_0/src; eval `scramv1 runtime -sh`; cmsDriver.py  --python_filename MUO-RunIIFall17DRPremix-00026_1_$NUM_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:$OUTFILE --pileup_input "file:/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20052/E06CBB83-1BCE-E711-ABF0-A4BF011259E0.root" --conditions 94X_mc2017_realistic_v10 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --filein file:$INFILE --datamix PreMix --era Run2_2017 --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall17DRPremix-00026_0_report.xml MUO-RunIIFall17DRPremix-00026_1_$NUM_cfg.py"""
    
    outdir = "Fall17_DIGI"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17_GENSIM/*root")):
        
        if "_inLHE" in infile: continue
        
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        if not overwrite and os.path.exists(outdir + "/" + infile.split("/")[-1]): continue
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "-1").replace("$NUM", str(i))
        commands.append(this_command)
        
    os.system("rm condor.fall17gen2/*")

    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.fall17gen2", confirm=confirm, use_sl6=use_sl6)
    #if status != 0: quit(str(status))

# generate Fall17 RECO:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/MUO-RunIIFall17DRPremix-00026
if step_reco:
    
    if not ultralegacy:
        example_command = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_9_4_0/src; eval `scramv1 runtime -sh`; cmsDriver.py --python_filename MUO-RunIIFall17DRPremix-00026_2_$NUM_cfg.py --eventcontent RECOSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RECO --fileout file:$OUTFILE --conditions 94X_mc2017_realistic_v10 --step RAW2DIGI,RECO --filein file:$INFILE --era Run2_2017 runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall17DRPremix-00026_report.xml MUO-RunIIFall17DRPremix-00026_2_$NUM_cfg.py"""
        outdir = "Fall17_RECO"
        
    else:
        example_command = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_6_2/src; eval `scramv1 runtime -sh`; cmsDriver.py --python_filename MUO-RunIIFall17DRPremix-00026_2_$NUM_cfg.py --eventcontent RECOSIM --datatier GEN-SIM-RECO --fileout file:$OUTFILE --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO --filein file:$INFILE --era Run2_2017,pf_badHcalMitigation --customise Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2018 --runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall17DRPremix-00026_report.xml MUO-RunIIFall17DRPremix-00026_2_$NUM_cfg.py"""
        outdir = "Fall17UL_RECO"
        
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17_DIGI/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        if not overwrite and os.path.exists(outdir + "/" + infile.split("/")[-1]): continue
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "-1").replace("$NUM", str(i))
        commands.append(this_command)

    os.system("rm condor.fall17gen3/*")
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.fall17gen3", confirm=confirm, use_sl6=use_sl6)
    #if status != 0: quit(str(status))


if step_digi_and_reco:
    
    example_command_digi = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_9_4_0/src; eval `scramv1 runtime -sh`; cmsDriver.py  --python_filename MUO-RunIIFall17DRPremix-00026_1_$NUM_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:$OUTFILE --pileup_input "file:/pnfs/desy.de/cms/tier2/store/user/vkutzner/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20052/E06CBB83-1BCE-E711-ABF0-A4BF011259E0.root" --conditions 94X_mc2017_realistic_v10 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --filein file:$INFILE --datamix PreMix --era Run2_2017 --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall17DRPremix-00026_0_report.xml MUO-RunIIFall17DRPremix-00026_1_$NUM_cfg.py"""
    example_command_reco = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_6_2/src; eval `scramv1 runtime -sh`; cmsDriver.py --python_filename MUO-RunIIFall17DRPremix-00026_2_$NUM_cfg.py --eventcontent RECOSIM --datatier GEN-SIM-RECO --fileout file:$OUTFILE --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO --filein file:$INFILE --era Run2_2017,pf_badHcalMitigation --customise Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2018 --runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall17DRPremix-00026_report.xml MUO-RunIIFall17DRPremix-00026_2_$NUM_cfg.py && rm $INFILE"""
    
    outdir = "Fall17_DIGI"
    os.system("mkdir -p %s" % outdir)
    outdir = "Fall17_RECO"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Fall17_GENSIM/*root")):
        
        if "_inLHE" in infile: continue
        
        outdir = "Fall17_DIGI"
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        if not overwrite and os.path.exists(outdir + "/" + infile.split("/")[-1]): continue
        this_command_digi = example_command_digi.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "-1").replace("$NUM", str(i))
        
        outdir = "Fall17_RECO"
        infile = infile.replace("_GENSIM", "_DIGI")
        if not overwrite and os.path.exists(outdir + "/" + infile.split("/")[-1]): continue
        this_command_reco = example_command_reco.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "-1").replace("$NUM", str(i))
        
        commands.append(this_command_digi + "; " + this_command_reco)
        
    os.system("rm condor.fall17gen2/*")
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.fall17gen2", confirm=confirm, use_sl6=use_sl6)
    #if status != 0: quit(str(status))



if step_rereco:
    
    if not ultralegacy:
        os.system("./submit_rereco.py --period Fall17")
    else:
        os.system("./submit_rereco.py --period Fall17UL")
