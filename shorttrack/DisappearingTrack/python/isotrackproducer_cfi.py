import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
# adds isolated track properties

options = VarParsing('analysis')
options.parseArguments()

process = cms.Process("ISOTRACK")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options  = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')

process.isotrackproducer = cms.EDProducer("IsoTrackProducer",
                                    selectedTracks = cms.InputTag("generalTracks"),
                                    selectedElectrons = cms.InputTag("gedGsfElectrons"),
                                    selectedMuons = cms.InputTag("muons"),
                                    selectedPFJets = cms.InputTag("ak4PFJetsCHS"),
                                    selectedPFCand = cms.InputTag("particleFlow"),
                                    minTrackPt = cms.double(15),
                                    maxTrackEta = cms.double(2.4),
                                    coneRelIsoDR = cms.double(0.3),
                                    conePtSumMaxPtFraction = cms.double(0.05),
                                    minTrackJetDR = cms.double(0.5),
                                    minTrackLeptonDR = cms.double(0.15),
                                    RequireNumberOfValidPixelHits = cms.int32(1),
                                    RequireNumberOfValidTrackerHits = cms.int32(7),
                                    maxDxy = cms.double(0.02),
                                    maxDz = cms.double(0.5),
                                    selectedEcalRecHitsEB = cms.InputTag("reducedEcalRecHitsEB"),
                                    selectedEcalRecHitsEE = cms.InputTag("reducedEcalRecHitsEE"),
                                    selectedEcalRecHitsES = cms.InputTag("reducedEcalRecHitsES"),
                                    selectedHcalRecHits = cms.InputTag("reducedHcalRecHits"),
                                    selectedCaloJets = cms.InputTag("ak4CaloJets"),
                                    useCaloJetsInsteadOfHits = cms.bool(False),
                                    minMissingOuterHits = cms.int32(3),
                                    caloEnergyDepositionMaxDR = cms.double(0.5),
                                    caloEnergyDepositionMaxE = cms.double(10),
                                    deadNoisyDR = cms.double(0.05),
                                    dEdxEstimator = cms.string('dedxHarmonic2'),
                                    doDeDx = cms.bool(True),
                                    PrimaryVertex = cms.InputTag('offlinePrimaryVertices'),
                                    maxChargedPFCandSumDR = cms.double(0.01),
                                    maxNeutralPFCandSumDR = cms.double(0.05),
                                    )
                                    
process.out = cms.OutputModule("PoolOutputModule", 
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = cms.untracked.vstring(
        'keep *',
        ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
 )

process.p = cms.Path(process.isotrackproducer)
process.e = cms.EndPath(process.out)

