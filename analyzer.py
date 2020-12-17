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

# handles for isotrk producer
isotrk_matchedCaloEnergy_handle = Handle("vector<double>")
isotrk_trackerLayersWithMeasurement_handle = Handle("vector<int>")
isotrk_chi2perNdof_handle = Handle("vector<double>")
isotrk_trackQualityHighPurity_handle = Handle("vector<bool>")
isotrk_ptError_handle = Handle("vector<double>")
isotrk_trkRelIso_handle = Handle("vector<double>")
isotrk_passPFCandVeto_handle = Handle("vector<bool>")
isotrk_deDxHarmonic2_handle = Handle("vector<double>")


# histograms
h_tracks_reco = TH1F("h_tracks_reco", "", 21, 0, 21)
h_tracks_rereco = TH1F("h_tracks_rereco", "", 21, 0, 21)
h_tracks_tagged = TH1F("h_tracks_tagged", "", 21, 0, 21)
h_layers2D = TH2F("h_layers2D", ";targeted number of remaining layers; layers with meas. of matched track", 20, 0, 20, 20, 0, 20)

# loop over events
for i_event, event in enumerate(events):
        
    # RECO collections:
    event.getByLabel("muons", "", "RECO", muons_handle)
    muons = muons_handle.product()
    event.getByLabel("rCluster%s" % layers_remaining, "", "HITREMOVER", tracks_handle)
    tracks = tracks_handle.product()
    
    # reRECO collections:
    event.getByLabel("muons", "", "reRECO", muons_rereco_handle)
    muons_rereco = muons_rereco_handle.product()
    event.getByLabel("generalTracks", "", "reRECO", tracks_rereco_handle)
    tracks_rereco = tracks_rereco_handle.product()

    # isotrk collections:
    event.getByLabel("isotrackproducer", "tracks@matchedCaloEnergy", "ISOTRACK", isotrk_matchedCaloEnergy_handle)
    isotrk_matchedCaloEnergy = isotrk_matchedCaloEnergy_handle.product()
    event.getByLabel("isotrackproducer", "tracks@trackerLayersWithMeasurement", "ISOTRACK", isotrk_trackerLayersWithMeasurement_handle)
    isotrk_trackerLayersWithMeasurement = isotrk_trackerLayersWithMeasurement_handle.product()
    event.getByLabel("isotrackproducer", "tracks@chi2perNdof", "ISOTRACK", isotrk_chi2perNdof_handle)
    isotrk_chi2perNdof = isotrk_chi2perNdof_handle.product()
    event.getByLabel("isotrackproducer", "tracks@trackQualityHighPurity", "ISOTRACK", isotrk_trackQualityHighPurity_handle)
    isotrk_trackQualityHighPurity = isotrk_trackQualityHighPurity_handle.product()
    event.getByLabel("isotrackproducer", "tracks@ptError", "ISOTRACK", isotrk_ptError_handle)
    isotrk_ptError = isotrk_ptError_handle.product()
    event.getByLabel("isotrackproducer", "tracks@trkRelIso", "ISOTRACK", isotrk_trkRelIso_handle)
    isotrk_trkRelIso = isotrk_trkRelIso_handle.product()
    event.getByLabel("isotrackproducer", "tracks@passPFCandVeto", "ISOTRACK", isotrk_passPFCandVeto_handle)
    isotrk_passPFCandVeto = isotrk_passPFCandVeto_handle.product()
    event.getByLabel("isotrackproducer", "tracks@deDxHarmonic2", "ISOTRACK", isotrk_deDxHarmonic2_handle)
    isotrk_deDxHarmonic2 = isotrk_deDxHarmonic2_handle.product()
    
    
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
                    print "matched track"
                   
                    #HitCategory { TRACK_HITS = 0, MISSING_INNER_HITS = 1, MISSING_OUTER_HITS = 2 }
                    #if  track.hitPattern().trackerLayersWithoutMeasurement(0) > 0 or track.hitPattern().trackerLayersWithoutMeasurement(1) > 0:
                    #    continue
                    
                    h_tracks_reco.Fill(layers_remaining)
                    
                    for track_rereco in tracks_rereco:
                        trerecovec = TLorentzVector()
                        trerecovec.SetPtEtaPhiM(track_rereco.pt(), track_rereco.eta(), track_rereco.phi(), 0.0);
                        deltaR = tvec.DeltaR(trerecovec)
                        if deltaR < 0.01:
                            
                            print "found rereco track"
                            h_layers2D.Fill(layers_remaining, track_rereco.hitPattern().trackerLayersWithMeasurement())
                            h_tracks_rereco.Fill(layers_remaining)
                        
                            # evaluate tag:
                            # without lepton/pion/jet vetos
                        
                            if track_rereco.pt()>15 and abs(track_rereco.eta())<2.4:

                                # matching to isotracks collection...
                                track_chi2perNdof = 1.0*track_rereco.chi2()/track_rereco.ndof()
                                isotrack_index = 0
                                for j, j_isotrk_chi2perNdof in enumerate(isotrk_chi2perNdof):
                                    if j_isotrk_chi2perNdof == track_chi2perNdof:
                                        isotrack_index = j

                                track_trackerLayersWithMeasurement = track_rereco.hitPattern().trackerLayersWithMeasurement() 
                                track_pixelLayersWithMeasurement = track_rereco.hitPattern().pixelLayersWithMeasurement() 
                                
                                if track_trackerLayersWithMeasurement == track_pixelLayersWithMeasurement:
                                    track_is_pixel_track = True
                                else:
                                    track_is_pixel_track = False
                                    
                                track_p = track_rereco.p()
                                track_pt = track_rereco.pt()
                                track_matchedCaloEnergy = isotrk_matchedCaloEnergy[isotrack_index]
                                track_trackQualityHighPurity = isotrk_trackQualityHighPurity[isotrack_index]
                                track_ptErrOverPt2 = track_pt / isotrk_ptError[isotrack_index]**2
                                track_dxyVtx = track_rereco.dxy()
                                track_dzVtx = track_rereco.dz()
                                track_trkRelIso = isotrk_trkRelIso[isotrack_index]
                                track_nValidTrackerHits = track_rereco.hitPattern().numberOfValidTrackerHits()
                                track_nValidPixelHits = track_rereco.hitPattern().numberOfValidPixelHits()
                                track_nMissingInnerHits = track_rereco.hitPattern().trackerLayersWithoutMeasurement(1)
                                track_nMissingOuterHits = track_rereco.hitPattern().trackerLayersWithoutMeasurement(2)
                                track_passPFCandVeto = isotrk_passPFCandVeto[isotrack_index]
                                track_deDxHarmonic2pixel = isotrk_deDxHarmonic2[isotrack_index]
                                                                                                                                
                                if track_matchedCaloEnergy < 10:
                                    h_tracks_tagged.Fill(layers_remaining)
                        
                    break
    
# make a canvas, draw, and save it
outfile = TFile("histograms_%s.root" % layers_remaining, "recreate")
h_tracks_reco.Write()
h_tracks_rereco.Write()
h_tracks_tagged.Write()
h_layers2D.Write()
outfile.Close()
