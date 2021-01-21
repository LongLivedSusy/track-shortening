#!/bin/env python
import sys
import os
import commands
import glob

datasets = []
blocks = []
files = []

for dataset in datasets:
    status, output = commands.getstatusoutput("""dasgoclient --query="file dataset=%s" """ % dataset)
    files += output.split("\n")

for block in blocks:
    status, output = commands.getstatusoutput("""dasgoclient --query="file block=%s" """ % block)
    files += output.split("\n")

files = [
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20052/E06CBB83-1BCE-E711-ABF0-A4BF011259E0.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/56CAC54B-0CCE-E711-BF07-001E677924AE.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/B6EBA3F2-0ACE-E711-9204-001E677925E6.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/86C2D6D2-0ACE-E711-8A58-001E67E6F869.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20051/2EA05F08-17CE-E711-8DEC-A4BF0112BC6A.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/DEA8DCBE-11CE-E711-B349-001E67396D56.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/DE8E59BB-11CE-E711-A45A-001E67792574.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/88186559-11CE-E711-9E04-A4BF01125A40.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/86FA1C76-11CE-E711-A6BD-001E67E63AE6.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/3E5AD3C1-10CE-E711-BE25-001E67792738.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/18F36CEC-10CE-E711-97D3-A4BF0108B0FA.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/566B596C-11CE-E711-BD97-A4BF01125B58.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/EC64F207-11CE-E711-8AE4-A4BF0112BDF8.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/CC619CDE-0DCE-E711-A0F5-A4BF01125500.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/7CF5E742-15CE-E711-B5D1-A4BF0112BE0E.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/06A76413-14CE-E711-93A2-A4BF01125620.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/6E43B0F0-13CE-E711-9D1F-001E677928A4.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/5202D395-12CE-E711-A1E1-A4BF0112DB7C.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20000/6833D6DC-21CE-E711-ABF0-001E677925E8.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20045/D6B74826-00CE-E711-AFEE-002590200B00.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/287B88CE-0CCE-E711-BC12-001E67792768.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/46637FBD-0CCE-E711-B5A1-002590A36FA2.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/62304DD9-0CCE-E711-8531-A4BF0112BDCC.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/14F2F5BD-0BCE-E711-8DFE-A4BF01125880.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/52765BC3-0BCE-E711-AAE2-A4BF01125548.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/9E123B9C-0BCE-E711-B5E7-A4BF0112BCAC.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/5C828131-11CE-E711-9DF5-A4BF0112BC2E.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/FA9A861B-11CE-E711-8F94-A4BF0112BC0A.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20049/220E4FE0-10CE-E711-A7BE-001E67792458.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/782FB2F3-13CE-E711-8D4F-A4BF011259E0.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/3E41C07C-13CE-E711-B0A4-A4BF0108B54A.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/D62F269F-13CE-E711-96EE-A4BF0112BE48.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/5A6EB585-12CE-E711-B988-A4BF0112BD04.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/A85B6590-12CE-E711-A56E-A4BF010F1208.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/B6B7659F-11CE-E711-A01C-A4BF0108B3D2.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20050/CECCBA9F-11CE-E711-883E-A4BF0112DD7C.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20043/183E123B-F0CD-E711-89FD-001E67398633.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/3602CE48-0DCE-E711-BA50-001E67E69879.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/34D3FDA9-0CCE-E711-AC06-A4BF0112BCFA.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/C6E501B1-0CCE-E711-8161-A4BF01125AB0.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/46311B8B-0CCE-E711-8A53-001E673972C4.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/A8085A45-0CCE-E711-82D2-A4BF0112BC4C.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/7C95C64A-0CCE-E711-AE59-001E67E71BFF.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/A8F227D4-0BCE-E711-8AE7-A4BF01125B00.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20045/66A6C17C-FDCD-E711-8E4B-001E67792442.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/7AAB1A81-09CE-E711-902A-A4BF0112BCCA.root",
    "/store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/20048/0862869A-08CE-E711-B351-A4BF0112BC14.root",
]


print files

for ifile in files:
    
    print ifile
    folder = "/".join(ifile.split("/")[:-1])
    os.system("mkdir -p /nfs/dust/cms/user/kutznerv/%s" % folder)

    if os.path.exists("/nfs/dust/cms/user/kutznerv/%s/%s" % (folder, ifile.split("/")[-1])):
        print "already there"
        continue
    
    #os.system("cp /pnfs/desy.de/cms/tier2/%s ~/dust/%s/" % (ifile, folder))
    os.system("xrdcp root://cmsxrootd.fnal.gov/%s ~/dust%s" % (ifile, ifile))
    
    