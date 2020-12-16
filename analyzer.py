#! /usr/bin/env python
from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser

# inspect RECO and reRECO collections
# comments @ Viktor Kutzner

gROOT.SetBatch()        
gROOT.SetStyle('Plain') 

parser = OptionParser()
parser.add_option("--inputfile", dest = "inputfile", default = "")
(options, args) = parser.parse_args()

events = Events(options.inputfile)

layers_remaining = int(options.inputfile.split(".root")[0].split("_")[-1])
print "remaining layers:", layers_remaining

# create handle outside of loop
muons_handle  = Handle("std::vector<reco::Muon>")
tracks_handle  = Handle("std::vector<reco::Track>")
muons_rereco_handle  = Handle("std::vector<reco::Muon>")
tracks_rereco_handle  = Handle("std::vector<reco::Track>")

h_tracks_reco = TH1F("h_tracks_reco", "", 21, 0, 21)
h_tracks_rereco = TH1F("h_tracks_rereco", "", 21, 0, 21)

h_layers2D = TH2F("h_layers2D", ";targeted number of remaining layers; layers with meas. of matched track", 20, 0, 20, 20, 0, 20)

# loop over events
for i, event in enumerate(events):
    
    event.getByLabel("muons", "", "RECO", muons_handle)
    muons = muons_handle.product()
    
    event.getByLabel("rCluster%s" % layers_remaining, "", "HITREMOVER", tracks_handle)
    tracks = tracks_handle.product()
    
    event.getByLabel("muons", "", "reRECO", muons_rereco_handle)
    muons_rereco = muons_rereco_handle.product()
    
    event.getByLabel("generalTracks", "", "reRECO", tracks_rereco_handle)
    tracks_rereco = tracks_rereco_handle.product()
    
    for muon in muons:
        
        if muon.pt()<30:
            continue
        if not muon.isIsolationValid():
            continue
        
        for track in tracks:
                    
            tvec = TLorentzVector()
            tvec.SetPtEtaPhiM(track.pt(), track.eta(), track.phi(), 0.0)
            
            mvec = TLorentzVector()
            mvec.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), muon.mass())

            # muon matched to track:
            if tvec.DeltaR(mvec)<0.01:

                # a long track muon:
                if track.hitPattern().trackerLayersWithMeasurement() > 10 and \
                   track.dxy() < 0.02 and \
                   track.dz() < 0.5:
                   
                    #HitCategory { TRACK_HITS = 0, MISSING_INNER_HITS = 1, MISSING_OUTER_HITS = 2 }
                    #if  track.hitPattern().trackerLayersWithoutMeasurement(0) > 0 or track.hitPattern().trackerLayersWithoutMeasurement(1) > 0:
                    #    continue
                                        
                    # check if matched to rereco track:                   
                    minDR = 9999
                    matched_track_layers = -1
                    for track_rereco in tracks_rereco:
                        
                        #if track_rereco.hitPattern().trackerLayersWithMeasurement() != layers_remaining:
                        #    continue                        
                                      
                        trerecovec = TLorentzVector()
                        trerecovec.SetPtEtaPhiM(track_rereco.pt(), track_rereco.eta(), track_rereco.phi(), 0.0);
                        deltaR = tvec.DeltaR(trerecovec)
                        if deltaR < minDR:
                            minDR = deltaR
                            matched_track_layers = track_rereco.hitPattern().trackerLayersWithMeasurement()

                    h_tracks_reco.Fill(layers_remaining)
                    if minDR < 0.01:
                        h_layers2D.Fill(layers_remaining, matched_track_layers)
                        h_tracks_rereco.Fill(layers_remaining)
                    break
    
# make a canvas, draw, and save it
outfile = TFile("histograms_%s.root" % layers_remaining, "recreate")
h_tracks_reco.Write()
h_tracks_rereco.Write()
h_layers2D.Write()
outfile.Close()
