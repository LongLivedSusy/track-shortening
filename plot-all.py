#!/bin/env python
import os
import submit_analyzer

for suffix in submit_analyzer.suffixes:
              
    os.system("./plot-reweighting-scalefactors-and-efficiencies-combined.py --suffix %s &" % suffix)
    os.system("./plot-trackvariables-years.py --suffix %s &" % suffix)
    
    