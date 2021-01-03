// Original Author:  Viktor Gerhard Kutzner
//         Created:  Sun, 03 Jan 2021 19:15:47 GMT

#include <memory>
#include <stdio.h>
#include <stdlib.h>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "DataFormats/MuonReco/interface/Muon.h"


class GoodRecoMuonsFilter : public edm::stream::EDFilter<> {
   public:
      explicit GoodRecoMuonsFilter(const edm::ParameterSet&);
      ~GoodRecoMuonsFilter();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginStream(edm::StreamID) override;
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      virtual void endStream() override;

      edm::EDGetTokenT<std::vector<reco::Muon>> muonsToken; 
      float minpt_;
      float maxabseta_;
};

GoodRecoMuonsFilter::GoodRecoMuonsFilter(const edm::ParameterSet& iConfig)
{
    muonsToken = consumes<std::vector<reco::Muon>>(iConfig.getParameter<edm::InputTag>("muonlabel"));
    minpt_     = iConfig.getParameter<double>("minPt");
    maxabseta_ = iConfig.getParameter<double>("maxAbsEta");
}


GoodRecoMuonsFilter::~GoodRecoMuonsFilter()
{
}


bool
GoodRecoMuonsFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   Handle<std::vector<reco::Muon>> muons;
   iEvent.getByToken( muonsToken, muons);
      
   bool result = false;
   for( const auto& muon : *muons){
       if ((muon.pt() > minpt_) && (abs(muon.eta()) < maxabseta_)) {
	   	   result = true;
		   break;
	   }
   }
   
   return result;
}

void
GoodRecoMuonsFilter::beginStream(edm::StreamID)
{
}

void
GoodRecoMuonsFilter::endStream() {
}

void
GoodRecoMuonsFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
DEFINE_FWK_MODULE(GoodRecoMuonsFilter);
