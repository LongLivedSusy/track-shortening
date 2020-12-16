# UHH Track Shortening Tool

Original author: Alexandra Tews, adapted for Disappearing Track analysis by Viktor Kutzner

## Setup

* clone in parallel to analysis repo
* needs SL6 for now, run on naf-cms11 or using `singularity`

## Steps

* generate RECO files for MC with `submit_mcgen_Summer16.py`
* run track hit removal tool and re-reconstruction with `submit_rereco.py`
* get efficiency plots with `submit_analyzer.py`

## Set up `singularity` on the NAF

* pull the official CMSSW image to your DUST directory: `SINGULARITY_CACHEDIR="/nfs/dust/cms/user/$USER/singularity" singularity pull /nfs/dust/cms/user/$USER/slc6_latest.sif docker://cmssw/slc6:latest`
* test e.g. `singularity exec --contain --bind /afs:/afs --bind /nfs:/nfs --bind /pnfs:/pnfs --bind /cvmfs:/cvmfs --bind /var/lib/condor:/var/lib/condor --bind /tmp:/tmp --pwd . ~/dust/slc6_latest.sif sh -c 'echo "Running command in SL6 environment"'`
* for this collection of scripts, use up-to-date version of `GridEngineTools.py` from analysis/tools repository