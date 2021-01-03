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
parser.add_option("--inputfile", dest = "inputfile", default = "")
(options, args) = parser.parse_args()

events = Events(options.inputfile)

layers_remaining = int(options.inputfile.split("_")[-1].replace(".root", ""))
print "remaining layers:", layers_remaining

if "Summer16" in options.inputfile.split(".root")[0]:
    period = "Summer16"
elif "Run2016" in options.inputfile.split(".root")[0]:
    period = "Run2016"
else:
    period = "unset"

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
h_tracks_reco = TH1F("h_tracks_reco", "", 21, 0, 21)
h_tracks_rereco = TH1F("h_tracks_rereco", "", 21, 0, 21)
h_tracks_preselection = TH1F("h_tracks_preselection", "", 21, 0, 21)
h_tracks_tagged = TH1F("h_tracks_tagged", "", 21, 0, 21)
h_tracks_preselectedandtagged = TH1F("h_tracks_preselectedandtagged", "", 21, 0, 21)
h_layers2D = TH2F("h_layers2D", ";targeted number of remaining layers; layers with meas. of matched track", 20, 0, 20, 20, 0, 20)
h_shortbdt2D = TH2F("h_shortbdt2D", ";BDT score; layers with meas. of matched track", 20, -1, 1, 20, 0, 20)
h_longbdt2D = TH2F("h_longbdt2D", ";BDT score; layers with meas. of matched track", 20, -1, 1, 20, 0, 20)
h_trkRelIso = TH1F("h_trkRelIso", "", 100, 0, 0.2)
h_muonPt = TH1F("h_muonPt", "", 20, 0, 500)

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

# loop over events
for i_event, event in enumerate(events):
        
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
        
        if muon.pt()<15: continue
        
        # PFCand isolation:
        summed_pt = 0
        for pfcand in pfcands:
            pfvec = TLorentzVector()
            pfvec.SetPtEtaPhiM(pfcand.pt(), pfcand.eta(), pfcand.phi(), pfcand.mass())
            mvec = TLorentzVector()
            mvec.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), muon.mass())
            if pfvec.DeltaR(mvec)>0.02 and pfvec.DeltaR(mvec)<0.3:
                summed_pt += pfcand.pt()
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
                if track.hitPattern().trackerLayersWithMeasurement() > 10 and \
                   track.dxy() < 0.2 and \
                   track.dz() < 0.5:

                    h_tracks_reco.Fill(layers_remaining)
                    h_muonPt.Fill(muon.pt())
                    
                    for track_rereco in tracks_rereco:
                        trerecovec = TLorentzVector()
                        trerecovec.SetPtEtaPhiM(track_rereco.pt(), track_rereco.eta(), track_rereco.phi(), 0.0);
                        deltaR = tvec.DeltaR(trerecovec)
                        if deltaR < 0.01:
                                                    
                            if track_rereco.pt()>15 and abs(track_rereco.eta())<2.4:

                                print "found rereco track"
                                h_layers2D.Fill(layers_remaining, track_rereco.hitPattern().trackerLayersWithMeasurement())
                                h_tracks_rereco.Fill(layers_remaining)
                                                
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
                                    
                                # fill var histograms:
                                h_trkRelIso.Fill(track_trkRelIso)
                                
                                is_preselected = False
                                is_tagged = False
                                
                                if track_is_pixel_track and \
                                   track_pt>15 and \
                                   track_trackQualityHighPurity==1 and \
                                   abs(track_eta)<2.4 and \
                                   track_ptErrOverPt2<10 and \
                                   abs(track_dzVtx)<0.1 and \
                                   track_trkRelIso<0.2 and \
                                   track_trackerLayersWithMeasurement>=2 and \
                                   track_nValidTrackerHits>=2 and \
                                   track_nMissingInnerHits==0 and \
                                   track_nValidPixelHits>=2 and \
                                   track_passPFCandVeto==1 and \
                                   track_passleptonveto==1 and \
                                   track_passpionveto==1 and \
                                   track_passjetveto==1 and \
                                   track_nMissingOuterHits>=0:
                                   is_preselected = True
                                   
                                if not track_is_pixel_track and \
                                   track_pt>30 and \
                                   track_trackQualityHighPurity==1 and \
                                   abs(track_eta)<2.4 and \
                                   track_ptErrOverPt2<10 and \
                                   abs(track_dzVtx)<0.1 and \
                                   track_trkRelIso<0.2 and \
                                   track_trackerLayersWithMeasurement>=2 and \
                                   track_nValidTrackerHits>=2 and \
                                   track_nMissingInnerHits==0 and \
                                   track_nValidPixelHits>=2 and \
                                   track_passPFCandVeto==1 and \
                                   track_passleptonveto==1 and \
                                   track_passpionveto==1 and \
                                   track_passjetveto==1 and \
                                   track_nMissingOuterHits>=2:
                                   is_preselected = True
                                
                                if track_is_pixel_track:
                                    var_dxyVtx_short[0] = track_dxyVtx
                                    var_dzVtx_short[0] = track_dzVtx
                                    var_trkRelIso_short[0] = track_trkRelIso
                                    var_nValidPixelHits_short[0] = track_nValidPixelHits
                                    var_ptErrOverPt2_short[0] = track_ptErrOverPt2
                                    var_chi2perNdof_short[0] = track_chi2perNdof
                                    track_mva = reader_short.EvaluateMVA("BDT")
                                    
                                    if track_p>0 and track_matchedCaloEnergy/track_p<0.2 and track_mva>0:
                                       is_tagged = True
                                       
                                    h_shortbdt2D.Fill(track_mva, track_rereco.hitPattern().trackerLayersWithMeasurement())
                                      
                                                                                                            
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
                                    
                                    if track_p>0 and track_matchedCaloEnergy/track_p<0.2 and track_mva>0.05:
                                       is_tagged = True
                                       
                                    h_longbdt2D.Fill(track_mva, track_rereco.hitPattern().trackerLayersWithMeasurement())

                                if not is_preselected:
                                    variables = ["track_is_pixel_track",
                                                 "track_dxyVtx",
                                                 "track_dzVtx",
                                                 "track_trkRelIso",
                                                 "track_nValidPixelHits",
                                                 "track_ptErrOverPt2",
                                                 "track_ptErrOverPt2",
                                                 "track_chi2perNdof",
                                                 "track_mva",
                                                 "track_pt",
                                                 "track_trackQualityHighPurity",
                                                 "track_eta",
                                                 "track_trackerLayersWithMeasurement",
                                                 "track_nValidTrackerHits",
                                                 "track_nMissingInnerHits",
                                                 "track_passPFCandVeto",
                                                 "track_nMissingOuterHits",
                                                 "track_matchedCaloEnergy",
                                                 "track_p"]
                                    
                                    print "Failed prelection"            
                                    for variable in variables:
                                        print "%s = %s " % (variable, eval(variable))
                                    print "============"
                                
                                if is_tagged:
                                    h_tracks_tagged.Fill(layers_remaining)
                                if is_preselected:
                                    h_tracks_preselection.Fill(layers_remaining)
                                if is_tagged and is_preselected:                 
                                    h_tracks_preselectedandtagged.Fill(layers_remaining)

                    break
    
# make a canvas, draw, and save it
outfile = TFile("histograms_%s_%s.root" % (period, layers_remaining), "recreate")
h_tracks_reco.Write()
h_tracks_rereco.Write()
h_tracks_tagged.Write()
h_tracks_preselection.Write()
h_tracks_preselectedandtagged.Write()
h_trkRelIso.Write()
h_layers2D.Write()
h_shortbdt2D.Write()
h_longbdt2D.Write()
h_muonPt.Write()
outfile.Close()
