//
// Original Author:  Alexandra Tews
//
// This producer makes a preselection of quality tracks.
// It then loops over the selected track collection
// and retrieves the Rechits for each track.
// RecHIts can be linked to clusters that are identified via the rawId  
// and their position in the vector container DetSetVector<>. 
// The output DetSetVector holds all but some selected cluster.
// The Number of hits (cluster) to remain for each quality track can be specified. 
//
// Created: 13.07.17
//
// 
//

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <TLorentzVector.h>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
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
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/TrackerRecHit2D/interface/BaseTrackerRecHit.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/Records/interface/TrackerTopologyRcd.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

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
#include<limits>

class RClusterProducer : public edm::stream::EDProducer<> {
   public:
      explicit RClusterProducer(const edm::ParameterSet&);
      ~RClusterProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginStream(edm::StreamID) override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endStream() override;


      edm::EDGetTokenT<std::vector<reco::Track>> tracksToken;
      edm::EDGetTokenT<std::vector<reco::GsfElectron>> electronsToken;
      edm::EDGetTokenT<std::vector<reco::Muon>> muonsToken; 
      edm::EDGetTokenT<edm::OwnVector<TrackingRecHit,edm::ClonePolicy<TrackingRecHit>>> generalTracksHitsToken;
      edm::EDGetTokenT<edmNew::DetSetVector<SiStripCluster>> oldStripClusterToken;
      edm::EDGetTokenT<edmNew::DetSetVector<SiPixelCluster>> oldPixelClusterToken;
      edm::EDGetTokenT<reco::VertexCollection> PrimVtxToken; 
      
      //int minNumberOfHits;                                      
      int minNumberOfLayers;                                      
      //unsigned int hitsRemaining;
      unsigned int layersRemaining;
      double_t matchInDr;
      bool onlyValidHits;
      bool debug;
      std::string matchTo;
      

};


RClusterProducer::RClusterProducer(const edm::ParameterSet& iConfig)
{
   produces<edmNew::DetSetVector<SiPixelCluster>>("").setBranchAlias("");
   produces<edmNew::DetSetVector<SiStripCluster>>("").setBranchAlias(""); 
   produces<reco::TrackCollection>("").setBranchAlias(""); 
   
   tracksToken = consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("allTracks"));
   electronsToken = consumes<std::vector<reco::GsfElectron>>(iConfig.getParameter<edm::InputTag>("matchElectrons"));
   muonsToken = consumes<std::vector<reco::Muon>>(iConfig.getParameter<edm::InputTag>("matchMuons"));
   oldStripClusterToken = consumes<edmNew::DetSetVector<SiStripCluster>>(iConfig.getParameter<edm::InputTag>("selectedStripCluster"));   
   oldPixelClusterToken = consumes<edmNew::DetSetVector<SiPixelCluster>>(iConfig.getParameter<edm::InputTag>("selectedPixelCluster"));   
   PrimVtxToken = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("PrimaryVertex"));
   
   minNumberOfLayers = iConfig.getParameter<int>("minNumberOfLayers");   
   layersRemaining = iConfig.getParameter<unsigned int>("layersRemaining");
   matchInDr = iConfig.getParameter<double_t>("requiredDr");
   onlyValidHits = iConfig.getParameter<bool>("onlyValidHits");
   debug = iConfig.getParameter<bool>("debug");
   matchTo = iConfig.getParameter<std::string>("matchTo");
}


RClusterProducer::~RClusterProducer()
{}


void
RClusterProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
  
   // register input collections:
   Handle<reco::TrackCollection> tracks;
   iEvent.getByToken(tracksToken, tracks);
   
   Handle<std::vector<reco::GsfElectron>> electrons; 
   iEvent.getByToken( electronsToken, electrons);
   
   Handle<std::vector<reco::Muon>> muons;
   iEvent.getByToken( muonsToken, muons);
   
   Handle<edmNew::DetSetVector<SiStripCluster>> oldStripCluster;
   iEvent.getByToken(oldStripClusterToken, oldStripCluster);
   
   Handle<edmNew::DetSetVector<SiPixelCluster>> oldPixelCluster;
   iEvent.getByToken(oldPixelClusterToken, oldPixelCluster);
   
   Handle<reco::VertexCollection> vtx_h;
   iEvent.getByToken(PrimVtxToken, vtx_h);
   const reco::Vertex vtx = vtx_h->at(0);
  
   // register output collection:

   std::unique_ptr <edmNew::DetSetVector<SiStripCluster>> outStrips (new edmNew::DetSetVector<SiStripCluster>);
   std::unique_ptr <edmNew::DetSetVector<SiPixelCluster>> outPixel (new edmNew::DetSetVector<SiPixelCluster>);
   std::unique_ptr<reco::TrackCollection> goodTracks(new reco::TrackCollection);

   // Preselection of long quality tracks
   
    std::vector<reco::Track> selTracks;
    reco::Track bestTrack; 
    const std::vector<reco::GsfElectron> *es = electrons.product();
	const std::vector<reco::Muon> *ms = muons.product();
	unsigned int tMuon	=0;
	Double_t fitProb = 100;
	unsigned int candidates = 0;
	double maxDxy = 0.02;
   double maxDz = 0.5;
	
	//std::cout << "candidate tracks: " << candidates << std::endl;
    
    for( const auto& track : *tracks){
		
		reco::HitPattern hitpattern = track.hitPattern();
		bool passedMinNumberLayers = false;
		bool isMatched = false;
		Double_t  dRmin = 10;
		Double_t chiNdof = track.normalizedChi2();
		Double_t dxy = std::abs(track.dxy(vtx.position()));
		Double_t dz = std::abs(track.dz(vtx.position()));
						
		if (hitpattern.trackerLayersWithMeasurement() >= minNumberOfLayers) passedMinNumberLayers = true;
		 
		TLorentzVector pTrack (track.px(), track.py(), track.pz(), track.pt());
				
		if (matchTo=="Electron"){
			for( const auto& e : *electrons){
				if (e.trackerDrivenSeed()&&(e.classification()!=2)&&(!e.ambiguous())){
					try {  
					//reco::Track matchedTrack = *(e.closestTrack());
				    reco::Track matchedTrack = *(e.bestTrack());
					TLorentzVector pMatched (matchedTrack.px(), matchedTrack.py(), matchedTrack.pz(), matchedTrack.pt());
					// match to general track in deltaR            
					Double_t dr = pTrack.DeltaR(pMatched);
					if (dr < dRmin) dRmin = dr;  
					}  
					catch(...) {   
				    if (debug) std::cout << "no track for e" << std::endl;
					}	
				}
			}
		}					
		 
		if (matchTo=="Muon"){
			for( const auto& m : *muons){
				if (m.isTrackerMuon()){
					tMuon++;
					reco::Track matchedTrack = *(m.innerTrack());
					TLorentzVector pMatched (matchedTrack.px(), matchedTrack.py(),matchedTrack.pz(), matchedTrack.pt());
					// match to general track in deltaR            
					Double_t dr = pTrack.DeltaR(pMatched);
					if (dr < dRmin) dRmin = dr;				
				}
			}								
		 }
		 
		if (dRmin<matchInDr) isMatched = true;
		// do vertex consistency:
		bool vertex_match = std::abs(track.dxy(vtx.position())) < maxDxy && std::abs(track.dz(vtx.position())) < maxDz;
		if (!(vertex_match)) continue;
		if (!(track.validFraction()==1)) continue;
		if (passedMinNumberLayers&&isMatched){
			//std::cout << "found match! " << std::endl;
			candidates ++;
			if (chiNdof < fitProb){
				std::cout << " dxy: " << dxy << " dz : " << dz << std::endl;
				fitProb = chiNdof;
				bestTrack = track;
				bestTrack.setExtra(track.extra());
				//selTracks.at(counter) = track;
			}				 
			if(debug) std::cout << " deltaR (general) track to matched Track: " << dRmin << std::endl;
			if(debug) std::cout << "chi2Ndof:" << chiNdof << " best Track: " << fitProb << std::endl;

		}

	}
	selTracks.push_back(bestTrack);
	
	//std::cout << "candidates: " << candidates << std::endl;
		
	if (debug) std::cout << " number of Tracker Muons: " << tMuon << ", thereof " << selTracks.size() << " tracks passed preselection." << std::endl;
	//std::cout << " number of Tracker Muons: " << tMuon << ", thereof " << selTracks.size() << " tracks passed preselection." << std::endl;
    
   // shorten preselected tracks
   
   std::set<unsigned int> stripIds;
   std::set<unsigned int> pixelIds;

   int tracksCounter = 0; 
   for( const auto& track : selTracks){
	   
	   //std::cout << "looping through selTracks..." << std::endl;   
	   //goodTracks->push_back(track);
       reco::HitPattern hitpattern = track.hitPattern();
       uint32_t thisLayer;
       uint32_t prevLayer;
       uint32_t thisSubStruct;
       uint32_t prevSubStruct;
       unsigned int sequLayers = 0;
	   int pxbLayers =0;
	   int pxfLayers =0;
	   int tibLayers =0;
	   int tidLayers =0;
	   int tobLayers =0;
	   int tecLayers =0;
       //std::cout << "retrieved hit pattern " << std::endl;	    
	   tracksCounter ++;
	   try{
			auto hb = track.recHitsBegin();
			//std::cout << " got first recHit. RecHitsSize: " << track.recHitsSize() << std::endl;

	   //for(unsigned int h=0;h<track.recHitsSize();h++){

				//uint32_t pHit = hitpattern.getHitPattern(reco::HitPattern::TRACK_HITS, h);
				//uint32_t nHit = hitpattern.getHitPattern(reco::HitPattern::TRACK_HITS, h+1);
				

		//}
	   for(unsigned int h=0;h<track.recHitsSize();h++){
		   
				uint32_t pHit = hitpattern.getHitPattern(reco::HitPattern::TRACK_HITS, h);
				uint32_t nHit = hitpattern.getHitPattern(reco::HitPattern::TRACK_HITS, h-1);
				
				   //  A consecutive sequence of hit layers can be obtained from the hit pattern summing all hit disks/wheels/layers per substructure 
   //  ignoring layers that are hit several times.		
   //                                            uint16_t
   // +--------+---------------+---------------------------+-----------------+----------------+
   // |  tk/mu | sub-structure |     sub-sub-structure     |     stereo      |    hit type    |
   // +--------+---------------+---------------------------+-----------------+----------------+
   // |   10   | 9   8    7    |  6     5     4     3      |        2        |    1        0  |  bit
   // +--------+---------------+---------------------------+-----------------+----------------|
   // | tk = 1 |    PXB = 1    | layer = 1-3               |                 | hit type = 0-3 |
   // | tk = 1 |    PXF = 2    | disk  = 1-2               |                 | hit type = 0-3 |
   // | tk = 1 |    TIB = 3    | layer = 1-4               | 0=rphi,1=stereo | hit type = 0-3 |
   // | tk = 1 |    TID = 4    | wheel = 1-3               | 0=rphi,1=stereo | hit type = 0-3 |
   // | tk = 1 |    TOB = 5    | layer = 1-6               | 0=rphi,1=stereo | hit type = 0-3 |
   // | tk = 1 |    TEC = 6    | wheel = 1-9               | 0=rphi,1=stereo | hit type = 0-3 |
   // | mu = 0 |    DT  = 1    | 4*(stat-1)+superlayer     |                 | hit type = 0-3 |
   // | mu = 0 |    CSC = 2    | 4*(stat-1)+(ring-1)       |                 | hit type = 0-3 |
   // | mu = 0 |    RPC = 3    | 4*(stat-1)+2*layer+region |                 | hit type = 0-3 |
   // | mu = 0 |    GEM = 4    | 2*(stat-1)+2*(layer-1)    |                 | hit type = 0-3 |
   // |mu = 0  |    ME0 = 5    | roll                      |                 | hit type = 0-3 |
   // +--------+---------------+---------------------------+-----------------+----------------+
   //		   
				if (debug) std::cout << "this hit: " << h << "trackerpart:" << hitpattern.getSubStructure(pHit) << " layer/disk/wheel : " << hitpattern.getLayer(pHit) <<std::endl;	
				if (debug) std::cout << "next hit: " << h+1 << "trackerpart:" << hitpattern.getSubStructure(nHit) << " layer/disk/wheel : " << hitpattern.getLayer(nHit) <<std::endl;	
				
				// define a sequence of hit layers:
				thisLayer =  hitpattern.getLayer(pHit);
				prevLayer =  hitpattern.getLayer(nHit);
				thisSubStruct =  hitpattern.getSubStructure(pHit);
				prevSubStruct =  hitpattern.getSubStructure(nHit);
				if (hitpattern.getSubStructure(pHit)==1 && !((thisLayer==prevLayer)&&(thisSubStruct==prevSubStruct))){
					pxbLayers ++;
				}
				if (hitpattern.getSubStructure(pHit)==2 && !((thisLayer==prevLayer)&&(thisSubStruct==prevSubStruct))){
					pxfLayers ++;
				}
				if (hitpattern.getSubStructure(pHit)==3 && !((thisLayer==prevLayer)&&(thisSubStruct==prevSubStruct))){
					tibLayers ++;
				}
				if (hitpattern.getSubStructure(pHit)==4 && !((thisLayer==prevLayer)&&(thisSubStruct==prevSubStruct))){
					tidLayers ++;
				}
				if (hitpattern.getSubStructure(pHit)==5 && !((thisLayer==prevLayer)&&(thisSubStruct==prevSubStruct))){
					tobLayers ++;
				}
				if (hitpattern.getSubStructure(pHit)==6 && !((thisLayer==prevLayer)&&(thisSubStruct==prevSubStruct))){
					tecLayers ++;
				}
				
			    sequLayers = pxbLayers+pxfLayers+tibLayers+tidLayers+tobLayers+tecLayers;
	            if (debug) std::cout << sequLayers << " : " << pxbLayers << " "<< pxfLayers << " "<< tibLayers << " "<< tidLayers << " "<< tobLayers << " "<< tecLayers <<std::endl;
	            std::cout << sequLayers << " : " << pxbLayers << " "<< pxfLayers << " "<< tibLayers << " "<< tidLayers << " "<< tobLayers << " "<< tecLayers <<std::endl;
				std::cout << "this hit: " << h << " trackerpart: " << hitpattern.getSubStructure(pHit) << " layer/disk/wheel : " << hitpattern.getLayer(pHit) <<" layer in sequence: " << sequLayers <<std::endl;								
				auto recHit = *(hb+h);
				auto const & hit = *recHit;
				unsigned int rawId = 0;
	
				if (onlyValidHits && !hit.isValid()){
					if(debug) std::cout<< "hit not valid: " << h <<std::endl;
					continue;
				}
				
				auto const & rhit = reinterpret_cast<BaseTrackerRecHit const&>(hit);
				auto const & rcluster = rhit.firstClusterRef();
				rawId = ((rhit.geographicalId()).rawId());
				// loop over the hits of the track. 
				if (onlyValidHits && !(hitpattern.validHitFilter(pHit))){
					if(debug) std::cout<< "hit not valid: " << h <<std::endl;
					continue;
				}
				if (debug) std::cout << "thisLayer : " << thisLayer << " prevLayer: " << prevLayer << " hit layer nr.:" << sequLayers << std::endl;					
				if (sequLayers > layersRemaining) {
								
					std::cout << "will remove hit: " << h << " trackerpart: " << hitpattern.getSubStructure(pHit) << " layer/disk/wheel : " << hitpattern.getLayer(pHit) << " layer in sequence: " << sequLayers <<std::endl;		
					if (rcluster.isStrip()){	
						if (std::find(stripIds.begin(), stripIds.end(), rawId) != stripIds.end()){
							if(debug) std::cout << "STRIP hit: " << h << " Id already in set: " << rawId << std::endl;
							continue;
						}							
						else {
							stripIds.insert(rawId); // ids to remove								
						}
					}
						
					if (rcluster.isPixel()){	
						if (std::find(pixelIds.begin(), pixelIds.end(), rawId) != pixelIds.end()){
							if (debug) std::cout << "PIXEL hit: " << h << " Id in set: " << rawId << std::endl;
							continue;
						}
						else {
							pixelIds.insert(rawId); // ids to remove 	
						}
					}					
				}		
		}
		goodTracks->push_back(track);
		}
		catch(...){
		std::cout << "de-referenced track extra" << std::endl;
		}       
	}
	
	if(debug) std::cout << "pixel Ids to remove: " << pixelIds.size() << " strip Ids to be removed: " << stripIds.size() << std::endl;
	
	for(unsigned int h=0;h<((oldStripCluster.product())->size());h++){
		
		unsigned int id = (oldStripCluster.product()->id(h));
		auto pos = ((oldStripCluster.product())->find(id)) - ((oldStripCluster.product())->begin());
		unsigned int sizetype = ((oldStripCluster.product())->detsetSize(pos));
		auto const datatype = 	((oldStripCluster.product())->data(pos));
		
		if (std::find(stripIds.begin(), stripIds.end(), id) != stripIds.end()){
		// found raw Id in list of Ids to remove
		// 
		}
		else {
			outStrips->insert(id,datatype,sizetype);
			if(debug &&(h%1000==0)) std::cout << " STRIP cluster: " << h << " inserted " << id << " , " << pos << " , " << sizetype << " to set with all ids, positions, sizes." << std::endl;

		}
		
	}	
	for(unsigned int h=0;h<((oldPixelCluster.product())->size());h++){
		
		unsigned int id = (oldPixelCluster.product()->id(h));
		auto pos = ((oldPixelCluster.product())->find(id)) - ((oldPixelCluster.product())->begin());
		unsigned int sizetype = ((oldPixelCluster.product())->detsetSize(pos));
		auto const datatype = 	((oldPixelCluster.product())->data(pos));
		
		if (std::find(pixelIds.begin(), pixelIds.end(), id) != pixelIds.end()){
		// found raw Id in list of Ids to remove
		}
		else {
			outPixel->insert(id,datatype,sizetype);
			if(debug && (h%100==0)) std::cout << " PIXEL cluster: " << h << " inserted " << id << " , " << pos << " , " << sizetype << " to set with all ids, positions, sizes." << std::endl;

		}
		
	}									
							
 
   // save track collection in event:
   iEvent.put(std::move(outStrips), "");
   iEvent.put(std::move(outPixel), "");
   iEvent.put(std::move(goodTracks), "");

}

void
RClusterProducer::beginStream(edm::StreamID)
{}

void
RClusterProducer::endStream() {
}


void
RClusterProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(RClusterProducer);
