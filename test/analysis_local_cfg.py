#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
import FWCore.ParameterSet.VarParsing as VarParsing

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------

options = VarParsing.VarParsing()

options.register('skipEvents',
                 0, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to skip")

options.register('processEvents',
                 -1, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to process")

options.register('inputFiles',
                 "root://cmsxrootd-site.fnal.gov//store/data/Commissioning2016/MinimumBias/RAW/v1/000/264/232/00000/1EDB8470-71D1-E511-A299-02163E014504.root", #default value, corresponds to LFN /store/data/Commissioning2016/MinimumBias/RAW/v1/000/264/232/00000/1EDB8470-71D1-E511-A299-02163E014504.root from run 267594
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 "Input files")

options.register('outputFile',
                 "file:/uscms/home/dryu/HCAL/data/HCALPFG/utca_noise_test/hcalTupleTree_267594.root", #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output file")

options.register('doReco',
                 False, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Run HCAL reconstruction algo?")
options.register('globalTag',
    '80X_dataRun2_Prompt_v8',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "Global Tag")

options.parseArguments()


#------------------------------------------------------------------------------------
# Declare the process and input variables
#------------------------------------------------------------------------------------
process = cms.Process('PFG')
inputFiles = options.inputFiles
skipEvents = options.skipEvents
processEvents = options.processEvents
outputFile = options.outputFile

#------------------------------------------------------------------------------------
# Get and parse the command line arguments
#------------------------------------------------------------------------------------
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(processEvents) )
process.source = cms.Source("HcalTBSource",
    fileNames  = cms.untracked.vstring(inputFiles),
    skipEvents = cms.untracked.uint32(skipEvents),
)

process.TFileService = cms.Service("TFileService",
     fileName = cms.string(outputFile)
)

#------------------------------------------------------------------------------------
# import of standard configurations
#------------------------------------------------------------------------------------
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.load("EventFilter.HcalRawToDigi.HcalRawToDigi_cfi")
process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
process.hbhereco = process.hbheprereco.clone()
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.es_ascii = cms.ESSource('HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(
            object = cms.string('ElectronicsMap'),
            file = cms.FileInPath('HCALPFG/HcalTupleMaker/data/2016-feb-24/version_G_emap_all.txt')
            ),
        )
    )
process.es_prefer = cms.ESPrefer('HcalTextCalibrations','es_ascii')

#------------------------------------------------------------------------------------
# Set up our analyzer
#------------------------------------------------------------------------------------
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_cfi") # Dont want to use this, load modules individually
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Tree_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalUnpackerReport_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Event_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHEDigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HODigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HFDigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHERecHits_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HORecHits_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HFRecHits_cfi")

#------------------------------------------------------------------------------------
# Since this is a local run, make sure we're looking for the FEDs in the right place
#------------------------------------------------------------------------------------
process.hcalDigis.InputLabel = cms.InputTag("source")

#------------------------------------------------------------------------------------
# FED numbers
#------------------------------------------------------------------------------------
#process.hcalDigis.FEDs = cms.untracked.vint32(1100, 1102, 1104, 1106, 1108, 1110, 1112, 1114, 1116)


#------------------------------------------------------------------------------------
# Specify Global Tag
#------------------------------------------------------------------------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options.globalTag #'80X_dataRun2_Prompt_v4'

#------------------------------------------------------------------------------------
# HcalTupleMaker sequence definition
#------------------------------------------------------------------------------------
process.tuple_step = cms.Sequence(
    # Make HCAL tuples: Event, run, ls number
    process.hcalTupleEvent*
    # Make HCAL tuples: FED info
    #process.hcalTupleFEDs*
    # Make HCAL tuples: unpacker info
    #process.hcalTupleUnpackReport*
    # Make HCAL tuples: digi info
    process.hcalTupleHBHEDigis*
    process.hcalTupleHODigis*
    process.hcalTupleHFDigis*
    #process.hcalCosmicDigis*
    #    process.hcalTupleTriggerPrimitives*
    #    # Make HCAL tuples: digi info
    #process.hcalTupleHBHECosmicsDigis*
    #    process.hcalTupleHOCosmicsDigis*
    #    # Make HCAL tuples: digi info
    #    process.hcalTupleHBHEL1JetsDigis*
    #    process.hcalTupleHFL1JetsDigis*
    #    process.hcalTupleL1JetTriggerPrimitives*
    #    # Make HCAL tuples: reco info
    process.hcalTupleHBHERecHits*
    process.hcalTupleHFRecHits*
    process.hcalTupleHORecHits*
    #process.hcalTupleHcalNoiseFilters*
    #process.hcalTupleMuonTrack*
    #
    #process.hcalTupleHBHERecHitsMethod0*
    #process.hcalTupleHcalNoiseFiltersMethod0*
    #process.hcalTupleCaloJetMetMethod0*
    #    process.hcalTupleHFRecHits*
    #    # Trigger info
    #process.hcalTupleTrigger*
    
    #    process.hcalTupleTriggerObjects*
    #    # Make HCAL tuples: cosmic muon info
    # process.hcalTupleCosmicMuons*
    #    # Package everything into a tree
    #
    process.hcalTupleTree
)


#-----------------------------------------------------------------------------------
# Path and EndPath definitions
#-----------------------------------------------------------------------------------
process.preparation = cms.Path(
    # Unpack digis from RAW
    process.hcalDigis*
    # Do energy reconstruction
#    process.hbhereco*
#    process.horeco*
#    process.hfreco*
    # Make the ntuples
    process.tuple_step
)
