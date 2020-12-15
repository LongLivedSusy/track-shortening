#include <vector>
#include <TLorentzVector.h>
#define _USE_MATH_DEFINES // for C++  
#include <cmath>  

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/Common/interface/SortedCollection.h"
#include "DataFormats/Common/interface/OwnVector.h"
#include "DataFormats/Common/interface/ClonePolicy.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/HcalRecHit/interface/HBHERecHit.h"
#include "DataFormats/HcalRecHit/interface/HFRecHit.h"
#include "DataFormats/HcalRecHit/interface/HORecHit.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/TrackerRecHit2D/interface/BaseTrackerRecHit.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/Records/interface/TrackerTopologyRcd.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"

#include "FWCore/Framework/interface/global/EDProducer.h"
#include "DataFormats/SiStripCluster/interface/SiStripCluster.h"
#include "DataFormats/SiPixelCluster/interface/SiPixelCluster.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripMatchedRecHit2D.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Provenance/interface/ProductID.h"
#include "DataFormats/Common/interface/ContainerMask.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/TrackerRecHit2D/interface/ClusterRemovalInfo.h"
#include "TrackingTools/PatternTools/interface/TrackCollectionTokens.h"
#include "RecoTracker/TransientTrackingRecHit/interface/Traj2TrackHits.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "TH1.h"
#include "TH2.h"


class MyMonitoringAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit MyMonitoringAnalyzer(const edm::ParameterSet&);
  ~MyMonitoringAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  edm::EDGetTokenT<std::vector<reco::Muon>> muonsToken_;
  edm::EDGetTokenT<std::vector<reco::GsfElectron>> electronsToken_;
  edm::EDGetTokenT<std::vector<reco::Track>> tracksToken_;
  edm::EDGetTokenT<std::vector<reco::Track>> selTracksToken_;
  edm::EDGetTokenT<std::vector<reco::Track>> muonTracksToken_;
  edm::EDGetTokenT<edmNew::DetSetVector<SiStripCluster>> stripClusterToken_;
  edm::EDGetTokenT<edmNew::DetSetVector<SiPixelCluster>> pixelClusterToken_;
  //edm::EDGetTokenT<std::vector<reco::Vertex>> vtxToken_;
  edm::EDGetTokenT<reco::VertexCollection> primaryVerticesToken;
  
  int minNumberOfHits;                                      
  double_t matchInDr; 
  std::string matchTo; 
  bool trackingOn;
  bool rClusterOn;
  bool selOn;
  bool debug;

  TH1F* hist_yield;
  TH1F* hist_mu_pt;
  TH1F* hist_mu_eta;
  TH1F* hist_mu_n;
  
  TH1F* hist_e_pt;
  TH1F* hist_e_eta;
  TH1F* hist_e_n;
  
  TH1F* hist_pre_n; // control plot for preselection collection. should be alsways the same for all removal steps. Also same as hist_selTrack_n
  TH1F* hist_pre_n_barrel; // control plot for preselection collection. should be alsways the same for all removal steps. Also same as hist_selTrack_n
  TH1F* hist_pre_pt; // control plot for preselection collection. should be alsways the same for all removal steps. Also same as hist_selTrack_n
  TH1F* hist_pre_eta; // control plot for preselection collection. should be alsways the same for all removal steps. Also same as hist_selTrack_n
  TH1F* hist_pre_chi2ndof; // control plot for preselection collection. should be alsways the same for all removal steps. Also same as hist_selTrack_n
  TH2F* hist_pre_pteta;

  TH1F* hist_pre_n_PU1; // bin preselection in PU
  TH1F* hist_pre_n_PU2; //
  TH1F* hist_pre_n_PU3; //
  TH1F* hist_pre_n_PU4; // 
  
  TH1F* hist_track_pt;
  TH1F* hist_track_eta;
  TH1F* hist_track_n;
  
  TH1F* hist_selTrack_pt;
  TH1F* hist_selTrack_eta;
  TH1F* hist_selTrack_layersWithout;
  TH1F* hist_selTrack_layersWith;
  TH1F* hist_selTrack_chi2ndof;
  TH1F* hist_selTrack_algos;
  TH1F* hist_selTrack_lostHits;
  TH1F* hist_selTrack_validHits;
  TH1F* hist_selTrack_validFrac;
  TH1F* hist_selTrack_d0;
  TH1F* hist_selTrack_dsz;
  TH1F* hist_selTrack_dz;
  TH1F* hist_selTrack_iso;
  
  TH1F* hist_pass_iso; // these are the most interesting histos after reRECO! 1. min deltaR to track in preselection
  TH1F* hist_pass_pass; // 2. number of tracks match to a track from the preselection
  TH1F* hist_pass_pass_barrel; // 2. number of tracks match to a track from the preselection
  TH1F* hist_pass_pt; // matched / passed tracks: pt
  TH1F* hist_pass_ptTrue; // matched / passed tracks: pt(true) = pt(sel)
  TH1F* hist_pass_eta; // 
  TH1F* hist_pass_chi2ndof; //  
  TH2F* hist_pass_pteta;
  TH1F* hist_pass_dRmin;
  TH1F* hist_pass_Nmatch; // number of matches per track
  
  TH1F* hist_pass_pass_PU1; // bin passed in PU
  TH1F* hist_pass_pass_PU2; // 
  TH1F* hist_pass_pass_PU3; // 
  TH1F* hist_pass_pass_PU4; // 
  
  TH1F* hist_nVtx; // number of matches per track  
  
  TH1F* hist_ptRes; // 
  
  TH1F* hist_ptRes_pt1;   // bin pt-resolution in pt(true)
  TH1F* hist_ptRes_pt2;   // pt1 : 1/pt = 0 - 0.001, pt > 1000 , pt2: 1/pt=0.001 - 0.002 pt=500-1000, pt3: 0.002 - 0.0025 , pt4: 0.0025-0.005 pt5: 0.005 - 0.1, pt6: 0.1-0.5, pt7: 0.5 -1. , pt8: 1/pt>1,
  TH1F* hist_ptRes_pt3;   
  TH1F* hist_ptRes_pt4;   
  TH1F* hist_ptRes_pt5;   
  TH1F* hist_ptRes_pt6;   
  TH1F* hist_ptRes_pt7;   
  TH1F* hist_ptRes_pt8;   
 
  TH1F* hist_ptRes_eta1;   // bin pt-resolution in eta(true)
  TH1F* hist_ptRes_eta2;   // eta1 : 2.4 - 1.479, eta2: 1.479 - 0.8, eta3: 0.8 - 0, eta4: , eta5, eta6 negativ
  TH1F* hist_ptRes_eta3;   //
  TH1F* hist_ptRes_eta4;   // 
  TH1F* hist_ptRes_eta5;   
  TH1F* hist_ptRes_eta6;    
 
  TH1F* hist_ptRes_phi1;   // bin pt-resolution in phi(true)
  TH1F* hist_ptRes_phi2;   // phi1 : -pi - -pi/2, phi2: -pi/2 - 0, phi3,4: positiv
  TH1F* hist_ptRes_phi3;   
  TH1F* hist_ptRes_phi4;   
  
  TH1F* hist_vtxRes; // 
  
  TH1F* hist_vtxRes_pt1;   // bin vtx-resolution (z) in pt(true)
  TH1F* hist_vtxRes_pt2;   // pt1 : 1/pt = 0 - 0.001, pt > 1000 , pt2: 1/pt=0.001 - 0.002 pt=500-1000, pt3: 0.002 - 0.0025 , pt4: 0.0025-0.005 pt5: 0.005 - 0.1, pt6: 0.1-0.5, pt7: 0.5 -1. , pt8: 1/pt>1,
  TH1F* hist_vtxRes_pt3;   
  TH1F* hist_vtxRes_pt4;   
  TH1F* hist_vtxRes_pt5;   
  TH1F* hist_vtxRes_pt6;   
  TH1F* hist_vtxRes_pt7;   
  TH1F* hist_vtxRes_pt8;   
 
  TH1F* hist_vtxRes_eta1;   // bin vtx-resolution (z) in eta(true)
  TH1F* hist_vtxRes_eta2;   // eta1 : 2.4 - 1.479, eta2: 1.479 - 0.8, eta3: 0.8 - 0, eta4: , eta5, eta6 negativ
  TH1F* hist_vtxRes_eta3;   //
  TH1F* hist_vtxRes_eta4;   // 
  TH1F* hist_vtxRes_eta5;   
  TH1F* hist_vtxRes_eta6;    
 
  TH1F* hist_vtxRes_phi1;   // bin vtx-resolution (z) in phi(true)
  TH1F* hist_vtxRes_phi2;   // phi1 : -pi - -pi/2, phi2: -pi/2 - 0, phi3,4: positiv
  TH1F* hist_vtxRes_phi3;   
  TH1F* hist_vtxRes_phi4;   

  TH1F* hist_vtxResX_pt1;   // bin vtx-resolution (x) in pt(true)
  TH1F* hist_vtxResX_pt2;   // pt1 : 1/pt = 0 - 0.001, pt > 1000 , pt2: 1/pt=0.001 - 0.002 pt=500-1000, pt3: 0.002 - 0.0025 , pt4: 0.0025-0.005 pt5: 0.005 - 0.1, pt6: 0.1-0.5, pt7: 0.5 -1. , pt8: 1/pt>1,
  TH1F* hist_vtxResX_pt3;   
  TH1F* hist_vtxResX_pt4;   
  TH1F* hist_vtxResX_pt5;   
  TH1F* hist_vtxResX_pt6;   
  TH1F* hist_vtxResX_pt7;   
  TH1F* hist_vtxResX_pt8;   
 
  TH1F* hist_vtxResX_eta1;   // bin vtx-resolution (X) in eta(true)
  TH1F* hist_vtxResX_eta2;   // eta1 : 2.4 - 1.479, eta2: 1.479 - 0.8, eta3: 0.8 - 0, eta4: , eta5, eta6 negativ
  TH1F* hist_vtxResX_eta3;   //
  TH1F* hist_vtxResX_eta4;   // 
  TH1F* hist_vtxResX_eta5;   
  TH1F* hist_vtxResX_eta6;    
 
  TH1F* hist_vtxResX_phi1;   // bin vtx-resolution (X) in phi(true)
  TH1F* hist_vtxResX_phi2;   // phi1 : -pi - -pi/2, phi2: -pi/2 - 0, phi3,4: positiv
  TH1F* hist_vtxResX_phi3;   
  TH1F* hist_vtxResX_phi4;   
  
  TH1F* hist_vtxResY_pt1;   // bin vtx-resolution (Y) in pt(true)
  TH1F* hist_vtxResY_pt2;   // pt1 : 1/pt = 0 - 0.001, pt > 1000 , pt2: 1/pt=0.001 - 0.002 pt=500-1000, pt3: 0.002 - 0.0025 , pt4: 0.0025-0.005 pt5: 0.005 - 0.1, pt6: 0.1-0.5, pt7: 0.5 -1. , pt8: 1/pt>1,
  TH1F* hist_vtxResY_pt3;   
  TH1F* hist_vtxResY_pt4;   
  TH1F* hist_vtxResY_pt5;   
  TH1F* hist_vtxResY_pt6;   
  TH1F* hist_vtxResY_pt7;   
  TH1F* hist_vtxResY_pt8;   
 
  TH1F* hist_vtxResY_eta1;   // bin vtx-resolution (Y) in eta(true)
  TH1F* hist_vtxResY_eta2;   // eta1 : 2.4 - 1.479, eta2: 1.479 - 0.8, eta3: 0.8 - 0, eta4: , eta5, eta6 negativ
  TH1F* hist_vtxResY_eta3;   //
  TH1F* hist_vtxResY_eta4;   // 
  TH1F* hist_vtxResY_eta5;   
  TH1F* hist_vtxResY_eta6;    
 
  TH1F* hist_vtxResY_phi1;   // bin vtx-resolution (Y) in phi(true)
  TH1F* hist_vtxResY_phi2;   // phi1 : -pi - -pi/2, phi2: -pi/2 - 0, phi3,4: positiv
  TH1F* hist_vtxResY_phi3;   
  TH1F* hist_vtxResY_phi4;    

  TH1F* hist_td_layersWithout;
  TH1F* hist_td_layersWith;
  TH1F* hist_td_chi2ndof;
  TH1F* hist_td_algos;
  TH1F* hist_td_lostHits;
  TH1F* hist_td_validHits;
  TH1F* hist_td_validFrac;
  TH1F* hist_td_d0;
  TH1F* hist_td_dsz;
  TH1F* hist_td_dz;
  TH1F* hist_td_iso;
  // Qoverp
  
  TH1F* hist_muTrack_pt;
  TH1F* hist_muTrack_eta;
  TH1F* hist_muTrack_n;
  
  TH1F* hist_sClus_n;
  TH1F* hist_sClus_q;
  //isMerged()
  
  TH1F* hist_pClus_n;
  TH1F* hist_pClus_q;
  TH1F* hist_pClus_size;
  //colspan, rowspan
  
  // make a list of mu, e, track, mutrack, sClus, pClus
  // for i in list make TH1F...

};

//                                                                                                                                                                                                             
// constructors and destructor                                                                                                                                                                                 
//                                                                                                                                                                                                             
MyMonitoringAnalyzer::MyMonitoringAnalyzer(const edm::ParameterSet& iConfig)
{
   usesResource("TFileService");
   muonsToken_ = consumes<std::vector<reco::Muon>>(iConfig.getParameter<edm::InputTag>("muons"));
   electronsToken_ = consumes<std::vector<reco::GsfElectron>>(iConfig.getParameter<edm::InputTag>("electrons"));
   tracksToken_ = consumes<std::vector<reco::Track>>(iConfig.getParameter<edm::InputTag>("tracks"));
   selTracksToken_ = consumes<std::vector<reco::Track>>(iConfig.getParameter<edm::InputTag>("selTracks"));
   muonTracksToken_ = consumes<std::vector<reco::Track>>(iConfig.getParameter<edm::InputTag>("muonTracks"));
   stripClusterToken_ = consumes<edmNew::DetSetVector<SiStripCluster>>(iConfig.getParameter<edm::InputTag>("stripCluster"));
   pixelClusterToken_ = consumes<edmNew::DetSetVector<SiPixelCluster>>(iConfig.getParameter<edm::InputTag>("pixelCluster"));
   //vtxToken_ = consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("vertexCollection")); 
   primaryVerticesToken = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection")); 
 
   //minNumberOfHits = iConfig.getParameter<int>("minNumberOfHits");   
   minNumberOfHits = iConfig.getParameter<int>("minNumberOfLayers");   
   matchInDr = iConfig.getParameter<double_t>("requiredDr");  
   matchTo = iConfig.getParameter<std::string>("matchTo"); 
   selOn = iConfig.getParameter<bool>("selectionDetails");
   trackingOn = iConfig.getParameter<bool>("trackingDetails");
   rClusterOn = iConfig.getParameter<bool>("clusterDetails");
   debug = iConfig.getParameter<bool>("debug");
}


MyMonitoringAnalyzer::~MyMonitoringAnalyzer()
{
}

void
MyMonitoringAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<std::vector<reco::Muon>> muons;
  iEvent.getByToken(muonsToken_,muons);
  
  edm::Handle<std::vector<reco::GsfElectron>> electrons;
  iEvent.getByToken(electronsToken_,electrons);
  
  edm::Handle<std::vector<reco::Track>> tracks;
  iEvent.getByToken(tracksToken_,tracks);
  
  edm::Handle<std::vector<reco::Track>> selTracks;
  iEvent.getByToken(selTracksToken_,selTracks);
  
  edm::Handle<std::vector<reco::Track>> muonTracks;
  iEvent.getByToken(muonTracksToken_,muonTracks);  
  
  edm::Handle<edmNew::DetSetVector<SiStripCluster>> stripCluster;
  iEvent.getByToken(stripClusterToken_,stripCluster);
  
  edm::Handle<edmNew::DetSetVector<SiPixelCluster>> pixelCluster;
  iEvent.getByToken(pixelClusterToken_,pixelCluster);   
  
  // handle to the primary vertex collection
  edm::Handle<reco::VertexCollection> primaryVertices;
  iEvent.getByToken(primaryVerticesToken, primaryVertices);   
  
  hist_yield->Fill(0.5);
  
  std::map<std::string, int> algoNames;
  algoNames["duplicateMerge"] = -1;
  algoNames["initialStep"] = 0;     
  algoNames["lowPtTripletStep"] = 1;     
  algoNames["pixelPairStep"] = 2;     
  algoNames["detachedTripletStep"] = 3;     
  algoNames["mixedTripletStep"] = 4;     
  algoNames["pixelLessStep"] = 5;     
  algoNames["tobTecStep"] = 6;     
  algoNames["muonSeededStepInOut"] = 7;  

  for(const auto& mu : *muons){
    hist_mu_pt->Fill(1/(mu.pt()));
    hist_mu_eta->Fill(mu.eta());
    hist_mu_n->Fill(0.5);
  }
  
  for(const auto& e : *electrons){
    hist_e_pt->Fill(1/(e.pt()));
    hist_e_eta->Fill(e.eta());
    hist_e_n->Fill(0.5);
  }
  int nVtx = 0;
  for(const reco::Vertex* vtx = &(*primaryVertices->begin());vtx != & (*primaryVertices->end());vtx++) {
	 nVtx++;
 
  }

  hist_nVtx->Fill(nVtx);
  
  for(const auto& sel : *selTracks){
	reco::HitPattern hitpattern = sel.hitPattern();
    hist_pre_n->Fill(0.5);
    hist_pre_pt->Fill(1/sel.pt());
    hist_pre_eta->Fill(sel.eta());
    hist_pre_pteta->Fill(sel.pt(),sel.eta());
    hist_pre_chi2ndof->Fill((sel.chi2())/(sel.ndof()));
	if(nVtx < 10) {
		hist_pre_n_PU1->Fill(0.5);

	}
	else if(nVtx>=10 &&(nVtx<18)) {
		hist_pre_n_PU2->Fill(0.5);
	}
	else if(nVtx>=18 && (nVtx<26)) {
		hist_pre_n_PU3->Fill(0.5);
	}
	else if(nVtx>=26) {
		hist_pre_n_PU4->Fill(0.5);
	}
	if(1.4>abs(sel.eta())) hist_pre_n_barrel->Fill(0.5);

    int nMatches = 0;  
    TLorentzVector pSel (sel.px(), sel.py(),sel.pz(), sel.pt());        
    
    // match to track in preselection = PASSED 
	Double_t Rmin = 10;
	//reco::Track *match = new reco::Track(); 					
	reco::Track match; 					
	for( const auto& track : *tracks){
		TLorentzVector pTrack (track.px(), track.py(), track.pz(), track.pt());
		Double_t dr = pTrack.DeltaR(pSel);
		if (dr < Rmin) {
			Rmin = dr;
			match = track;
		}
		hist_pass_iso->Fill(Rmin);
	}
	if(Rmin < matchInDr){ // matches , passed reRECO!
		 nMatches ++;
		 hist_pass_pass->Fill(0.5);
		 hist_pass_dRmin->Fill(Rmin);
		 hist_pass_pt->Fill(1/match.pt());
		 hist_pass_ptTrue->Fill(1/sel.pt());
		 hist_pass_eta->Fill(match.eta());
		 hist_pass_chi2ndof->Fill((match.chi2())/(match.ndof()));
		 hist_pass_pteta->Fill(match.pt(), match.eta());
		 if(1.4>abs(match.eta())) hist_pass_pass_barrel->Fill(0.5);
		 hist_ptRes->Fill((1/match.pt())-((1/sel.pt())));
		 double_t pt = sel.pt();
		 double_t eta = sel.eta();
		 double_t phi = sel.phi();

		 if(1/pt<0.001){
			  hist_ptRes_pt1->Fill((1/match.pt())-((1/sel.pt())));
			  hist_vtxRes_pt1->Fill((match.vz())-(sel.vz()));
			  hist_vtxResX_pt1->Fill((match.vx())-(sel.vx()));
			  hist_vtxResY_pt1->Fill((match.vy())-(sel.vy()));
		  }
		 else if((1/pt>=0.001)&&(1/pt<0.002)) {
			 hist_ptRes_pt2->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt2->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt2->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt2->Fill((match.vy())-(sel.vy()));
			 }
		 else if((1/pt>=0.002)&&(1/pt<0.005)) {
			 hist_ptRes_pt3->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt3->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt3->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt3->Fill((match.vy())-(sel.vy()));
			 }
		 else if((1/pt>=0.005)&&(1/pt<0.01)) {
			 hist_ptRes_pt4->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt4->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt4->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt4->Fill((match.vy())-(sel.vy()));
			 }
		 else if((1/pt>=0.01)&&(1/pt<0.1)) {
			 hist_ptRes_pt5->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt5->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt5->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt5->Fill((match.vy())-(sel.vy()));
			 }
		 else if((1/pt>=0.1)&&(1/pt<0.5)) {
			 hist_ptRes_pt6->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt6->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt6->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt6->Fill((match.vy())-(sel.vy()));
			 }
		 else if((1/pt>=0.5)&&(1/pt<1)) {
			 hist_ptRes_pt7->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt7->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt7->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt7->Fill((match.vy())-(sel.vy()));
			 }	
		 else if((1/pt>=1)) {
			 hist_ptRes_pt8->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_pt8->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_pt8->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_pt8->Fill((match.vy())-(sel.vy()));
			 }
		 
		 if((2.4>=eta)&&(eta>1.479)) {
			 hist_ptRes_eta1->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_eta1->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_eta1->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_eta1->Fill((match.vy())-(sel.vy()));
		 }
		 else if((1.479>=eta)&&(eta>0.8)) {
			 hist_ptRes_eta2->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_eta2->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_eta2->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_eta2->Fill((match.vy())-(sel.vy()));
			 }
		 else if((0.8>=eta)&&(eta>0.)) {
			 hist_ptRes_eta3->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_eta3->Fill((match.vz())-(sel.vz()));	 
			 hist_vtxResX_eta3->Fill((match.vx())-(sel.vx()));	 
			 hist_vtxResY_eta3->Fill((match.vy())-(sel.vy()));	 
			 }
		 else if((0>=eta)&&(eta>-0.8)) {
			 hist_ptRes_eta4->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_eta4->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_eta4->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_eta4->Fill((match.vy())-(sel.vy()));
			 }
		 else if((-0.8>=eta)&&(eta>-1.479)) {
			 hist_ptRes_eta5->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_eta5->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_eta5->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_eta5->Fill((match.vy())-(sel.vy()));
			 }
		 else if((-1.479>=eta)&&(eta>=-2.4)) {
			 hist_ptRes_eta6->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_eta6->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_eta6->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_eta6->Fill((match.vy())-(sel.vy()));
			 }
		 
		 if((M_PI>=phi)&&(phi>M_PI/2)) {
			 hist_ptRes_phi1->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_phi1->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_phi1->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_phi1->Fill((match.vy())-(sel.vy()));
		 }
		 else if((M_PI/2>=phi)&&(phi>0)) {
			 hist_ptRes_phi2->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_phi2->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_phi2->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_phi2->Fill((match.vy())-(sel.vy()));
			 }
		 else if((0>=phi)&&(phi>-M_PI/2)) {
			 hist_ptRes_phi3->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_phi3->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_phi3->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_phi3->Fill((match.vy())-(sel.vy()));
			 }
		 else if((-M_PI/2>=phi)&&(phi>-M_PI)) {
			 hist_ptRes_phi4->Fill((1/match.pt())-((1/sel.pt())));
			 hist_vtxRes_phi4->Fill((match.vz())-(sel.vz()));
			 hist_vtxResX_phi4->Fill((match.vx())-(sel.vx()));
			 hist_vtxResY_phi4->Fill((match.vy())-(sel.vy()));
			 }
			 
		 if(nVtx < 10) {
			 hist_pass_pass_PU1->Fill(0.5);

		 }
		 else if(nVtx>=10 &&(nVtx<18)) {
			 hist_pass_pass_PU2->Fill(0.5);
			 }
		 else if(nVtx>=18 && (nVtx<26)) {
			 hist_pass_pass_PU3->Fill(0.5);
			 }
		 else if(nVtx>=26) {
			 hist_pass_pass_PU4->Fill(0.5);
			 }
		  
		 hist_vtxRes->Fill((match.vz())-(sel.vz()));
	 }
	 hist_pass_Nmatch->Fill(nMatches);		
	 
	// details on selction			
    if(selOn){
		hist_selTrack_eta->Fill(sel.eta());
		hist_selTrack_pt->Fill(1/sel.pt());
		hist_selTrack_layersWithout->Fill(hitpattern.trackerLayersWithoutMeasurement(reco::HitPattern::TRACK_HITS));
		hist_selTrack_layersWith->Fill(hitpattern.trackerLayersWithMeasurement());
		if (algoNames.find(sel.algoName()) != algoNames.end()){
			hist_selTrack_algos->Fill(algoNames[sel.algoName()]);				
		}
		hist_selTrack_lostHits->Fill(sel.numberOfLostHits());
		hist_selTrack_validHits->Fill(sel.numberOfValidHits());
		hist_selTrack_validFrac->Fill(sel.validFraction());
		hist_selTrack_chi2ndof->Fill(sel.normalizedChi2());
		hist_selTrack_d0->Fill(sel.d0());
		//hist_selTrack_d0->SetError(sel.d0Error());
		hist_selTrack_dsz->Fill(sel.dsz());
		//hist_selTrack_dsz->SetError(sel.dszError());
		hist_selTrack_dz->Fill(sel.dz());	
		//hist_selTrack_dz->SetError(sel.dzError());
		TLorentzVector pSel (sel.px(), sel.py(), sel.pz(), sel.pt());
		Double_t dRmin = 10;
		for( const auto& t : *tracks){
			TLorentzVector pMatched (t.px(), t.py(),t.pz(), t.pt());
			if (pMatched != pSel){
				Double_t dr = pSel.DeltaR(pMatched);
				if (dr < dRmin) dRmin = dr;
			}
		}
		hist_selTrack_iso->Fill(dRmin);	
  
    }       
  }
  
  for(const auto& track : *tracks){
    hist_track_pt->Fill(1/(track.pt()));
    hist_track_eta->Fill(track.eta());
    hist_track_n->Fill(0.5);
	TLorentzVector pTrack (track.px(), track.py(), track.pz(), track.pt());  
    // details on tracking      
    if(trackingOn) {
		if (debug) std::cout << "analysing tracking ..." << std::endl;
		reco::HitPattern hitpattern = track.hitPattern();
		
		if (algoNames.find(track.algoName()) != algoNames.end()){
			//std::cout << "algoname: " << track.algoName() << "number " << algoNames[track.algoName()] << std::endl;
			hist_td_algos->Fill(algoNames[track.algoName()]);				
		}
		
		hist_td_layersWithout->Fill(hitpattern.trackerLayersWithoutMeasurement(reco::HitPattern::TRACK_HITS));
		hist_td_layersWith->Fill(hitpattern.trackerLayersWithMeasurement());
		hist_td_lostHits->Fill(track.numberOfLostHits());
		hist_td_validHits->Fill(track.numberOfValidHits());
		hist_td_validFrac->Fill(track.validFraction());
		hist_td_chi2ndof->Fill((track.chi2())/(track.ndof()));
		hist_td_d0->Fill(track.d0());
		//hist_td_d0->SetError(track.d0Error());
		hist_td_dsz->Fill(track.dsz());
		//hist_td_dsz->SetError(track.dszError());
		hist_td_dz->Fill(track.dz());	
		//hist_td_dz->SetError(track.dzError());
		
		Double_t min = 10;
		for( const auto& t : *tracks){
			TLorentzVector pMatched (t.px(), t.py(),t.pz(), t.pt());
			if (pMatched != pTrack){         
					Double_t dr = pTrack.DeltaR(pMatched);
					if (dr < min) min = dr;
			}
		}
		hist_td_iso->Fill(min);
	}	  
  }

  
  for(const auto& muTrack : *muonTracks){
    hist_muTrack_pt->Fill(1/(muTrack.pt()));
    hist_muTrack_eta->Fill(muTrack.eta());
    hist_muTrack_n->Fill(0.5);
  }
  
  for(const auto& sClus : *stripCluster){
    hist_sClus_n->Fill(0.5);
    if (rClusterOn){
		 //std::cout << sClus.begin()->charge()<< std::endl;
		auto hb = sClus.begin();
		for (unsigned int h=0; h<sClus.size(); h++){
			auto scluster = *(hb+h);
			//auto const & cluster = *scluster;
			hist_sClus_q->Fill(scluster.charge());
		}
	}
  }
	
  for(const auto& pClus : *pixelCluster){
    hist_pClus_n->Fill(0.5);
    if (rClusterOn){
		auto ib = pClus.begin();
		for (unsigned int i=0; i<pClus.size(); i++){
			auto pcluster = *(ib+i);
			//std::cout << "here i am, charge: " << pcluster.charge() << std::endl;
			hist_pClus_q->Fill(pcluster.charge());
			//auto const & cluster = *scluster;
			hist_pClus_size->Fill(pcluster.size());
		}		
	}
  }
  
  
}


// ------------ method called once each job just before starting event loop  ------------                                                                                                                      
void
MyMonitoringAnalyzer::beginJob()
{
  //register to the TFileService                                                                                                                                                                               
  edm::Service<TFileService> fs;

  // book histograms:                                                                                                                                                                                          
  hist_yield   = fs->make<TH1F>("yield"    , "event yield"                , 1  , 0., 1.);
  hist_mu_pt   = fs->make<TH1F>("mupt"     , "muon 1/pt;1/pt[GeV];muons"      , 50 , 0., 10.);
  hist_mu_eta  = fs->make<TH1F>("mueta"     , "muon eta;eta;muons"      , 50 ,-2.5, 2.5);
  hist_mu_n  = fs->make<TH1F>("mun"     , "number of muons"      , 1 ,0.,1.);
  
  hist_e_pt   = fs->make<TH1F>("ept"     , "electron 1/pt;1/pt[GeV];electrons"      , 50 , 0., 10.);
  hist_e_eta  = fs->make<TH1F>("eeta"     , "electron eta;eta;electrons"      , 50 ,-2.5, 2.5);
  hist_e_n  = fs->make<TH1F>("en"     , "number of electrons"      , 1 ,0.,1.);
  
  hist_pre_n  = fs->make<TH1F>("pren"     , "number of tracks in pre-selection collection"      , 1 ,0.,1.);
  hist_pre_n_barrel  = fs->make<TH1F>("prenbarrel"     , "number of barrel tracks in pre-selection collection"      , 1 ,0.,1.);
  hist_pre_pt  = fs->make<TH1F>("prept"     , "tracks in pre-selection: pt"      , 200 ,0.,10.);
  hist_pre_pteta  = fs->make<TH2F>("prepteta"     , "tracks in pre-selection: pt, eta"      , 200 ,0.,20. , 50 ,-2.5, 2.5);
  hist_pre_eta  = fs->make<TH1F>("preeta"     , "tracks in pre-selection: eta"      , 50 ,-2.5, 2.5);
  hist_pre_chi2ndof  = fs->make<TH1F>("prechi2ndof"     , "racks in pre-selection: chi-2/Ndof"     , 60 ,0.,30.);
  
  hist_pre_n_PU1  = fs->make<TH1F>("prenPU1"     , "selected tracks with < 10 vertices"      , 1 ,0.,1.);
  hist_pre_n_PU2 = fs->make<TH1F>("prenPU2"     , "selected tracks with 10 - 17 vertices"      , 1 ,0.,1.);  
  hist_pre_n_PU3  = fs->make<TH1F>("prenPU3"     , "selected tracks with 18 - 25  vertices"      , 1 ,0.,1.);
  hist_pre_n_PU4  = fs->make<TH1F>("prenPU4"     , "selected tracks with > 25 vertices"      , 1 ,0.,1.);

  //hist_pre_pt1_pt  = fs->make<TH1F>("prept1pt"     , "selected tracks with p_{t} > 1000 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt2_pt  = fs->make<TH1F>("prept2pt"     , "selected tracks with p_{t} = 500 - 1000 GeV;1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt3_pt  = fs->make<TH1F>("prept3pt"     , "selected tracks with p_{t} = 500 - 400 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt4_pt  = fs->make<TH1F>("prept4pt"     , "selected tracks with p_{t}: 400 - 200 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt5_pt  = fs->make<TH1F>("prept5pt"     , "selected tracks with p_{t}: 200 - 10 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt6_pt  = fs->make<TH1F>("prept6pt"     , "selected tracks with p_{t}: 10 - 2 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt7_pt  = fs->make<TH1F>("prept7pt"     , "selected tracks with p_{t}: 2 - 1 GeV; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pre_pt8_pt  = fs->make<TH1F>("prept8pt"     , "selected tracks with p_{t}: < 1 GeV; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  
  //hist_pre_eta1_pt  = fs->make<TH1F>("preeta1pt"     , "selected tracks with #eta:-2.4 - -1.479 ;1/p_{t}[GeV]; tracks"     , 100 ,-2.5,-1.5);
  //hist_pre_eta2_pt  = fs->make<TH1F>("preeta2pt"     , "selected tracks with #eta: -1.479 - -0.8;1/p_{t}[GeV]; tracks"       , 100 ,-1.5,-0.5);
  //hist_pre_eta3_pt  = fs->make<TH1F>("preeta3pt"     , "selected tracks with #eta: -0.8 - 0;1/p_{t}[GeV]; tracks"       , 100 ,-1,0);
  //hist_pre_eta4_pt  = fs->make<TH1F>("preeta4pt"     , "selected tracks with #eta: 0 - 0.8;1/p_{t}[GeV]; tracks"       , 100 ,0.,1.);
  //hist_pre_eta5_pt  = fs->make<TH1F>("preeta5pt"     , "selected tracks with #eta: 0.8 - 1.479;1/p_{t}[GeV]; tracks"       , 100 ,0.5,1.5);
  //hist_pre_eta6_pt  = fs->make<TH1F>("preeta6pt"     , "selected tracks with #eta: 1.479 - 2.4;1/p_{t}[GeV]; tracks"       , 100 ,1.5,2.5);
  
  //hist_pre_phi1_pt  = fs->make<TH1F>("prephi1pt"     , "selected tracks with #phi: -#pi - - #pi / 2 ;1/p_{t}[GeV]; tracks"      , 100 ,M_PI,M_PI/2);
  //hist_pre_phi2_pt = fs->make<TH1F>("prephi2pt"     , "selected tracks with #phi: -#pi /2 - 0;1/p_{t}[GeV]; tracks"         , 100 ,M_PI/2,0.);
  //hist_pre_phi3_pt  = fs->make<TH1F>("prephi3pt"     , "selected tracks with #phi: 0 - #pi/2;1/p_{t}[GeV]; tracks"       , 100 ,0.,M_PI/2);
  //hist_pre_phi4_pt  = fs->make<TH1F>("prephi4pt"     , "selected tracks with #phi: #pi /2 - #pi;1/p_{t}[GeV]; tracks"       , 100 ,M_PI/2,M_PI);
  
  //hist_pre_PU1_n  = fs->make<TH1F>("prePU1n"     , "selected tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,0.,2.);
  //hist_pre_PU2_n  = fs->make<TH1F>("prePU2n"     , "selected tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,2.,4.);
  //hist_pre_PU3_n  = fs->make<TH1F>("prePU3n"     , "selected tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,4.,6.);
  //hist_pre_PU4_n  = fs->make<TH1F>("prePU4n"     , "selected tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,6.,100.);

  hist_track_pt   = fs->make<TH1F>("trackpt"     , "track 1/pt;1/pt[GeV];tracks"      , 200 , 0., 20.);
  hist_track_eta  = fs->make<TH1F>("tracketa"     , "tracks eta;eta;tracks"      , 50 ,-2.5, 2.5);
  hist_track_n  = fs->make<TH1F>("trackn"     , "number of tracks"      , 1 ,0.,1.);

  if(selOn){
  hist_selTrack_pt   = fs->make<TH1F>("selTrackpt"     , "selected Track 1/pt;1/pt[GeV];sel.Tracks"      , 200 , 0., 20.);
  hist_selTrack_eta  = fs->make<TH1F>("selTracketa"     , "selected Tracks eta;eta;sel.Tracks"      , 50 ,-2.5, 2.5);
  hist_selTrack_chi2ndof  = fs->make<TH1F>("selTrackchi2"     , "selction details: chi2/ndof; chi2/ndof; tracks"      , 60 ,0.,30.);
  hist_selTrack_layersWithout  = fs->make<TH1F>("selTracklayersWithout"     , "selction details: trackLayersWithoutMeasurement; layers; tracks"      , 30 ,0.,30.);
  hist_selTrack_layersWith  = fs->make<TH1F>("selTracklayersWith"     , "selction details: trackerLayersWithMeasurement; layers; tracks"      , 30 ,0.,30.);
  hist_selTrack_algos  = fs->make<TH1F>("selTrackalgos"     , "selction details: tracking algo;   duplicateMerge:-1 initialStep:0 lowPtTripletStep:1 pixelPairStep:2 detachedTripletStep:3 mixedTripletStep:4 pixelLessStep:5 tobTecStep:6 muonSeededStepInOut:7; tracks"      , 8 ,-1.,7.);
  hist_selTrack_lostHits  = fs->make<TH1F>("selTracklostHits"     , "selction details: N lost hits;   hits; tracks"      , 10 ,0.,10.);
  hist_selTrack_validHits  = fs->make<TH1F>("selTrackvalidHits"     , "selction details: N valid Hits;   hits; tracks"      , 35 ,0.,35.);
  hist_selTrack_validFrac  = fs->make<TH1F>("selTrackvalidFrac"     , "selction details: fract. of valid hits;   fract. of hits; tracks"      , 10,0.,1.);
  hist_selTrack_d0  = fs->make<TH1F>("selTrackd0"     , "selction details: d0;   d0; tracks"      , 500 ,0.,5.);
  hist_selTrack_dsz  = fs->make<TH1F>("selTrackdsz"     , "selction details: dsz;   dsz; tracks"      , 35 ,0.,10.);
  hist_selTrack_dz  = fs->make<TH1F>("selTrackdz"     , "selction details: dz;   dz; tracks"      , 35 ,0.,10.);
  hist_selTrack_iso  = fs->make<TH1F>("selTrackiso"     , "selction details: Minimum DeltaR between tracks;   dR; tracks"      , 100 ,0.,1.);
  }
  
  hist_pass_iso  = fs->make<TH1F>("passiso"     , "Minimum DeltaR to preselected track;   dR; tracks"      , 1000 ,0.,10);
  hist_pass_dRmin  = fs->make<TH1F>("passdRmin"     , "Minimum DeltaR from  matched to preselected track;   dR; tracks"      , 100 ,0.,0.01);
  hist_pass_pass  = fs->make<TH1F>("passpass"     , "passed tracks: Number of tracks matched to presel. tracks"      , 1 ,0.,1.);
  hist_pass_pass_barrel  = fs->make<TH1F>("passpassbarrel"     , "passed barrel tracks: Number of tracks matched to presel. tracks"      , 1 ,0.,1.);
  hist_pass_pt  = fs->make<TH1F>("passpt"     , "passed tracks: 1/pt; 1/pt; tracks"     , 200 ,0.,20.);
  hist_pass_ptTrue  = fs->make<TH1F>("passptTrue"     , "passed tracks: 1/pt(true); 1/pt(true); tracks"     , 200 ,0.,10.);
  hist_pass_eta  = fs->make<TH1F>("passeta"     , "passed tracks: eta; eta; tracks"      , 50 ,-2.5, 2.5);
  hist_pass_pteta  = fs->make<TH2F>("passpteta"     , "passed tracks: pt, eta; pt; eta; tracks"      , 200 ,0.,20, 50 ,-2.5, 2.5);
  hist_pass_chi2ndof  = fs->make<TH1F>("passchindof"     , "passed tracks: chi-2/Ndof; chi2/Ndof; tracks"     , 60 ,0.,30.);
  hist_pass_Nmatch  = fs->make<TH1F>("passNmatch"     , "passed tracks: number of matches; matched with #Delta R < 0.01; tracks"  , 5 ,-0.5,4.5);
 
  hist_nVtx  = fs->make<TH1F>("nVtx"     , "PU: number of vtx/Event; N; events"  , 100 ,-0.5,99.5);

  hist_pass_pass_PU1  = fs->make<TH1F>("passpassPU1"     , "passed tracks with < 10 vertices: Number of tracks matched to presel. tracks"      , 1 ,0.,1.);
  hist_pass_pass_PU2 = fs->make<TH1F>("passpassPU2"     , "passed tracks with 10 - 17 vertices: Number of tracks matched to presel. tracks"      , 1 ,0.,1.);  
  hist_pass_pass_PU3  = fs->make<TH1F>("passpassPU3"     , "passed trackswith 18 - 25  vertices: Number of tracks matched to presel. tracks"      , 1 ,0.,1.);
  hist_pass_pass_PU4  = fs->make<TH1F>("passpassPU4"     , "passed tracks with > 25 vertices: Number of tracks matched to presel. tracks"      , 1 ,0.,1.);
    
  //hist_pass_pt1_pt  = fs->make<TH1F>("passpt1pt"     , "passed tracks with p_{t} > 1000 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt2_pt  = fs->make<TH1F>("passpt2pt"     , "passed tracks with p_{t}(true) = 500 - 1000 GeV;1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt3_pt  = fs->make<TH1F>("passpt3pt"     , "passed tracks with p_{t}(true) = 500 - 400 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt4_pt  = fs->make<TH1F>("passpt4pt"     , "passed tracks with p_{t}(true): 400 - 200 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt5_pt  = fs->make<TH1F>("passpt5pt"     , "passed tracks with p_{t}(true): 200 - 10 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt6_pt  = fs->make<TH1F>("passpt6pt"     , "passed tracks with p_{t}(true): 10 - 2 GeV ; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt7_pt  = fs->make<TH1F>("passpt7pt"     , "passed tracks with p_{t}(true): 2 - 1 GeV; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  //hist_pass_pt8_pt  = fs->make<TH1F>("passpt8pt"     , "passed tracks with p_{t}(true): < 1 GeV; 1/p_{t}[GeV]; tracks"      , 200 ,0.,10.);
  
  //hist_pass_eta1_pt  = fs->make<TH1F>("passeta1pt"     , "passed tracks with #eta (true):-2.4 - -1.479 ;1/p_{t}[GeV]; tracks"     , 100 ,-2.5,-1.5);
  //hist_pass_eta2_pt  = fs->make<TH1F>("passeta2pt"     , "passed tracks with #eta (true): -1.479 - -0.8;1/p_{t}[GeV]; tracks"       , 100 ,-1.5,-0.5);
  //hist_pass_eta3_pt  = fs->make<TH1F>("passeta3pt"     , "passed tracks with #eta (true): -0.8 - 0;1/p_{t}[GeV]; tracks"       , 100 ,-1,0);
  //hist_pass_eta4_pt  = fs->make<TH1F>("passeta4pt"     , "passed tracks with #eta (true): 0 - 0.8;1/p_{t}[GeV]; tracks"       , 100 ,0.,1.);
  //hist_pass_eta5_pt  = fs->make<TH1F>("passeta5pt"     , "passed tracks with #eta (true): 0.8 - 1.479;1/p_{t}[GeV]; tracks"       , 100 ,0.5,1.5);
  //hist_pass_eta6_pt  = fs->make<TH1F>("passeta6pt"     , "passed tracks with #eta (true): 1.479 - 2.4;1/p_{t}[GeV]; tracks"       , 100 ,1.5,2.5);
  
  //hist_pass_phi1_pt  = fs->make<TH1F>("passphi1pt"     , "passed tracks with #phi (true): -#pi - - #pi / 2 ;1/p_{t}[GeV]; tracks"      , 100 ,M_PI,M_PI/2);
  //hist_pass_phi2_pt = fs->make<TH1F>("passphi2pt"     , "passed tracks with #phi (true): -#pi /2 - 0;1/p_{t}[GeV]; tracks"         , 100 ,M_PI/2,0.);
  //hist_pass_phi3_pt  = fs->make<TH1F>("passphi3pt"     , "passed tracks with #phi (true): 0 - #pi/2;1/p_{t}[GeV]; tracks"       , 100 ,0.,M_PI/2);
  //hist_pass_phi4_pt  = fs->make<TH1F>("passphi4pt"     , "passed tracks with #phi (true): #pi /2 - #pi;1/p_{t}[GeV]; tracks"       , 100 ,M_PI/2,M_PI);
  
  //hist_pass_PU1_n  = fs->make<TH1F>("passPU1n"     , "passed tracks with PU:; 1/p_{t}[GeV]; :;tracks"      , 100 ,0.,2.);
  //hist_pass_PU2_n  = fs->make<TH1F>("passPU2n"     , "passed tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,2.,4.);
  //hist_pass_PU3_n  = fs->make<TH1F>("passPU3n"     , "passed tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,4.,6.);
  //hist_pass_PU4_n  = fs->make<TH1F>("passPU4n"     , "passed tracks with PU:; 1/p_{t}[GeV]; ;tracks"      , 100 ,6.,100.); 
 
  hist_vtxRes_pt1  = fs->make<TH1F>("vtxRespt1pt"     , "passed tracks with p_{t} > 1000 GeV ; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt2  = fs->make<TH1F>("vtxRespt2pt"     , "passed tracks with p_{t}(true) = 500 - 1000 GeV;#Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt3  = fs->make<TH1F>("vtxRespt3pt"     , "passed tracks with p_{t}(true) = 500 - 400 GeV ; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt4  = fs->make<TH1F>("vtxRespt4pt"     , "passed tracks with p_{t}(true): 400 - 200 GeV ; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt5  = fs->make<TH1F>("vtxRespt5pt"     , "passed tracks with p_{t}(true): 200 - 10 GeV ; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt6  = fs->make<TH1F>("vtxRespt6pt"     , "passed tracks with p_{t}(true): 10 - 2 GeV ; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt7  = fs->make<TH1F>("vtxRespt7pt"     , "passed tracks with p_{t}(true): 2 - 1 GeV; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_pt8  = fs->make<TH1F>("vtxRespt8pt"     , "passed tracks with p_{t}(true): < 1 GeV; #Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  
  hist_vtxRes_eta1  = fs->make<TH1F>("vtxReseta1pt"     , "passed tracks with #eta (true):-2.4 - -1.479 ;#Delta z_{vxt}; tracks"     , 2000,-0.5,0.5);
  hist_vtxRes_eta2  = fs->make<TH1F>("vtxReseta2pt"     , "passed tracks with #eta (true): -1.479 - -0.8;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxRes_eta3  = fs->make<TH1F>("vtxReseta3pt"     , "passed tracks with #eta (true): -0.8 - 0;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxRes_eta4  = fs->make<TH1F>("vtxReseta4pt"     , "passed tracks with #eta (true): 0 - 0.8;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxRes_eta5  = fs->make<TH1F>("vtxReseta5pt"     , "passed tracks with #eta (true): 0.8 - 1.479;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxRes_eta6  = fs->make<TH1F>("vtxReseta6pt"     , "passed tracks with #eta (true): 1.479 - 2.4;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);
  
  hist_vtxRes_phi1  = fs->make<TH1F>("vtxResphi1pt"     , "passed tracks with #phi (true): -#pi - - #pi / 2 ;#Delta z_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxRes_phi2 = fs->make<TH1F>("vtxResphi2pt"     , "passed tracks with #phi (true): -#pi /2 - 0;#Delta z_{vxt}; tracks"         , 2000,-0.5,0.5);
  hist_vtxRes_phi3  = fs->make<TH1F>("vtxResphi3pt"     , "passed tracks with #phi (true): 0 - #pi/2;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxRes_phi4 = fs->make<TH1F>("vtxResphi4pt"     , "passed tracks with #phi (true): #pi /2 - #pi;#Delta z_{vxt}; tracks"       , 2000,-0.5,0.5);

  hist_vtxRes  = fs->make<TH1F>("vtxRes"     , "vertex Resolution: (true - reRECO); #Delta z_{vertex}; tracks"  , 2000,-0.5,0.5);

  hist_vtxResY_pt1  = fs->make<TH1F>("vtxResY_pt1pt"     , "passed tracks with p_{t} > 1000 GeV ; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt2  = fs->make<TH1F>("vtxResY_pt2pt"     , "passed tracks with p_{t}(true) = 500 - 1000 GeV;#Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt3  = fs->make<TH1F>("vtxResY_pt3pt"     , "passed tracks with p_{t}(true) = 500 - 400 GeV ; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt4  = fs->make<TH1F>("vtxResY_pt4pt"     , "passed tracks with p_{t}(true): 400 - 200 GeV ; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt5  = fs->make<TH1F>("vtxResY_pt5pt"     , "passed tracks with p_{t}(true): 200 - 10 GeV ; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt6  = fs->make<TH1F>("vtxResY_pt6pt"     , "passed tracks with p_{t}(true): 10 - 2 GeV ; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt7  = fs->make<TH1F>("vtxResY_pt7pt"     , "passed tracks with p_{t}(true): 2 - 1 GeV; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_pt8  = fs->make<TH1F>("vtxResY_pt8pt"     , "passed tracks with p_{t}(true): < 1 GeV; #Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  
  hist_vtxResY_eta1  = fs->make<TH1F>("vtxResY_eta1pt"     , "passed tracks with #eta (true):-2.4 - -1.479 ;#Delta y_{vxt}; tracks"     , 2000,-0.5,0.5);
  hist_vtxResY_eta2  = fs->make<TH1F>("vtxResY_eta2pt"     , "passed tracks with #eta (true): -1.479 - -0.8;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResY_eta3  = fs->make<TH1F>("vtxResY_eta3pt"     , "passed tracks with #eta (true): -0.8 - 0;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResY_eta4  = fs->make<TH1F>("vtxResY_eta4pt"     , "passed tracks with #eta (true): 0 - 0.8;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResY_eta5  = fs->make<TH1F>("vtxResY_eta5pt"     , "passed tracks with #eta (true): 0.8 - 1.479;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResY_eta6  = fs->make<TH1F>("vtxResY_eta6pt"     , "passed tracks with #eta (true): 1.479 - 2.4;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);
  
  hist_vtxResY_phi1  = fs->make<TH1F>("vtxResY_phi1pt"     , "passed tracks with #phi (true): -#pi - - #pi / 2 ;#Delta y_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResY_phi2 = fs->make<TH1F>("vtxResY_phi2pt"     , "passed tracks with #phi (true): -#pi /2 - 0;#Delta y_{vxt}; tracks"         , 2000,-0.5,0.5);
  hist_vtxResY_phi3  = fs->make<TH1F>("vtxResY_phi3pt"     , "passed tracks with #phi (true): 0 - #pi/2;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResY_phi4 = fs->make<TH1F>("vtxResY_phi4pt"     , "passed tracks with #phi (true): #pi /2 - #pi;#Delta y_{vxt}; tracks"       , 2000,-0.5,0.5);

  hist_vtxResX_pt1  = fs->make<TH1F>("vtxResX_pt1pt"     , "passed tracks with p_{t} > 1000 GeV ; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt2  = fs->make<TH1F>("vtxResX_pt2pt"     , "passed tracks with p_{t}(true) = 500 - 1000 GeV;#Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt3  = fs->make<TH1F>("vtxResX_pt3pt"     , "passed tracks with p_{t}(true) = 500 - 400 GeV ; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt4  = fs->make<TH1F>("vtxResX_pt4pt"     , "passed tracks with p_{t}(true): 400 - 200 GeV ; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt5  = fs->make<TH1F>("vtxResX_pt5pt"     , "passed tracks with p_{t}(true): 200 - 10 GeV ; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt6  = fs->make<TH1F>("vtxResX_pt6pt"     , "passed tracks with p_{t}(true): 10 - 2 GeV ; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt7  = fs->make<TH1F>("vtxResX_pt7pt"     , "passed tracks with p_{t}(true): 2 - 1 GeV; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_pt8  = fs->make<TH1F>("vtxResX_pt8pt"     , "passed tracks with p_{t}(true): < 1 GeV; #Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  
  hist_vtxResX_eta1  = fs->make<TH1F>("vtxResX_eta1pt"     , "passed tracks with #eta (true):-2.4 - -1.479 ;#Delta x_{vxt}; tracks"     , 2000,-0.5,0.5);
  hist_vtxResX_eta2  = fs->make<TH1F>("vtxResX_eta2pt"     , "passed tracks with #eta (true): -1.479 - -0.8;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResX_eta3  = fs->make<TH1F>("vtxResX_eta3pt"     , "passed tracks with #eta (true): -0.8 - 0;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResX_eta4  = fs->make<TH1F>("vtxResX_eta4pt"     , "passed tracks with #eta (true): 0 - 0.8;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResX_eta5  = fs->make<TH1F>("vtxResX_eta5pt"     , "passed tracks with #eta (true): 0.8 - 1.479;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResX_eta6  = fs->make<TH1F>("vtxResX_eta6pt"     , "passed tracks with #eta (true): 1.479 - 2.4;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
  
  hist_vtxResX_phi1  = fs->make<TH1F>("vtxResX_phi1pt"     , "passed tracks with #phi (true): -#pi - - #pi / 2 ;#Delta x_{vxt}; tracks"      , 2000,-0.5,0.5);
  hist_vtxResX_phi2 = fs->make<TH1F>("vtxResX_phi2pt"     , "passed tracks with #phi (true): -#pi /2 - 0;#Delta x_{vxt}; tracks"         , 2000,-0.5,0.5);
  hist_vtxResX_phi3  = fs->make<TH1F>("vtxResX_phi3pt"     , "passed tracks with #phi (true): 0 - #pi/2;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
  hist_vtxResX_phi4 = fs->make<TH1F>("vtxResX_phi4pt"     , "passed tracks with #phi (true): #pi /2 - #pi;#Delta x_{vxt}; tracks"       , 2000,-0.5,0.5);
   
  hist_ptRes_pt1  = fs->make<TH1F>("ptRespt1pt"     , "passed tracks with p_{t} > 1000 GeV ; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt2  = fs->make<TH1F>("ptRespt2pt"     , "passed tracks with p_{t}(true) = 500 - 1000 GeV;#Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt3  = fs->make<TH1F>("ptRespt3pt"     , "passed tracks with p_{t}(true) = 500 - 400 GeV ; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt4  = fs->make<TH1F>("ptRespt4pt"     , "passed tracks with p_{t}(true): 400 - 200 GeV ; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt5  = fs->make<TH1F>("ptRespt5pt"     , "passed tracks with p_{t}(true): 200 - 10 GeV ; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt6  = fs->make<TH1F>("ptRespt6pt"     , "passed tracks with p_{t}(true): 10 - 2 GeV ; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt7  = fs->make<TH1F>("ptRespt7pt"     , "passed tracks with p_{t}(true): 2 - 1 GeV; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_pt8  = fs->make<TH1F>("ptRespt8pt"     , "passed tracks with p_{t}(true): < 1 GeV; #Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  
  hist_ptRes_eta1  = fs->make<TH1F>("ptReseta1pt"     , "passed tracks with #eta (true):-2.4 - -1.479 ;#Delta 1/p_{t}; tracks"     , 2000,-0.5,0.5);
  hist_ptRes_eta2  = fs->make<TH1F>("ptReseta2pt"     , "passed tracks with #eta (true): -1.479 - -0.8;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);
  hist_ptRes_eta3  = fs->make<TH1F>("ptReseta3pt"     , "passed tracks with #eta (true): -0.8 - 0;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);
  hist_ptRes_eta4  = fs->make<TH1F>("ptReseta4pt"     , "passed tracks with #eta (true): 0 - 0.8;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);
  hist_ptRes_eta5  = fs->make<TH1F>("ptReseta5pt"     , "passed tracks with #eta (true): 0.8 - 1.479;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);
  hist_ptRes_eta6  = fs->make<TH1F>("ptReseta6pt"     , "passed tracks with #eta (true): 1.479 - 2.4;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);
  
  hist_ptRes_phi1  = fs->make<TH1F>("ptResphi1pt"     , "passed tracks with #phi (true): -#pi - - #pi / 2 ;#Delta 1/p_{t}; tracks"      , 2000,-0.5,0.5);
  hist_ptRes_phi2 = fs->make<TH1F>("ptResphi2pt"     , "passed tracks with #phi (true): -#pi /2 - 0;#Delta 1/p_{t}; tracks"         , 2000,-0.5,0.5);
  hist_ptRes_phi3  = fs->make<TH1F>("ptResphi3pt"     , "passed tracks with #phi (true): 0 - #pi/2;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);
  hist_ptRes_phi4 = fs->make<TH1F>("ptResphi4pt"     , "passed tracks with #phi (true): #pi /2 - #pi;#Delta 1/p_{t}; tracks"       , 2000,-0.5,0.5);  
  
  hist_ptRes  = fs->make<TH1F>("ptRes"     , "pt Resolution (true - reRECO); 1/pt(true) - 1/pt(pass); tracks"  , 2000,-0.5,0.5);
  
  if(trackingOn){  
  hist_td_chi2ndof  = fs->make<TH1F>("tdchi2"     , "tracking details: chi2/ndof; chi2/ndof; tracks"      , 60 ,0.,30.);
  hist_td_layersWithout  = fs->make<TH1F>("tdlayersWithout"     , "tracking details: trackLayersWithoutMeasurement; layers; tracks"      , 30 ,0.,30.);
  hist_td_layersWith  = fs->make<TH1F>("tdlayersWith"     , "tracking details: trackerLayersWithMeasurement; layers; tracks"      , 30 ,0.,30.);
  hist_td_algos  = fs->make<TH1F>("tdalgos"     , "tracking details: tracking algo;   duplicateMerge:-1 initialStep:0 lowPtTripletStep:1 pixelPairStep:2 detachedTripletStep:3 mixedTripletStep:4 pixelLessStep:5 tobTecStep:6 muonSeededStepInOut:7; tracks"      , 8 ,-1.,7.);
  hist_td_lostHits  = fs->make<TH1F>("tdlostHits"     , "tracking details: N lost hits;   hits; tracks"      , 10 ,0.,10.);
  hist_td_validHits  = fs->make<TH1F>("tdvalidHits"     , "tracking details: N valid Hits;   hits; tracks"      , 35 ,0.,35.);
  hist_td_validFrac  = fs->make<TH1F>("tdvalidFrac"     , "tracking details: fract. of valid hits;   fract. of hits; tracks"      , 10,0.,1.);
  hist_td_d0  = fs->make<TH1F>("tdd0"     , "tracking details: d0;   d0; tracks"      , 500 ,0.,5.);
  hist_td_dsz  = fs->make<TH1F>("tddsz"     , "tracking details: dsz;   dsz; tracks"      , 35 ,0.,10.);
  hist_td_dz  = fs->make<TH1F>("tddz"     , "tracking details: dz;   dz; tracks"      , 35 ,0.,10.);
  hist_td_iso  = fs->make<TH1F>("tdiso"     , "tracking details: Minimum DeltaR between tracks;   dR; tracks"      , 100 ,0.,1.);
  }
  
  hist_muTrack_pt   = fs->make<TH1F>("muTrackpt"     , "muonTrack 1/pt;1/pt[GeV];muonTracks"      , 50 , 0., 10.);
  hist_muTrack_eta  = fs->make<TH1F>("muTracketa"     , "muonTrack eta;eta;muonsTracks"      , 50 ,-2.5, 2.5);
  hist_muTrack_n  = fs->make<TH1F>("muTrackn"     , "number of muonTracks"      , 1 ,0.,1.);

  hist_sClus_n  = fs->make<TH1F>("sClusn"     , "number of Strip Cluster"      , 1 ,0.,1.);
  hist_sClus_q  = fs->make<TH1F>("sClusq"     , "cluster details: strip cluster charge; charge[];cluster"      , 100 ,0.,1000.);

  hist_pClus_n  = fs->make<TH1F>("pClusn"     , "number of Pixel Cluster"      , 1 ,0.,1.);
  hist_pClus_q  = fs->make<TH1F>("pClusq"     , "cluster details: pixel cluster charge; charge[];cluster"      , 1000 ,0.,100000.);
  hist_pClus_size  = fs->make<TH1F>("pClusqsize"     , "cluster details: pixel cluster size; size;cluster"      , 20 ,0.,20.);
  
}

// ------------ method called once each job just after ending the event loop  ------------                                                                                                                     
void
MyMonitoringAnalyzer::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------                                                                                                           
void
MyMonitoringAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  desc.setUnknown();
  descriptions.addDefault(desc);

  //desc.add<edm::InputTag>("muons")->setComment("input muon collection");
  //desc.add<edm::InputTag>("electrons")->setComment("input electron collection");
  //desc.add<edm::InputTag>("muonTracks")->setComment("input muon track collection");
  //desc.add<edm::InputTag>("pixelCluster")->setComment("input pixel cluster collection");
  //desc.add<edm::InputTag>("stripCluster")->setComment("input strip cluster collection");
  //desc.add<edm::InputTag>("tracks")->setComment("input general tracks collection");
  //desc.add<bool>("debug")->setComment("debugging?");
  //desc.add<bool>("trackingDetails")->setComment("trackingDetails?");
  //descriptions.addDefault(desc);
}

//define this as a plug-in                                                                                                                                                                                     
DEFINE_FWK_MODULE(MyMonitoringAnalyzer);
