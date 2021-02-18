#!/bin/env python
import GridEngineTools
import os
import glob

# generate Autumn18 MC, all steps
# comments @ Viktor Kutzner

# select steps:
step_gensim = 0
step_digi   = 0
step_reco   = 1
step_rereco = 1
overwrite   = 0
runmode     = "grid"
confirm     = 0
use_sl6     = 0

# GT: 102X_upgrade2018_realistic_v11

# set up CMSSW:
if not os.path.exists("CMSSW_10_2_5"):
    os.system("export SCRAM_ARCH=slc7_amd64_gcc700; scramv1 project CMSSW CMSSW_10_2_5; cd CMSSW_10_2_5/src; eval `scramv1 runtime -sh`; scram b -j10")

# generate Autumn18 GEN-SIM:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/MUO-RunIIFall18wmLHEGS-00001
if step_gensim:
        
    command = r"""tdir=$(mktemp -d /tmp/foo.XXXXXXXXX); cd $tdir; export SCRAM_ARCH=slc7_amd64_gcc700; scramv1 project CMSSW CMSSW_10_2_3; cd CMSSW_10_2_3/src; eval `scramv1 runtime -sh`; curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/MUO-RunIIFall18wmLHEGS-00001 --retry 3 --create-dirs -o Configuration/GenProduction/python/MUO-RunIIFall18wmLHEGS-00001-fragment.py; scram b; cmsDriver.py Configuration/GenProduction/python/MUO-RunIIFall18wmLHEGS-00001-fragment.py --python_filename MUO-RunIIFall18wmLHEGS-00001_1_$SEED_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:$OUTFILE --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=$SEED\\nprocess.source.numberEventsInLuminosityBlock="cms.untracked.uint32(227)" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIFall18wmLHEGS-00001_report.xml MUO-RunIIFall18wmLHEGS-00001_1_$SEED_cfg.py"""
    
    outdir = "Autumn18_GENSIM"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i in range(200,400):
        outfile = "/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/" + outdir + "/seed_%s.root" % i
        if not overwrite and os.path.exists(outfile): continue
        this_command = command.replace("$OUTFILE", outfile).replace("$NEV", "200").replace("$SEED", str(i))
        commands.append(this_command)
    
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.Autumn18gen1", confirm=confirm, use_sl6=use_sl6)


# generate Autumn18 DIGI:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/MUO-RunIIAutumn18DRPremix-00012
if step_digi:

    command = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_2_5/src; eval `scramv1 runtime -sh`; cmsDriver.py  --python_filename MUO-RunIIAutumn18DRPremix-00012_1_$NUM_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:$OUTFILE --pileup_input file:///nfs/dust/cms/user/kutznerv/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/PUAutumn18_102X_upgrade2018_realistic_v15-v1/110006/86483043-B8C9-9244-89C0-2C87F65A5EC7.root --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:$INFILE --datamix PreMix --era Run2_2018 --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIAutumn18DRPremix-00012_0_report.xml MUO-RunIIAutumn18DRPremix-00012_1_$NUM_cfg.py"""
    
    outdir = "Autumn18_DIGI"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Autumn18_GENSIM/*root")):
        
        if "_inLHE" in infile: continue
        
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        if not overwrite and os.path.exists(outdir + "/" + infile.split("/")[-1]): continue
        this_command = command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "-1").replace("$NUM", str(i))
        commands.append(this_command)
        
    os.system("rm condor.Autumn18gen2/*")
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.Autumn18gen2", confirm=confirm, use_sl6=use_sl6)
    #if status != 0: quit(str(status))

# generate Autumn18 RECO:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/MUO-RunIIAutumn18DRPremix-00012
if step_reco:
        
    command = """cd /nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/CMSSW_10_2_5/src; eval `scramv1 runtime -sh`; cmsDriver.py --python_filename MUO-RunIIAutumn18DRPremix-00012_2_$NUM_cfg.py --eventcontent RECOSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RECO --fileout file:$OUTFILE --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO --procModifiers premix_stage2 --filein file:$INFILE --era Run2_2018 runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j MUO-RunIIAutumn18DRPremix-00012_report.xml MUO-RunIIAutumn18DRPremix-00012_2_$NUM_cfg.py"""
    
    outdir = "Autumn18_RECO"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Autumn18_DIGI/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        if not overwrite and os.path.exists(outdir + "/" + infile.split("/")[-1]): continue
        this_command = command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "-1").replace("$NUM", str(i))
        commands.append(this_command)

    os.system("rm condor.Autumn18gen3/*")
    status = GridEngineTools.runParallel(commands, runmode, condorDir="condor.Autumn18gen3", confirm=confirm, use_sl6=use_sl6)
    #if status != 0: quit(str(status))


if step_rereco:
    os.system("./submit_rereco.py --period Autumn18")
