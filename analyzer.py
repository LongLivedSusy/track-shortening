#! /usr/bin/env python
from ROOT import *
import sys, os
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
import array as pyarray

# inspect RECO and reRECO collections
# comments @ Viktor Kutzner

gROOT.SetBatch() 
gROOT.SetStyle('Plain')

parser = OptionParser()
parser.add_option("--low_pt", dest = "low_pt_threshold", default = 15)
parser.add_option("--high_pt", dest = "high_pt_threshold", default = 99999)
parser.add_option("--low_eta", dest = "low_eta_threshold", default = 0)
parser.add_option("--high_eta", dest = "high_eta_threshold", default = 2.2)
parser.add_option("--bdt", dest = "bdt", default = "may21-equSgXsec3")
parser.add_option("--iso", dest = "iso", default = 0)
parser.add_option("--suffix", dest = "suffix", default = "")
parser.add_option("--outputfolder", dest = "outputfolder", default = "histograms")
parser.add_option("--nev", dest = "nev", default = -1)
parser.add_option("--override_category_pt", dest = "override_category_pt", action="store_true")
parser.add_option("--onlyp1bdt", dest = "onlyp1bdt", action="store_true")

(options_, args) = parser.parse_args()

overwrite = True

layers_remaining = int(args[0].split("_")[-1].replace(".root", ""))
print "remaining layers:", layers_remaining

period = ""
periods = [
            "RunUL2017C",
            "Fall17UL",
            "Summer16",
            "Fall17",
            "Autumn18",
            "Run2016B",
            "Run2016C",
            "Run2016D",
            "Run2016E",
            "Run2016F",
            "Run2016G",
            "Run2016H",
            "Run2017B",
            "Run2017C",
            "Run2017D",
            "Run2017E",
            "Run2017F",
            "Run2018A",
            "Run2018B",
            "Run2018C",
            "Run2018D",
          ]

for i_period in periods:
    if i_period in args[0].split(".root")[0]:
        period = i_period
        print "period", period
        break
if period == "":
    quit("No run period")

# test for invalid files:
sane_files = []
for arg in args:
    if "mimes" in arg: continue
    test = TFile(arg)
    if not (test.IsZombie() or test.TestBit(TFile.kRecovered)):
        sane_files.append(arg)
    else:
        print "deleting file: %s" % arg
        os.system("rm %s" % arg)
    test.Close()

print "sane_files", sane_files

events = Events(sane_files)

# create handle outside of loop
muons_handle = Handle("std::vector<reco::Muon>")
pfcands_handle = Handle("std::vector<reco::PFCandidate>")
tracks_handle = Handle("std::vector<reco::Track>")
muons_rereco_handle = Handle("std::vector<reco::Muon>")
tracks_rereco_handle = Handle("std::vector<reco::Track>")

# handles for isotrk producer
isotrk_matchedCaloEnergy_handle = Handle("std::vector<double>")
isotrk_trackerLayersWithMeasurement_handle = Handle("std::vector<int>")
isotrk_chi2perNdof_handle = Handle("std::vector<double>")
isotrk_trackQualityHighPurity_handle = Handle("std::vector<bool>")
isotrk_ptError_handle = Handle("std::vector<double>")
isotrk_trkRelIso_handle = Handle("std::vector<double>")
isotrk_passPFCandVeto_handle = Handle("std::vector<bool>")
isotrk_deDxHarmonic2_handle = Handle("std::vector<double>")
isotrk_dxyVtx_handle = Handle("std::vector<double>")
isotrk_dzVtx_handle = Handle("std::vector<double>")

#TH1F("h_tracks_reco_rebinned", "", len([0, 21]) - 1, pyarray.array('d', [0, 21]))

# histograms
histos = {}
histos["cutflow"]                            = TH1F("cutflow", "", 25, 0, 25)
histos["h_tracks_reco"]                      = TH1F("h_tracks_reco", "", 21, 0, 21)
histos["h_tracks_reco_rebinned"]             = TH1F("h_tracks_reco_rebinned", "", 1, 0, 21)
histos["h_tracks_rereco"]                    = TH1F("h_tracks_rereco", "", 21, 0, 21)
histos["h_tracks_rereco_rebinned"]           = TH1F("h_tracks_rereco_rebinned", "", 1, 0, 21)
histos["h_tracks_rereco_exact"]              = TH1F("h_tracks_rereco_exact", "", 21, 0, 21)
histos["h_tracks_preselection"]              = TH1F("h_tracks_preselection", "", 21, 0, 21)
histos["h_tracks_tagged"]                    = TH1F("h_tracks_tagged", "", 21, 0, 21)
histos["h_tracks_tagged_rebinned"]           = TH1F("h_tracks_tagged_rebinned", "", 1, 0, 21)
histos["h_tracks_tagged_exact"]              = TH1F("h_tracks_tagged_exact", "", 21, 0, 21)
histos["h_tracks_algo"]                      = TH1F("h_tracks_algo", "", 50, 0, 50)
histos["h_layers2D"]                         = TH2F("h_layers2D", ";targeted number of remaining layers; layers with meas. of matched track;Tracks", 20, 0, 20, 20, 0, 20)
histos["h_ptratio2D"]                        = TH2F("h_ptratio2D", ";p_{T} of #mu-matched track (GeV); p_{T} of shortened track (GeV);Tracks", 20, 0, 300, 20, 0, 300)
histos["h_shortbdt2D"]                       = TH2F("h_shortbdt2D", ";BDT score; layers with meas. of matched track;Tracks", 20, -1, 1, 20, 0, 20)
histos["h_longbdt2D"]                        = TH2F("h_longbdt2D", ";BDT score; layers with meas. of matched track;Tracks", 20, -1, 1, 20, 0, 20)
histos["h_chi2ndof2D"]                       = TH2F("h_chi2ndof2D", ";layers with meas. of matched track;shortened track p_{T} (GeV); <#chi^{2}/ndof>", 20, 0, 20, 20, 0, 300)
histos["h_muonPtCand"]                       = TH1F("h_muonPtCand", "", 20, 0, 200)
histos["h_muonEtaCand"]                      = TH1F("h_muonEtaCand", "", 20, 0, 3.2)
histos["h_muonPt"]                           = TH1F("h_muonPt", "", 20, 0, 200)
histos["h_muonEta"]                          = TH1F("h_muonEta", "", 20, 0, 3.2)
histos["h_pfIso"]                            = TH1F("h_pfIso", "", 25, 0, 1)
histos["h_ptratio"]                          = TH1F("h_ptratio", "", 40, 0, 2)
histos["h_ptratioOrig"]                      = TH1F("h_ptratioOrig", "", 40, 0, 2)
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
histos["h_mismatch"]                         = TH1F("h_mismatch", "", 21, 0, 21)

# add layer-dependent track variable histograms:
for label in histos.keys():
    if "h_tracks_" in label or "cutflow" in label:
        histos[label + "_short"] = histos[label].Clone()
        histos[label + "_short"].SetName(label + "_short")
        histos[label + "_long"] = histos[label].Clone()
        histos[label + "_long"].SetName(label + "_long")

for label in histos.keys():
    if "track_" in label or "h_ptratio" in label or "cutflow" in label:
        for i in range(3,9):
            histos[label + "_layer%s" % i] = histos[label].Clone()
            histos[label + "_layer%s" % i].SetName(label + "_layer%s" % i)

if options_.onlyp1bdt or ("Run2016" in period or "Summer16" in period):
    print "Using Phase-0 BDTs"
    weights_short = "../analysis/disappearing-track-tag/2016-short-tracks-%s/dataset/weights/TMVAClassification_BDT.weights.xml" % options_.bdt
    weights_long = "../analysis/disappearing-track-tag/2016-long-tracks-%s/dataset/weights/TMVAClassification_BDT.weights.xml" % options_.bdt
    phase = 0
else:
    print "Using Phase-1 BDTs"
    weights_short = "../analysis/disappearing-track-tag/2017-short-tracks-%s/dataset/weights/TMVAClassification_BDT.weights.xml" % options_.bdt
    weights_long = "../analysis/disappearing-track-tag/2017-long-tracks-%s/dataset/weights/TMVAClassification_BDT.weights.xml" % options_.bdt
    phase = 1
    
# load BDTs
TMVA.Tools.Instance()
reader_short = TMVA.Reader( "!Color:!Silent" )
var_dxyVtx_short = pyarray.array('f',[0]) ; reader_short.AddVariable("tracks_dxyVtx", var_dxyVtx_short)
var_dzVtx_short = pyarray.array('f',[0]) ; reader_short.AddVariable("tracks_dzVtx", var_dzVtx_short)
var_trkRelIso_short = pyarray.array('f',[0]) ; reader_short.AddVariable("tracks_trkRelIso", var_trkRelIso_short)
var_nValidPixelHits_short_ = pyarray.array('f',[0]) ; reader_short.AddVariable("tracks_nValidPixelHits", var_nValidPixelHits_short_)
var_ptErrOverPt2_short = pyarray.array('f',[0]) ; reader_short.AddVariable("tracks_ptErrOverPt2", var_ptErrOverPt2_short)
var_chi2perNdof_short = pyarray.array('f',[0]) ; reader_short.AddVariable("tracks_chi2perNdof", var_chi2perNdof_short)
reader_short.BookMVA("BDT", weights_short)

reader_long = TMVA.Reader( "!Color:!Silent" )
var_dxyVtx_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_dxyVtx", var_dxyVtx_long)
var_dzVtx_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_dzVtx", var_dzVtx_long)
var_trkRelIso_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_trkRelIso", var_trkRelIso_long)
var_nValidPixelHits_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_nValidPixelHits", var_nValidPixelHits_long)
var_nValidTrackerHits_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_nValidTrackerHits", var_nValidTrackerHits_long)
var_nMissingOuterHits_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_nMissingOuterHits", var_nMissingOuterHits_long)
var_ptErrOverPt2_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_ptErrOverPt2", var_ptErrOverPt2_long)
var_chi2perNdof_long = pyarray.array('f',[0]) ; reader_long.AddVariable("tracks_chi2perNdof", var_chi2perNdof_long)
reader_long.BookMVA("BDT", weights_long)

    
cutflow_counter = -1

def cutflow_fill(layers_remaining, pixel_track):
    
    if pixel_track:
        category = "_short"
    else:
        category = "_long"
    
    if cutflow_counter>=0:
        for i in range(cutflow_counter + 1):
            histos["cutflow" + category].Fill(i)
            histos["cutflow"].Fill(i)
    
            if layers_remaining in range(3,9):
                histos["cutflow_layer%s" % (layers_remaining)].Fill(i)
                histos["cutflow%s_layer%s" % (category, layers_remaining)].Fill(i)


# loop over events
for i_event, event in enumerate(events):
        
    if (i_event+1) % 100 == 0:
        print "%s, event %s / %s (layers_remaining=%s)" % (period, i_event+1, events.size(), layers_remaining)
        if int(options_.nev)>0 and i_event>int(options_.nev): break
    
    # FIXME
    if period == "SummerOld16" or period == "Run2016PromptH":
        isotrack_producerlabel = "ISOTRACK"
    else:
        isotrack_producerlabel = "reRECO"
            
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
    event.getByLabel("isotrackproducer", "tracks@matchedCaloEnergy", isotrack_producerlabel, isotrk_matchedCaloEnergy_handle)
    #event.getByLabel("tracks@matchedCaloEnergy", isotrk_matchedCaloEnergy_handle)
    isotrk_matchedCaloEnergy = isotrk_matchedCaloEnergy_handle.product()
    event.getByLabel("isotrackproducer", "tracks@trackerLayersWithMeasurement", isotrack_producerlabel, isotrk_trackerLayersWithMeasurement_handle)
    isotrk_trackerLayersWithMeasurement = isotrk_trackerLayersWithMeasurement_handle.product()
    event.getByLabel("isotrackproducer", "tracks@chi2perNdof", isotrack_producerlabel, isotrk_chi2perNdof_handle)
    isotrk_chi2perNdof = isotrk_chi2perNdof_handle.product()
    event.getByLabel("isotrackproducer", "tracks@trackQualityHighPurity", isotrack_producerlabel, isotrk_trackQualityHighPurity_handle)
    isotrk_trackQualityHighPurity = isotrk_trackQualityHighPurity_handle.product()
    event.getByLabel("isotrackproducer", "tracks@ptError", isotrack_producerlabel, isotrk_ptError_handle)
    isotrk_ptError = isotrk_ptError_handle.product()
    event.getByLabel("isotrackproducer", "tracks@trkRelIso", isotrack_producerlabel, isotrk_trkRelIso_handle)
    isotrk_trkRelIso = isotrk_trkRelIso_handle.product()
    event.getByLabel("isotrackproducer", "tracks@passPFCandVeto", isotrack_producerlabel, isotrk_passPFCandVeto_handle)
    isotrk_passPFCandVeto = isotrk_passPFCandVeto_handle.product()
    event.getByLabel("isotrackproducer", "tracks@deDxHarmonic2", isotrack_producerlabel, isotrk_deDxHarmonic2_handle)
    isotrk_deDxHarmonic2 = isotrk_deDxHarmonic2_handle.product()
    event.getByLabel("isotrackproducer", "tracks@dxyVtx", isotrack_producerlabel, isotrk_dxyVtx_handle)
    isotrk_dxyVtx = isotrk_dxyVtx_handle.product()
    event.getByLabel("isotrackproducer", "tracks@dzVtx", isotrack_producerlabel, isotrk_dzVtx_handle)
    isotrk_dzVtx = isotrk_dzVtx_handle.product()
    
    for muon in muons:
                        
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
        
        if int(options_.iso) == 0:
            # default, isolated:
            if not (summed_pt/muon.pt()<0.2):
                continue
        elif int(options_.iso) == 1:
            # default, non-isolated:
            if not (summed_pt/muon.pt()>0.2):
                continue
        elif int(options_.iso) == 2:
            # default, non-isolated:
            if not (summed_pt/muon.pt()>0.4 and summed_pt/muon.pt()<0.6):
                continue
        elif int(options_.iso) == 3:
            # default, non-isolated:
            if not (summed_pt/muon.pt()>0.2 and summed_pt/muon.pt()<0.4):
                continue
        elif int(options_.iso) == 4:
            # default, non-isolated:
            if not (summed_pt/muon.pt()<0.1):
                continue
        elif int(options_.iso) == 5:
            # default, non-isolated:
            if not (summed_pt/muon.pt()>0.1 and summed_pt/muon.pt()<0.2):
                continue
        
        histos["h_muonPtCand"].Fill(muon.pt())
        histos["h_muonEtaCand"].Fill(abs(muon.eta()))
        
        # select best muon track:
        try:
            track = muon.bestTrack()
        except:
            print "No associated best track for muon"
            continue            

        if not (abs(track.eta())<2.2 and track.pt()>40):
            break
        
        tvec = TLorentzVector()
        tvec.SetPtEtaPhiM(track.pt(), track.eta(), track.phi(), 0.0)

        # get best muon track and check DeltaR:
        mvec = TLorentzVector()
        mvec.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), muon.mass())
        bestTrackDR = mvec.DeltaR(tvec)            
        best_track_is_in_tracks_collection = False
        for i_track in tracks:            
            itvec = TLorentzVector()
            itvec.SetPtEtaPhiM(i_track.pt(), i_track.eta(), i_track.phi(), 0.0)
            if bestTrackDR == mvec.DeltaR(itvec):
                best_track_is_in_tracks_collection = True
        if not best_track_is_in_tracks_collection:
            continue
                                                
        # a long track muon:
        if track.hitPattern().trackerLayersWithMeasurement() > 10 and track.dxy() < 0.2 and track.dz() < 0.1:
                    
            histos["h_tracks_reco"].Fill(layers_remaining)
            histos["h_tracks_reco_rebinned"].Fill(layers_remaining)
            
            # possible short/long tracks after shortening:
            if track.hitPattern().pixelLayersWithMeasurement() == layers_remaining: 
                histos["h_tracks_reco_short"].Fill(layers_remaining)
                histos["h_tracks_reco_rebinned_short"].Fill(layers_remaining)
            elif layers_remaining > track.hitPattern().pixelLayersWithMeasurement():
                histos["h_tracks_reco_long"].Fill(layers_remaining)
                histos["h_tracks_reco_rebinned_long"].Fill(layers_remaining)
            
            histos["h_muonPt"].Fill(muon.pt())
            histos["h_muonEta"].Fill(abs(muon.eta()))
            
            for track_rereco in tracks_rereco:
                trerecovec = TLorentzVector()
                trerecovec.SetPtEtaPhiM(track_rereco.pt(), track_rereco.eta(), track_rereco.phi(), 0.0)
                deltaR = tvec.DeltaR(trerecovec)
                if deltaR < 0.01 \
                   and (options_.override_category_pt or ((track_rereco.hitPattern().trackerLayersWithMeasurement() <= track_rereco.hitPattern().pixelLayersWithMeasurement() \
                        and track_rereco.pt()>25) \
                        or (track_rereco.hitPattern().trackerLayersWithMeasurement() > track_rereco.hitPattern().pixelLayersWithMeasurement()\
                        and track_rereco.pt()>40))) \
                   and track_rereco.pt()>int(options_.low_pt_threshold) and track_rereco.pt()<=int(options_.high_pt_threshold) \
                   and abs(track_rereco.eta())>float(options_.low_eta_threshold) \
                   and abs(track_rereco.eta())<=float(options_.high_eta_threshold):
                    
                    # get all necessary tag variables:
                    track_trackerLayersWithMeasurement = track_rereco.hitPattern().trackerLayersWithMeasurement() 
                    track_pixelLayersWithMeasurement = track_rereco.hitPattern().pixelLayersWithMeasurement() 
                    if track_trackerLayersWithMeasurement == track_pixelLayersWithMeasurement:
                        track_is_pixel_track = True
                    else:
                        track_is_pixel_track = False
                    
                    # fill track mismatch histogram:
                    if track_trackerLayersWithMeasurement == layers_remaining:
                        histos["h_tracks_rereco_exact"].Fill(layers_remaining)
                    else:
                        histos["h_mismatch"].Fill(layers_remaining)
                    
                    histos["h_layers2D"].Fill(layers_remaining, track_trackerLayersWithMeasurement)
                    histos["h_ptratio2D"].Fill(track.pt(), track_rereco.pt())
                    histos["h_tracks_rereco"].Fill(layers_remaining)
                    histos["h_tracks_rereco_rebinned"].Fill(layers_remaining)
                    histos["h_tracks_algo"].Fill(track_rereco.algo())
                    
                    if track_is_pixel_track:
                        histos["h_tracks_rereco_short"].Fill(layers_remaining)
                        histos["h_tracks_rereco_rebinned_short"].Fill(layers_remaining)
                        if track_trackerLayersWithMeasurement == layers_remaining:
                            histos["h_tracks_rereco_exact_short"].Fill(layers_remaining)
                    else:
                        histos["h_tracks_rereco_long"].Fill(layers_remaining)
                        histos["h_tracks_rereco_rebinned_long"].Fill(layers_remaining)
                        if track_trackerLayersWithMeasurement == layers_remaining:
                            histos["h_tracks_rereco_exact_long"].Fill(layers_remaining)
                                                            
                    for i_layer in range(3,9):
                        if layers_remaining == i_layer:
                            histos["h_ptratio_layer%s" % i_layer].Fill(1.0 * track_rereco.pt() / track.pt())
                    
                    cutflow_counter = 0
                                                                            
                    if track_rereco.ndof()>0:
                        track_chi2perNdof = 1.0*track_rereco.chi2()/track_rereco.ndof()
                    else:
                        track_chi2perNdof = 0
                    
                    histos["h_chi2ndof2D"].Fill(layers_remaining, track_rereco.pt(), track_chi2perNdof)
                    
                    # matching to isotracks collection...
                    isotrack_index = -1
                    for j, j_isotrk_chi2perNdof in enumerate(isotrk_chi2perNdof):
                        if j_isotrk_chi2perNdof == track_chi2perNdof:
                            isotrack_index = j
            
                    if isotrack_index == -1:
                        print "isotrack matching failed"
                        break

                    track_p = track_rereco.p()
                    track_eta = track_rereco.eta()
                    track_pt = track_rereco.pt()
                    track_matchedCaloEnergy = isotrk_matchedCaloEnergy[isotrack_index]
                    track_trackQualityHighPurity = bool(isotrk_trackQualityHighPurity[isotrack_index])
                    if track_pt>0:
                        track_ptErrOverPt2 = isotrk_ptError[isotrack_index] / track_pt**2
                    else:
                        track_ptErrOverPt2 = 0
    
                    track_dzVtx = isotrk_dzVtx[isotrack_index]
                    track_dxyVtx = isotrk_dxyVtx[isotrack_index]
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
                        if othertrack.pt()>15 and abs(othertrack.eta())<2.2:
                            othertrackvec = TLorentzVector()
                            othertrackvec.SetPtEtaPhiM(othertrack.pt(), othertrack.eta(), othertrack.phi(), 0.0)
                            deltaR = othertrackvec.DeltaR(trerecovec)
                            if deltaR<0.01:
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
                        if abs(track_eta)<2.0:
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
                                                                 if track_pt>25:
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
                        var_nValidPixelHits_short_[0] = track_nValidPixelHits
                        var_ptErrOverPt2_short[0] = track_ptErrOverPt2
                        var_chi2perNdof_short[0] = track_chi2perNdof
                        track_mva = reader_short.EvaluateMVA("BDT")
                        
                        if is_preselected and ((phase==0 and track_mva>0.1) or (phase==1 and track_mva>0.1)):
                            cutflow_counter += 1
                            if (track_matchedCaloEnergy<15 or track_matchedCaloEnergy/track_p<0.15):
                                cutflow_counter += 1
                                is_tagged = True
                                histos["h_shortbdt2D"].Fill(track_mva, track_trackerLayersWithMeasurement)
                                                                                                                                      
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
                        
                        if is_preselected and ((phase==0 and track_mva>0.12) or (phase==1 and track_mva>0.15)):
                            cutflow_counter += 1
                            if (track_matchedCaloEnergy<15 or track_matchedCaloEnergy/track_p<0.15):
                                cutflow_counter += 1
                                is_tagged = True
                                histos["h_longbdt2D"].Fill(track_mva, track_trackerLayersWithMeasurement)
            
                    cutflow_fill(layers_remaining, track_is_pixel_track)      
                    
                    # fill var histograms:
                    for label in histos:
                        if "track_" in label and "_layer" not in label:
                            value = eval(label)
                            histos[label].Fill(value)
                            
                            # fill layer-dependent histograms:
                            if layers_remaining in range(3,9):
                                histos[label + "_layer%s" % layers_remaining].Fill(value)
                            
                    if is_tagged:
                        histos["h_tracks_tagged"].Fill(layers_remaining)
                        histos["h_tracks_tagged_rebinned"].Fill(layers_remaining)

                        if track_trackerLayersWithMeasurement == layers_remaining:
                            histos["h_tracks_tagged_exact"].Fill(layers_remaining)

                        if track_is_pixel_track:
                            histos["h_tracks_tagged_short"].Fill(layers_remaining)
                            histos["h_tracks_tagged_rebinned_short"].Fill(layers_remaining)
                            if track_trackerLayersWithMeasurement == layers_remaining:
                                histos["h_tracks_tagged_exact_short"].Fill(layers_remaining)
                        else:
                            histos["h_tracks_tagged_long"].Fill(layers_remaining)
                            histos["h_tracks_tagged_rebinned_long"].Fill(layers_remaining)
                            if track_trackerLayersWithMeasurement == layers_remaining:
                                histos["h_tracks_tagged_exact_long"].Fill(layers_remaining)
                        
                    if is_preselected:
                        histos["h_tracks_preselection"].Fill(layers_remaining)
                    
                    #if layers_remaining == 2:
                    #    print "layers_remaining", layers_remaining
                    #    print "track_trackerLayersWithMeasurement", track_trackerLayersWithMeasurement
                    #    print "track_pixelLayersWithMeasurement", track_pixelLayersWithMeasurement
                    #    print "track_eta", track_eta
                    #    print "track_pt", track_pt
                    #    print "track_matchedCaloEnergy", track_matchedCaloEnergy
                    #    print "track_trackQualityHighPurity", track_trackQualityHighPurity
                    #    print "track_dxyVtx", track_dxyVtx
                    #    print "track_dzVtx", track_dzVtx
                    #    print "track_trkRelIso", track_trkRelIso
                    #    print "track_nValidTrackerHits", track_nValidTrackerHits
                    #    print "track_nValidPixelHits", track_nValidPixelHits
                    #    print "track_nMissingInnerHits", track_nMissingInnerHits
                    #    print "track_nMissingOuterHits", track_nMissingOuterHits
                    
                    # exit shortened track loop
                    break
            
            # exit muon loop to only process a single muon per event:
            break
                                                        
                        
# make a canvas, draw, and save it
os.system("mkdir -p %s" % options_.outputfolder)
outfilename = "%s/histograms%s_%s_%s.root" % (options_.outputfolder, options_.suffix, period, layers_remaining)
outfile = TFile(outfilename, "recreate")
if histos["h_chi2ndof2D"].GetEntries()>0:
    histos["h_chi2ndof2D"].Scale(1.0/histos["h_chi2ndof2D"].GetEntries())
for label in histos:
    histos[label].Write()
outfile.Close()
