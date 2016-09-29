#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------

import FWCore.ParameterSet.Config as cms
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
                 #"file:/uscms/home/dryu/HCAL/data/HCALPFG/LaserTag/06D51970-8E65-E611-8E4A-FA163EE80441.root",
                 #"/store/data/Run2016G/TestEnablesEcalHcal/RAW/v1/000/279/022/00000/06D51970-8E65-E611-8E4A-FA163EE80441.root",
                "",
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 "Input files")

options.register('outputFile',
                 "HCAL_output.root", #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output file")
options.register('lbRange', 
                  "",
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string, 
                  "String specifying the lumiblocks to run over.")

options.register('globalTag',
    '80X_dataRun2_Prompt_v11',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "Global Tag")



options.parseArguments()

print "Skip events =", options.skipEvents
print "Process events =", options.processEvents
print "inputFiles =", options.inputFiles
print "outputFile =", options.outputFile
print "Global Tag =", options.globalTag
print "lbRange =", options.lbRange

if len(options.inputFiles) == 0:
    options.inputFiles = ["/store/data/Run2016G/TestEnablesEcalHcal/RAW/v1/000/279/022/00000/06D51970-8E65-E611-8E4A-FA163EE80441.root", "/store/data/Run2016G/TestEnablesEcalHcal/RAW/v1/000/279/022/00000/308B6578-8265-E611-8B72-02163E012B55.root", "/store/data/Run2016G/TestEnablesEcalHcal/RAW/v1/000/279/022/00000/42CA8E30-7D65-E611-900A-02163E014428.root", "/store/data/Run2016G/TestEnablesEcalHcal/RAW/v1/000/279/022/00000/5A994658-8E65-E611-A308-FA163E9F796D.root", "/store/data/Run2016G/TestEnablesEcalHcal/RAW/v1/000/279/022/00000/A6343F0B-8865-E611-A94E-FA163E642BEC.root"]

#------------------------------------------------------------------------------------
# Declare the process
#------------------------------------------------------------------------------------

process = cms.Process("PFG")

#-------------------------------------
#   Central DQM Stuff imports
#-------------------------------------
from DQM.Integration.config.online_customizations_cfi import *
useOfflineGT = True
if useOfflineGT:
    process.load('DQM.Integration.config.FrontierCondition_GT_Offline_cfi')
    process.GlobalTag.globaltag = options.globalTag
else:
    process.load('DQM.Integration.config.FrontierCondition_GT_cfi')
#useFileInput = False
#if useFileInput:
#    process.load("DQM.Integration.config.fileinputsource_cfi")
#else:
#    process.load('DQM.Integration.config.inputsource_cfi')
process.load('DQMServices.Components.DQMEnvironment_cfi')
process.load('DQM.Integration.config.environment_cfi')

#-------------------------------------
#   CMSSW/Hcal non-DQM Related Module import
#-------------------------------------
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.load("EventFilter.HcalRawToDigi.HcalRawToDigi_cfi")
process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
process.load("SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff")
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.load("L1Trigger.Configuration.L1DummyConfig_cff")
process.load("EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi")
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")

#-------------------------------------
#   CMSSW/Hcal non-DQM Related Module Settings
#   -> runType
#   -> Generic Input tag for the Raw Collection
#   -> cmssw version
#   -> Turn off default blocking of dead channels from rechit collection
#   -> Drop Channel Status Bits (had benn 'HcalCellOff', "HcalCellDead")
#   -> For Trigger Primitives Emulation
#   -> L1 GT setting
#   -> Rename the hbheprereco to hbhereco
#-------------------------------------
#runType         = process.runType.getRunType()
rawTag          = cms.InputTag("hltHcalCalibrationRaw")
process.essourceSev = cms.ESSource(
        "EmptyESSource",
        recordName      = cms.string("HcalSeverityLevelComputerRcd"),
        firstValid      = cms.vuint32(1),
        iovIsRunNotTime = cms.bool(True)
)
process.hcalRecAlgos.DropChannelStatusBits = cms.vstring('')
process.emulTPDigis = process.simHcalTriggerPrimitiveDigis.clone()
process.emulTPDigis.inputLabel = \
        cms.VInputTag("hcalDigis", 'hcalDigis')
process.emulTPDigis.FrontEndFormatError = cms.bool(True)
process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(False)
process.emulTPDigis.FG_threshold = cms.uint32(2)
process.emulTPDigis.InputTagFEDRaw = rawTag
process.l1GtUnpack.DaqGtInputTag = rawTag
process.hbhereco = process.hbheprereco.clone()

#-------------------------------------
#   To force using uTCA
#   Absent for Online Running
#-------------------------------------
useMap = False
if useMap:
    process.es_pool = cms.ESSource("PoolDBESSource",
            process.CondDBSetup,
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string(
                        "HcalElectronicsMapRcd"
                    ),
                    tag = cms.string(
                        "HcalElectronicsMap_v7.05_hlt"
                    )
                )
            ),
            connect = cms.string(
                'frontier://FrontierProd/CMS_CONDITIONS'),
            authenticationMethod = cms.untracked.uint32(0)
    )   
    process.es_prefer_es_pool = cms.ESPrefer('PoolDBESSource', 'es_pool')
#-------------------------------------
#   Some Settings before Finishing up
#-------------------------------------
process.hcalDigis.InputLabel = rawTag
process.hcalDigis.ComplainEmptyData = True



#------------------------------------------------------------------------------------
# Set up the input source, depending on whether this is a local or global run
#------------------------------------------------------------------------------------

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(options.inputFiles),
  skipEvents = cms.untracked.uint32(options.skipEvents),
)

if options.lbRange != "":
    print "lbRange = " + options.lbRange
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(options.lbRange)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(
       options.processEvents
   )
)
process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)


#------------------------------------------------------------------------------------
# Set up the output
#------------------------------------------------------------------------------------

#process.TFileService = cms.Service("TFileService",
#    fileName = cms.string( 'HCAL_output.root' )
#)
process.TFileService = cms.Service("TFileService", fileName = cms.string( options.outputFile ))


# Set up our analyzer
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Tree_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Event_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_FEDs_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHEDigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HODigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HFDigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalCalibDigis_cfi")
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalLaserDigis_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_QIE10Digis_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HBHERecHits_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HORecHits_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HFRecHits_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_Trigger_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_TriggerObjects_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_RecoTracks_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalTriggerPrimitives_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_L1Jets_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_L1GCTJets_cfi")
#process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_HcalUnpackerReport_cfi")
process.hcalTupleTree = cms.EDAnalyzer("HcalTupleMaker_Tree",
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_hcalTupleEvent_*_*',
        'keep *_hcalTupleFEDs_*_*',
        'keep *_hcalTupleHBHEDigis_*_*',
        'keep *_hcalTupleHODigis_*_*',
        'keep *_hcalTupleHFDigis_*_*',
        'keep *_hcalTupleCalibDigis_*_*',
        'keep *_hcalTupleLaserDigis_*_*',
        #'keep *_hcalTupleHBHERecHits_*_*',
        #'keep *_hcalTupleHORecHits_*_*',
        #'keep *_hcalTupleHFRecHits_*_*'
    )
)

process.hcalDigis.InputLabel = cms.InputTag("hltHcalCalibrationRaw")
#process.qie10Digis.InputLabel = cms.InputTag("hltHcalCalibrationRaw")
process.hcalTupleFEDs.source = cms.untracked.InputTag("hltHcalCalibrationRaw")
process.hcalDigis.FilterDataQuality = cms.bool(False)
process.hcalDigis.FEDs = cms.untracked.vint32()
for FED in [x+700 for x in range(32)]:
    process.hcalDigis.FEDs.append ( FED ) 
for FED in xrange(1100, 1124, 2):
    process.hcalDigis.FEDs.append ( FED ) 

#------------------------------------------------------------------------------------
# Define the final path
#------------------------------------------------------------------------------------

process.p = cms.Path(
    # Unpack digis from RAW
    process.hcalDigis*
    #process.qie10Digis*
    # Make HCAL tuples: Event, run, ls number
    process.hcalTupleEvent*
    # Make HCAL tuples: FED info
    process.hcalTupleFEDs*
    # Make HCAL tuples: digi info
    process.hcalTupleHBHEDigis*
    process.hcalTupleHFDigis*
    process.hcalTupleCalibDigis*
    process.hcalTupleLaserDigis*
    # Make HCAL tuples: reco info
    #process.hcalTupleHBHERecHits*
    #process.hcalTupleHFRecHits*
    # Package everything into a tree
    process.hcalTupleTree
)

#------------------------------------------------------------------------------------
# Make a schedule and run
#------------------------------------------------------------------------------------

process.schedule = cms.Schedule(process.p)

