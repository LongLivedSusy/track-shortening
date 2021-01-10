#! /usr/bin/env python
from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
from array import array
import re, array

# inspect RECO and reRECO collections
# comments @ Viktor Kutzner

gROOT.SetBatch()        
gROOT.SetStyle('Plain') 

parser = OptionParser()
(options, args) = parser.parse_args()

events = Events(args)

layers_remaining = int(args[0].split("_")[-1].replace(".root", ""))
print "remaining layers:", layers_remaining

if "Summer16" in args[0].split(".root")[0]:
    period = "Summer16"
elif "Run2016" in args[0].split(".root")[0]:
    period = "Run2016"

# create handle outside of loop
muons_handle = Handle("std::vector<reco::Muon>")
pfcands_handle = Handle("std::vector<reco::PFCandidate>")
tracks_handle = Handle("std::vector<reco::Track>")
muons_rereco_handle = Handle("std::vector<reco::Muon>")
tracks_rereco_handle = Handle("std::vector<reco::Track>")

# handles for isotrk producer
isotrk_matchedCaloEnergy_handle = Handle("vector<double>")
isotrk_trackerLayersWithMeasurement_handle = Handle("vector<int>")
isotrk_chi2perNdof_handle = Handle("vector<double>")
isotrk_trackQualityHighPurity_handle = Handle("vector<bool>")
isotrk_ptError_handle = Handle("vector<double>")
isotrk_trkRelIso_handle = Handle("vector<double>")
isotrk_passPFCandVeto_handle = Handle("vector<bool>")
isotrk_deDxHarmonic2_handle = Handle("vector<double>")
isotrk_dxyVtx_handle = Handle("vector<double>")
isotrk_dzVtx_handle = Handle("vector<double>")

# histograms
histos = {}
histos["cutflow"]                            = TH1F("cutflow", "", 25, 0, 25)
histos["h_tracks_reco"]                      = TH1F("h_tracks_reco", "", 21, 0, 21)
histos["h_tracks_reco_rebinned"]             = TH1F("h_tracks_reco_rebinned", "", len([0, 3, 4, 21]) - 1, array.array('d', [0, 3, 4, 21]))
histos["h_tracks_rereco"]                    = TH1F("h_tracks_rereco", "", 21, 0, 21)
histos["h_tracks_rereco_rebinned"]           = TH1F("h_tracks_rereco_rebinned", "", len([0, 3, 4, 21]) - 1, array.array('d', [0, 3, 4, 21]))
histos["h_tracks_preselection"]              = TH1F("h_tracks_preselection", "", 21, 0, 21)
histos["h_tracks_tagged"]                    = TH1F("h_tracks_tagged", "", 21, 0, 21)
histos["h_tracks_tagged_rebinned"]           = TH1F("h_tracks_tagged_rebinned", "", len([0, 3, 4, 21]) - 1, array.array('d', [0, 3, 4, 21]))
histos["h_layers2D"]                         = TH2F("h_layers2D", ";targeted number of remaining layers; layers with meas. of matched track", 20, 0, 20, 20, 0, 20)
histos["h_ptratio2D"]                        = TH2F("h_ptratio2D", ";p_{T} of #mu-matched track (GeV); p_{T} of shortened track (GeV)", 20, 0, 300, 20, 0, 300)
histos["h_shortbdt2D"]                       = TH2F("h_shortbdt2D", ";BDT score; layers with meas. of matched track", 20, -1, 1, 20, 0, 20)
histos["h_longbdt2D"]                        = TH2F("h_longbdt2D", ";BDT score; layers with meas. of matched track", 20, -1, 1, 20, 0, 20)
histos["h_muonPt"]                           = TH1F("h_muonPt", "", 20, 0, 200)
histos["h_muonEta"]                          = TH1F("h_muonEta", "", 20, 0, 3.2)
histos["h_pfIso"]                            = TH1F("h_pfIso", "", 25, 0, 1)
histos["h_ptratio_layer3"]                   = TH1F("h_ptratio_layer3", "", 40, 0, 2)
histos["h_ptratio_layer4"]                   = TH1F("h_ptratio_layer4", "", 40, 0, 2)
histos["h_ptratio_layer5"]                   = TH1F("h_ptratio_layer5", "", 40, 0, 2)
histos["h_ptratio_layer6"]                   = TH1F("h_ptratio_layer6", "", 40, 0, 2)
histos["h_ptratio_layer7"]                   = TH1F("h_ptratio_layer7", "", 40, 0, 2)
histos["h_ptratio_layer8"]                   = TH1F("h_ptratio_layer8", "", 40, 0, 2)
histos["h_ptratio_layer9"]                   = TH1F("h_ptratio_layer9", "", 40, 0, 2)
histos["h_ptratio_layer10"]                  = TH1F("h_ptratio_layer10", "", 40, 0, 2)
histos["track_is_pixel_track"]               = TH1F("track_is_pixel_track", "", 2, 0, 2)
histos["track_dxyVtx"]                       = TH1F("track_dxyVtx", "", 20, 0, 0.1)
histos["track_dzVtx"]                        = TH1F("track_dzVtx", "", 20, 0, 0.1)
histos["track_trkRelIso"]                    = TH1F("track_trkRelIso", "", 20, 0, 0.2)
histos["track_nValidPixelHits"]              = TH1F("track_nValidPixelHits", "", 10, 0, 10)
histos["track_nValidTrackerHits"]            = TH1F("track_nValidTrackerHits", "", 20, 0, 20)
histos["track_trackerLayersWithMeasurement"] = TH1F("track_trackerLayersWithMeasurement", "", 20, 0, 20)
histos["track_ptErrOverPt2"]                 = TH1F("track_ptErrOverPt2", "", 20, 0, 0.01)
histos["track_chi2perNdof"]                  = TH1F("track_chi2perNdof", "", 20, 0, 2)
histos["track_mva"]                          = TH1F("track_mva", "", 20, -1, 1)
histos["track_pt"]                           = TH1F("track_pt", "", 20, 0, 200)
histos["track_trackQualityHighPurity"]       = TH1F("track_trackQualityHighPurity", "", 2, 0, 2)
histos["track_nMissingInnerHits"]            = TH1F("track_nMissingInnerHits", "", 5, 0, 5)
histos["track_passPFCandVeto"]               = TH1F("track_passPFCandVeto", "", 2, 0, 2)
histos["track_nMissingOuterHits"]            = TH1F("track_nMissingOuterHits", "", 10, 0, 10)
histos["track_matchedCaloEnergy"]            = TH1F("track_matchedCaloEnergy", "", 25, 0, 50)
histos["track_p"]                            = TH1F("track_p", "", 20, 0, 200)

# load BDTs
TMVA.Tools.Instance()
weights_short = "../analysis/disappearing-track-tag/2016-short-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml"
reader_short = TMVA.Reader( "!Color:!Silent" )
var_dxyVtx_short = array.array('f',[0]) ; reader_short.AddVariable("tracks_dxyVtx", var_dxyVtx_short)
var_dzVtx_short = array.array('f',[0]) ; reader_short.AddVariable("tracks_dzVtx", var_dzVtx_short)
var_trkRelIso_short = array.array('f',[0]) ; reader_short.AddVariable("tracks_trkRelIso", var_trkRelIso_short)
var_nValidPixelHits_short = array.array('f',[0]) ; reader_short.AddVariable("tracks_nValidPixelHits", var_nValidPixelHits_short)
var_ptErrOverPt2_short = array.array('f',[0]) ; reader_short.AddVariable("tracks_ptErrOverPt2", var_ptErrOverPt2_short)
var_chi2perNdof_short = array.array('f',[0]) ; reader_short.AddVariable("tracks_chi2perNdof", var_chi2perNdof_short)
reader_short.BookMVA("BDT", weights_short)

weights_long = "../analysis/disappearing-track-tag/2016-long-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml"
reader_long = TMVA.Reader( "!Color:!Silent" )
var_dxyVtx_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_dxyVtx", var_dxyVtx_long)
var_dzVtx_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_dzVtx", var_dzVtx_long)
var_trkRelIso_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_trkRelIso", var_trkRelIso_long)
var_nValidPixelHits_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_nValidPixelHits", var_nValidPixelHits_long)
var_nValidTrackerHits_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_nValidTrackerHits", var_nValidTrackerHits_long)
var_nMissingOuterHits_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_nMissingOuterHits", var_nMissingOuterHits_long)
var_ptErrOverPt2_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_ptErrOverPt2", var_ptErrOverPt2_long)
var_chi2perNdof_long = array.array('f',[0]) ; reader_long.AddVariable("tracks_chi2perNdof", var_chi2perNdof_long)
reader_long.BookMVA("BDT", weights_long)

cutflow_counter = -1

def cutflow_fill():
    if cutflow_counter>=0:
        for i in range(cutflow_counter + 1):
            histos["cutflow"].Fill(i)


# loop over events
for i_event, event in enumerate(events):
    
    if (i_event+1) % 10 == 0:
        print "event %s / %s (layers_remaining=%s)" % (i_event+1, events.size(), layers_remaining)
    
    # RECO collections:
    event.getByLabel("muons", "", "RECO", muons_handle)
    muons = muons_handle.product()
    event.getByLabel("rCluster%s" % layers_remaining, "", "HITREMOVER", tracks_handle)
    tracks = tracks_handle.product()
    event.getByLabel("particleFlow", "", "RECO", pfcands_handle)
    pfcands = pfcands_handle.product()
    
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
    event.getByLabel("isotrackproducer", "tracks@dxyVtx", "ISOTRACK", isotrk_dxyVtx_handle)
    isotrk_dxyVtx = isotrk_dxyVtx_handle.product()
    event.getByLabel("isotrackproducer", "tracks@dzVtx", "ISOTRACK", isotrk_dzVtx_handle)
    isotrk_dzVtx = isotrk_dzVtx_handle.product()
    
    for muon in muons:
                
        if muon.pt()<15:
            continue
        
        # PFCand isolation:
        summed_pt = 0
        for pfcand in pfcands:
            pfvec = TLorentzVector()
            pfvec.SetPtEtaPhiM(pfcand.pt(), pfcand.eta(), pfcand.phi(), pfcand.mass())
            mvec = TLorentzVector()
            mvec.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), muon.mass())
            if pfvec.DeltaR(mvec)>0.02 and pfvec.DeltaR(mvec)<0.3:
                summed_pt += pfcand.pt()
        histos["h_pfIso"].Fill(summed_pt/muon.pt())
        if summed_pt/muon.pt()>0.2:
            continue
                
        for track in tracks:
                                        
            tvec = TLorentzVector()
            tvec.SetPtEtaPhiM(track.pt(), track.eta(), track.phi(), 0.0)
            
            mvec = TLorentzVector()
            mvec.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), muon.mass())

            # muon matched to track:
            if tvec.DeltaR(mvec)<0.01:

                # a long track muon:
                if track.hitPattern().trackerLayersWithMeasurement() > 10:
                    if track.dxy() < 0.2:
                        if track.dz() < 0.5:

                            if not ((track.hitPattern().trackerLayersWithMeasurement() == 3 and track.pt()>15) or (track.hitPattern().trackerLayersWithMeasurement() > 3 and track.pt()>40)):
                                continue
                                
                            histos["h_tracks_reco"].Fill(layers_remaining)
                            histos["h_tracks_reco_rebinned"].Fill(layers_remaining)
                            histos["h_muonPt"].Fill(muon.pt())
                            histos["h_muonEta"].Fill(abs(muon.eta()))
                                                
                            for track_rereco in tracks_rereco:
                                trerecovec = TLorentzVector()
                                trerecovec.SetPtEtaPhiM(track_rereco.pt(), track_rereco.eta(), track_rereco.phi(), 0.0);
                                deltaR = tvec.DeltaR(trerecovec)
                                if deltaR < 0.01:
                                                                                                                                
                                    if track_rereco.pt()>15 and abs(track_rereco.eta())<2.4:
                                        
                                        #if track_rereco.hitPattern().trackerLayersWithMeasurement() > 10: continue
                                        
                                        #if track_is_pixel_track and track_pt>15:
                                        histos["h_layers2D"].Fill(layers_remaining, track_rereco.hitPattern().trackerLayersWithMeasurement())
                                        histos["h_ptratio2D"].Fill(track.pt(), track_rereco.pt())
                                        histos["h_tracks_rereco"].Fill(layers_remaining)
                                        histos["h_tracks_rereco_rebinned"].Fill(layers_remaining)
                                        
                                        for i_layer in range(3,11):
                                            if layers_remaining == i_layer:
                                                histos["h_ptratio_layer%s" % i_layer].Fill(1.0 * track.pt() / track_rereco.pt())
                                        
                                        cutflow_counter = 0
                                                                                                
                                        # matching to isotracks collection...
                                        if track_rereco.ndof()>0:
                                            track_chi2perNdof = 1.0*track_rereco.chi2()/track_rereco.ndof()
                                        else:
                                            track_chi2perNdof = 0
                                        
                                        isotrack_index = 0
                                        for j, j_isotrk_chi2perNdof in enumerate(isotrk_chi2perNdof):
                                            if j_isotrk_chi2perNdof == track_chi2perNdof:
                                                isotrack_index = j
                            
                                        # get all necessary tag variables:
                                        track_trackerLayersWithMeasurement = track_rereco.hitPattern().trackerLayersWithMeasurement() 
                                        track_pixelLayersWithMeasurement = track_rereco.hitPattern().pixelLayersWithMeasurement() 
                                        
                                        if track_trackerLayersWithMeasurement == track_pixelLayersWithMeasurement:
                                            track_is_pixel_track = True
                                        else:
                                            track_is_pixel_track = False
                                            
                                        track_p = track_rereco.p()
                                        track_eta = track_rereco.eta()
                                        track_pt = track_rereco.pt()
                                        track_matchedCaloEnergy = isotrk_matchedCaloEnergy[isotrack_index]
                                        track_trackQualityHighPurity = bool(isotrk_trackQualityHighPurity[isotrack_index])
                                        if track_pt>0:
                                            track_ptErrOverPt2 = isotrk_ptError[isotrack_index] / track_pt**2
                                        else:
                                            track_ptErrOverPt2 = 0
                                        track_dxyVtx = isotrk_dxyVtx[isotrack_index]
                                        track_dzVtx = isotrk_dzVtx[isotrack_index]
                                        track_trkRelIso = isotrk_trkRelIso[isotrack_index]
                                        track_nValidTrackerHits = track_rereco.hitPattern().numberOfValidTrackerHits()
                                        track_nValidPixelHits = track_rereco.hitPattern().numberOfValidPixelHits()
                                        track_nMissingInnerHits = track_rereco.hitPattern().trackerLayersWithoutMeasurement(1)
                                        track_nMissingOuterHits = track_rereco.hitPattern().trackerLayersWithoutMeasurement(2)
                                        track_passPFCandVeto = bool(isotrk_passPFCandVeto[isotrack_index])
                                        track_deDxHarmonic2pixel = isotrk_deDxHarmonic2[isotrack_index]
                                                                                
                                        # ignore for now
                                        track_passleptonveto = 1
                                        track_passpionveto = 1
                                        track_passjetveto = 1
                                        
                                        # reset this as the muon will always cause the veto to fail:
                                        track_passPFCandVeto = 1
                                        
                                        # redo relIso, but without the muon:
                                        conePtSum_rel = 0
                                        for othertrack in tracks_rereco:
                                            if othertrack.pt()>15 and abs(othertrack.eta())<2.4: #and abs(othertrack.dxy())<0.03 and abs(othertrack.dz())<0.05
                                                othertrackvec = TLorentzVector()
                                                othertrackvec.SetPtEtaPhiM(othertrack.pt(), othertrack.eta(), othertrack.phi(), 0.0)
                                                deltaR = othertrackvec.DeltaR(trerecovec)
                                                if deltaR<0.00001:
                                                    continue
                                                if deltaR<0.3:
                                                    conePtSum_rel += othertrack.pt()
                                        if track_rereco.pt()>0:
                                            track_trkRelIso = conePtSum_rel / track_rereco.pt()
                                        else:
                                            track_trkRelIso = 0
                                                                            
                                        is_tagged = False
                                        is_preselected = False
                                        
                                        if track_trackQualityHighPurity==1:
                                            cutflow_counter += 1
                                            if abs(track_eta)<2.4:
                                                cutflow_counter += 1
                                                if track_ptErrOverPt2<10:
                                                    cutflow_counter += 1
                                                    if abs(track_dzVtx)<0.1:
                                                        cutflow_counter += 1
                                                        if track_trkRelIso<0.2:
                                                            cutflow_counter += 1
                                                            if track_trackerLayersWithMeasurement>=2:
                                                                cutflow_counter += 1
                                                                if track_nValidTrackerHits>=2:
                                                                    cutflow_counter += 1
                                                                    if track_nMissingInnerHits==0:
                                                                        cutflow_counter += 1
                                                                        if track_nValidPixelHits>=2:
                                                                            cutflow_counter += 1
                                                                            if track_passPFCandVeto==1:
                                                                                cutflow_counter += 1
                                                                                if track_is_pixel_track:
                                                                                     if track_pt>15:
                                                                                         cutflow_counter += 1
                                                                                         if track_nMissingOuterHits>=0:
                                                                                             cutflow_counter += 1
                                                                                             is_preselected = True
                                                                                else:
                                                                                     if track_pt>40:
                                                                                         cutflow_counter += 1
                                                                                         if track_nMissingOuterHits>=2:
                                                                                             cutflow_counter += 1
                                                                                             is_preselected = True
                                                                                     
                                        if track_is_pixel_track:
                                            var_dxyVtx_short[0] = track_dxyVtx
                                            var_dzVtx_short[0] = track_dzVtx
                                            var_trkRelIso_short[0] = track_trkRelIso
                                            var_nValidPixelHits_short[0] = track_nValidPixelHits
                                            var_ptErrOverPt2_short[0] = track_ptErrOverPt2
                                            var_chi2perNdof_short[0] = track_chi2perNdof
                                            track_mva = reader_short.EvaluateMVA("BDT")
                                            
                                            if is_preselected and track_mva>0:
                                                cutflow_counter += 1
                                                if track_matchedCaloEnergy/track_p<0.2:
                                                    cutflow_counter += 1
                                                    is_tagged = True
                                                    histos["h_shortbdt2D"].Fill(track_mva, track_rereco.hitPattern().trackerLayersWithMeasurement())
                                                                                                                                                          
                                        else:
                                            var_dxyVtx_long[0] = track_dxyVtx
                                            var_dzVtx_long[0] = track_dzVtx
                                            var_trkRelIso_long[0] = track_trkRelIso
                                            var_nValidPixelHits_long[0] = track_nValidPixelHits
                                            var_nValidTrackerHits_long[0] = track_nValidTrackerHits
                                            var_nMissingOuterHits_long[0] = track_nMissingOuterHits
                                            var_ptErrOverPt2_long[0] = track_ptErrOverPt2
                                            var_chi2perNdof_long[0] = track_chi2perNdof
                                            track_mva = reader_long.EvaluateMVA("BDT")  
                                            
                                            if is_preselected and track_mva>0.05:
                                                cutflow_counter += 1
                                                if track_matchedCaloEnergy/track_p<0.2:
                                                    cutflow_counter += 1
                                                    is_tagged = True
                                                    histos["h_longbdt2D"].Fill(track_mva, track_rereco.hitPattern().trackerLayersWithMeasurement())
                            
                                        cutflow_fill()            
                                        
                                        # fill var histograms:
                                        for label in histos:
                                            if "track_" in label:
                                                value = eval(label)
                                                histos[label].Fill(value)
                            
                                        if is_tagged:
                                            histos["h_tracks_tagged"].Fill(layers_remaining)
                                            histos["h_tracks_tagged_rebinned"].Fill(layers_remaining)
                                        if is_preselected:
                                            histos["h_tracks_preselection"].Fill(layers_remaining)
                                    
                                        break
                
                        
# make a canvas, draw, and save it
outfile = TFile("histograms_%s_%s.root" % (period, layers_remaining), "recreate")
for label in histos:
    histos[label].Write()
outfile.Close()
