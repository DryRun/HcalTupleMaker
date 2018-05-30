#ifndef HcalTupleMaker_QIE11Digis_h
#define HcalTupleMaker_QIE11Digis_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibFormats/HcalObjects/interface/HcalCalibrations.h"
#include "CalibFormats/HcalObjects/interface/HcalTPGCoder.h"
#include "CalibFormats/HcalObjects/interface/HcalTPGRecord.h"
#include "CalibCalorimetry/HcalTPGAlgos/interface/HcaluLUTTPGCoder.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalDigi/interface/HcalUMNioDigi.h"
#include "DataFormats/HcalDetId/interface/HcalGenericDetId.h"

class HcalTupleMaker_QIE11Digis : public edm::EDProducer {
public:
  explicit HcalTupleMaker_QIE11Digis(const edm::ParameterSet&);

private:
  void produce( edm::Event &, const edm::EventSetup & ); 
  std::string prefix,suffix; 
  bool storelaser;
  const edm::InputTag _taguMNio;
  const edm::InputTag m_qie11DigisTag;
  
  edm::EDGetTokenT<HcalDataFrameContainer<QIE11DataFrame> > qie11digisToken_;
  edm::EDGetTokenT<HcalUMNioDigi> _tokuMNio;
};

#endif
