import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
# searches for muon tracks with sufficient number of hits and removes the corresponding cluster of all but N inner hits of that tracks.

options = VarParsing('analysis')
options.parseArguments()

process = cms.Process("HITREMOVER")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options  = cms.untracked.PSet( wantSummary = cms.untracked.bool(True),
                                       SkipEvent = cms.untracked.vstring('ProductNotFound') )

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

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag

if "Run2016" in options.inputFiles[0]:
    #process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v14', '')
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016LegacyRepro_v4', '')
elif "Run2017" in options.inputFiles[0]:
    process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_ReReco17_forValidation', '')
elif "Run2018D" in options.inputFiles[0]:
    process.GlobalTag = GlobalTag(process.GlobalTag, '102X_dataRun2_Prompt_v11', '')
elif "Run2018" in options.inputFiles[0]:
    process.GlobalTag = GlobalTag(process.GlobalTag, '102X_dataRun2_Sep2018Rereco_v1', '')
elif "Summer16" in options.inputFiles[0]:
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v8', '')
elif "Fall17" in options.inputFiles[0]:
    process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v10', '')
else:
    print "Where is the global tag?"
    quit()
    
process.goodMuons = cms.EDFilter("GoodRecoMuonsFilter",
    trackslabel = cms.InputTag("generalTracks"),
    muonlabel = cms.InputTag("muons"),
    minPt = cms.double(15),
    maxAbsEta = cms.double(2.2),
    filter = cms.bool(True)
)
                                         
process.rCluster = cms.EDProducer("RClusterProducer",
                                      allTracks = cms.InputTag("generalTracks"), 
                                      matchElectrons = cms.InputTag("gedGsfElectrons"),
                                      matchMuons = cms.InputTag("muons"),
                                      matchTo = cms.string("Muon"), #track selection beginning
                                      requiredDr = cms.double(0.01),
                                      minNumberOfLayers = cms.int32(10), #track selection end
                                      layersRemaining = cms.uint32(50), #cluster removal...
                                      onlyValidHits = cms.bool(True),
                                      debug = cms.bool(False),
                                      selectedStripCluster = cms.InputTag("siStripClusters"),
                                      selectedPixelCluster = cms.InputTag("siPixelClusters"),
                                      PrimaryVertex = cms.InputTag('offlinePrimaryVertices'),
                                     )

process.rCluster20 = process.rCluster.clone()
process.rCluster20.layersRemaining=cms.uint32(20)

process.rCluster19 = process.rCluster.clone()
process.rCluster19.layersRemaining=cms.uint32(19)

process.rCluster18 = process.rCluster.clone()
process.rCluster18.layersRemaining=cms.uint32(18)

process.rCluster17 = process.rCluster.clone()
process.rCluster17.layersRemaining=cms.uint32(17)

process.rCluster16 = process.rCluster.clone()
process.rCluster16.layersRemaining=cms.uint32(16)

process.rCluster15 = process.rCluster.clone()
process.rCluster15.layersRemaining=cms.uint32(15)

process.rCluster14 = process.rCluster.clone()
process.rCluster14.layersRemaining=cms.uint32(14)

process.rCluster13 = process.rCluster.clone()
process.rCluster13.layersRemaining=cms.uint32(13)

process.rCluster12 = process.rCluster.clone()
process.rCluster12.layersRemaining=cms.uint32(12)

process.rCluster11 = process.rCluster.clone()
process.rCluster11.layersRemaining=cms.uint32(11)

process.rCluster10 = process.rCluster.clone()
process.rCluster10.layersRemaining=cms.uint32(10)

process.rCluster9 = process.rCluster.clone()
process.rCluster9.layersRemaining=cms.uint32(9)

process.rCluster8 = process.rCluster.clone()
process.rCluster8.layersRemaining=cms.uint32(8)

process.rCluster7 = process.rCluster.clone()
process.rCluster7.layersRemaining=cms.uint32(7)

process.rCluster6 = process.rCluster.clone()
process.rCluster6.layersRemaining=cms.uint32(6)

process.rCluster5 = process.rCluster.clone()
process.rCluster5.layersRemaining=cms.uint32(5)

process.rCluster4 = process.rCluster.clone()
process.rCluster4.layersRemaining=cms.uint32(4)

process.rCluster3 = process.rCluster.clone()
process.rCluster3.layersRemaining=cms.uint32(3)

process.rCluster2 = process.rCluster.clone()
process.rCluster2.layersRemaining=cms.uint32(2)

process.rCluster1 = process.rCluster.clone()
process.rCluster1.layersRemaining=cms.uint32(1)

process.rCluster0 = process.rCluster.clone()
process.rCluster0.layersRemaining=cms.uint32(0)

process.out = cms.OutputModule("PoolOutputModule", 
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = cms.untracked.vstring(
        'keep *',
        ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
 )

#        'drop *',
#        'keep *_*_*_RECO',
#        'keep *_*_*_HITREMOVER',


process.p = cms.Path(process.goodMuons*process.rCluster*process.rCluster20*process.rCluster19*process.rCluster18*process.rCluster17*process.rCluster16*process.rCluster15*process.rCluster14*process.rCluster13*process.rCluster12*process.rCluster11*process.rCluster10*process.rCluster9*process.rCluster8*process.rCluster7*process.rCluster6*process.rCluster5*process.rCluster4*process.rCluster3*process.rCluster2*process.rCluster1*process.rCluster0)
process.e = cms.EndPath(process.out)
