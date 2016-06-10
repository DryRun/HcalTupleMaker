
# example crab configuration file for one single run

##________________________________________________________________________________||
#Configurables

#dataset = '/MinimumBias/Commissioning2016-v1/RAW'
#dataset = '/Cosmics/Commissioning2016-v1/RAW'
#dataset = '/JetHT/Run2016B-v2/RAW'
dataset = '/JetHT/Run2016B-v1/RAW'
runs = '272760,272761,272762'
version = "v1_1_sub2"
#run = '266150'
#run = '268500'

##________________________________________________________________________________||

jobname = "HCALPFG_digis_isobx_"
jobname += dataset[1:].replace('/','_').replace(':','_')#.replace('RAW','RAW_'+run)
jobname += "_" + version
##________________________________________________________________________________||

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

##________________________________________________________________________________||

config.General.requestName = jobname
config.General.workArea = 'crab_workarea'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/uscms/home/dryu/HCAL/CMSSW_8_0_8_patch1/src/HCALPFG/HcalTupleMaker/test/analysis_digis_isobx_cfg.py'
config.JobType.pyCfgParams = ['outputFile=hcalTupleTree.root']

config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
#config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
config.Data.runRange = runs # '193093-194075'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'HCALPFG_digis_isobx_' + dataset.split("/")[0] + "_" + dataset.split("/")[1] + "_" + version

config.Site.storageSite = "T3_US_FNALLPC"
#config.Site.storageSite = "T3_US_Brown"
