
# example crab configuration file for one single run

##________________________________________________________________________________||
#Configurables
#dataset = '/MinimumBias/Run2016G-v1/RAW'
dataset='/TestEnablesEcalHcal/Run2016G-v1/RAW'
#run = '266150'
run = '279022'

##________________________________________________________________________________||

jobname = dataset[1:].replace('/','_')
jobname = jobname.replace(':','_')
jobname = jobname.replace('RAW','RAW_'+run)
jobname += "_v1"
##________________________________________________________________________________||

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

##________________________________________________________________________________||

config.General.requestName = jobname
config.General.workArea = 'crab_workarea'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/home/dryu/HCAL/CMSSW_8_0_8_patch1/src/HCALPFG/HcalTupleMaker/test/crab/lasertag_cfg.py'
config.JobType.pyCfgParams = ['outputFile=hcalTupleTree.root', 'lbRange=279022:389-279022:390']

config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.totalUnits = 20
#config.Data.lumiMask = 'lasertag_lumimask.json'
config.Data.runRange = run # '193093-194075'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'PFG_HcalTupleMaker'
config.Data.ignoreLocality = True

#config.Site.storageSite = "T3_US_FNALLPC"
config.Site.storageSite = "T3_US_Brown"
