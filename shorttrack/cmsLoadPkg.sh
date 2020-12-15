#!/bin/bash

# faster way to get cmssw packages with available cvmfs mount
# usage: ./cmsLoadPkg CondFormats HcalObjects

if [ -d "$CMSSW_BASE"/src/"$1"/"$2" ]
then
    echo "Package already installed."
else
    mkdir -p "$CMSSW_BASE"/src/"$1"/"$2"
    cp -r /cvmfs/cms.cern.ch/"$SCRAM_ARCH"/cms/cmssw/"$CMSSW_VERSION"/src/"$1"/"$2" "$CMSSW_BASE"/src/"$1"/
fi



