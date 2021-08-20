#!/bin/env python
import os
import time

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


periods = [
            #"Summer16",
            #"Fall17",
            #"Autumn18",
            #"Run2016B",    ##
            #"Run2016C",     ##
            #"Run2016D",    ##
            #"Run2016E",     #
            #"Run2016F",     #
            #"Run2016G",     #
            #"Run2016H",    ##
            "Run2017B",     #?
            #"Run2017C",     ##
            "Run2017D",     #?
            "Run2017E",     #?
            "Run2017F",     #?
            "Run2018A",     #?
            #"Run2018B",     #>>
            #"Run2018C",     #>>
            "Run2018D",     #?
            #"RunUL2017C",
          ]

#for period in periods:
#    os.system("./submit_rereco.py --period %s --step 3 &" % period)

for i, i_chunk in enumerate(chunks(periods, 3)):
    for period in i_chunk:
        #os.system("./submit_rereco.py --period %s &" % period)
        os.system("./submit_rereco.py --period %s --step 3 &" % period)
    time.sleep(60*60*2)

