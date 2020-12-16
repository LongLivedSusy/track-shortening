#!/bin/env python
import GridEngineTools
import os
import glob

# generate Summer16 MC, all steps
# comments @ Viktor Kutzner

# select steps:
step_gensim = 0
step_digi   = 1
step_reco   = 0
step_rereco = 0
step_aod    = 0

# set up CMSSW:
if not os.path.exists("CMSSW_7_1_20_patch3"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; cmsrel CMSSW_7_1_20_patch3; cd CMSSW_7_1_20_patch3/src; eval `scramv1 runtime -sh`; scram b -j10")
if not os.path.exists("CMSSW_8_0_21"):
    os.system("export SCRAM_ARCH=slc6_amd64_gcc530; cmsrel CMSSW_8_0_21; cd CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; scram b -j10")

# generate Summer16 GEN-SIM:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/SUS-RunIISummer15GS-00148
if step_gensim:
    example_command = "cd ~/dust/shorttrack/track-shortening/CMSSW_7_1_20_patch3/src; eval `scramv1 runtime -sh`; cmsDriver.py Configuration/GenProduction/python/SUS-RunIISummer15GS-00148-fragment.py --python_filename SUS-RunIISummer15GS-00148_1_$NUM_cfg.py --eventcontent RAWSIM --datatier GEN-SIM --fileout file:$OUTFILE --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --filein file://$INFILE --no_exec --mc -n $NEV; cmsRun -e -j SUS-RunIISummer15GS-00148_report.xml SUS-RunIISummer15GS-00148_1_$NUM_cfg.py"
    
    outdir = "Summer16_GENSIM"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/afs/desy.de/user/k/kutznerv/dust/store/mc/RunIIWinter15wmLHE/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/LHE/MCRUN2_71_V1_ext1-v1/30000/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "1000").replace("$NUM", str(i))
        commands.append(this_command)
    
    commands = GridEngineTools.shoot_cmds_into_sl6_singularity(commands)
    GridEngineTools.runParallel(commands, "grid", confirm=False, use_sl6=False)

# generate Summer16 DIGI:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/SUS-RunIISummer16DR80Premix-00036
if step_digi:
    example_command = "cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; cmsDriver.py --python_filename SUS-RunIISummer16DR80Premix-00036_1_$NUM_cfg.py --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --fileout file:$OUTFILE --pileup_input dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --filein file://$INFILE --datamix PreMix --era Run2_2016 --no_exec --mc -n $NEV; cmsRun -e -j SUS-RunIISummer16DR80Premix-00036_0_report.xml SUS-RunIISummer16DR80Premix-00036_1_$NUM_cfg.py"
    
    outdir = "Summer16_DIGI"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_GENSIM/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "1000").replace("$NUM", str(i))
        commands.append(this_command)
        
    commands = GridEngineTools.shoot_cmds_into_sl6_singularity(commands)
    GridEngineTools.runParallel(commands, "multi", confirm=False, use_sl6=False)

# generate Summer16 RECO:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/SUS-RunIISummer16DR80Premix-00036
if step_reco:
    example_command = 'cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; cmsDriver.py --python_filename SUS-RunIISummer16DR80Premix-00036_2_$NUM_cfg.py --eventcontent RECOSIM --datatier GEN-SIM-RECO --fileout file:$OUTFILE --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO --filein file:$INFILE --era Run2_2016 --runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j SUS-RunIISummer16DR80Premix-00036_report.xml SUS-RunIISummer16DR80Premix-00036_2_$NUM_cfg.py; cd -'
    
    outdir = "Summer16_RECO"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_DIGI/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "1000").replace("$NUM", str(i))
        commands.append(this_command)

    commands = GridEngineTools.shoot_cmds_into_sl6_singularity(commands)    
    GridEngineTools.runParallel(commands, "grid", confirm=False, use_sl6=False)

# generate Summer16 reRECO:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/SUS-RunIISummer16DR80Premix-00036
if step_rereco:
    example_command = 'cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; cmsDriver.py  --python_filename SUS-RunIISummer16DR80Premix-00036_2b_$NUM_cfg.py --eventcontent RECOSIM --datatier RECOSIM --process reRECO --fileout file:$OUTFILE --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RECO --filein file:$INFILE --era Run2_2016 --runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j SUS-RunIISummer16DR80Premix-00036_report.xml SUS-RunIISummer16DR80Premix-00036_2b_$NUM_cfg.py; cd -'
    
    outdir = "Summer16_reRECO"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "1000").replace("$NUM", str(i))
        commands.append(this_command)
    
    commands = GridEngineTools.shoot_cmds_into_sl6_singularity(commands)
    GridEngineTools.runParallel(commands, "grid", confirm=False, use_sl6=False)

# generate Summer16 AOD:
# recipe from https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/SUS-RunIISummer16DR80Premix-00036
if step_aod:
    example_command = 'cd ~/dust/shorttrack/track-shortening/CMSSW_8_0_21/src; eval `scramv1 runtime -sh`; cmsDriver.py  --python_filename SUS-RunIISummer16DR80Premix-00036_3_$NUM_cfg.py --eventcontent AODSIM --datatier AODSIM --fileout file:$OUTFILE --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step EI --filein file:$INFILE --era Run2_2016 --runUnscheduled --no_exec --mc -n $NEV; cmsRun -e -j SUS-RunIISummer16DR80Premix-00036_report.xml SUS-RunIISummer16DR80Premix-00036_3_$NUM_cfg.py; cd -'
    
    outdir = "Summer16_AODSIM"
    os.system("mkdir -p %s" % outdir)
    
    commands = []
    for i, infile in enumerate(glob.glob("/nfs/dust/cms/user/kutznerv/shorttrack/track-shortening/Summer16_RECO/*root")):
        outfile = "../../" + outdir + "/" + infile.split("/")[-1]
        this_command = example_command.replace("$INFILE", infile).replace("$OUTFILE", outfile).replace("$NEV", "1000").replace("$NUM", str(i))
        commands.append(this_command)
    
    commands = GridEngineTools.shoot_cmds_into_sl6_singularity(commands)
    GridEngineTools.runParallel(commands, "grid", confirm=False, use_sl6=False)
