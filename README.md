# UHH Track Shortening Tool

Original author: Alexandra Tews, adapted for Disappearing Track analysis by Viktor Kutzner

## Setup

* clone in parallel to analysis repo
* needs SL6 for now, run on naf-cms11 or using `singularity`

## Steps

* generate RECO files for MC with `submit_mcgen_Summer16.py`
* run track hit removal tool and re-reconstruction with `submit_rereco.py`
* get efficiency plots with `submit_analyzer.py`
