from pysnmp.hlapi import *
import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta

class hassio_unifi_internet_interface(hass.Hass):
    def initialize(self):

        self.log("########### unifi pppoe query OID INIT ###########", level = 'INFO')

        self.run_every(self.hassio_unifi_internet_interface_query,datetime.now(), self.args["ScanInterval"])
		
        self.log("########### unifi pppoe query OID END INIT ###########", level = 'INFO')

    def hassio_unifi_internet_interface_query(self, kwargs):
          try:
          
#### Variables from yaml file
            Host = self.args["Host"]
            comunity_read = self.args["comunity_read"]

            Interface = self.args["Interface"]
            OID = self.args["OID"]
            
            ReplaceNode = "." + self.args["ReplaceNode"]
            UploadNode = "." + self.args["UploadNode"] + "."
            DownloadNode = "." + self.args["DownloadNode"] + "."	
#####################################################
##
##  START CODE
##
#####################################################
            for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(), 
            CommunityData(comunity_read), UdpTransportTarget((Host, 161)), ContextData(), 
            ObjectType(ObjectIdentity(OID + ReplaceNode)),lookupMib=False,lexicographicMode=False):
                if errorIndication:
                    self.log("########### ERROR ###########", level = 'DEBUG')
                    print(errorIndication, file=sys.stderr)
                    break
                elif errorStatus:
                    self.log("########### ERROR STATUS###########", level = 'DEBUG')				
                    print('%s at %s' % (errorStatus.prettyPrint(),
                                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
                                        file=sys.stderr)             
                    break
                else:
                    for varBind in varBinds:
                        if varBind[1]._value.decode('UTF-8') == Interface:
                            uploadOID = varBind[0].prettyPrint().replace(ReplaceNode + ".",UploadNode)
                            downloadOID = varBind[0].prettyPrint().replace(ReplaceNode + ".",DownloadNode)
            self.log("########### RESULTS ###########", level = 'DEBUG')
            self.log(uploadOID, level = 'DEBUG')
            self.log(downloadOID, level = 'DEBUG')

#####################################################
##
##  UPLOAD | DOWNLOAD SPEED
##
#####################################################

            for (errorIndication,errorStatus,errorIndex,varBinds) in getCmd(SnmpEngine(), 
            CommunityData(comunity_read), UdpTransportTarget((Host, 161)), ContextData(), 
            ObjectType(ObjectIdentity(uploadOID)), ObjectType(ObjectIdentity(downloadOID)),lookupMib=False,lexicographicMode=False):
                if errorIndication:
                    self.log("########### ERROR ###########", level = 'DEBUG')
                    print(errorIndication, file=sys.stderr)
                    break
                elif errorStatus:
                    self.log("########### ERROR STATUS###########", level = 'DEBUG')				
                    print('%s at %s' % (errorStatus.prettyPrint(),
                                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
                                        file=sys.stderr)             
                    break
                else:
#                    for varBind in varBinds:
#                        UploadSpeedPPPoE = varBind[1]._value
                    UploadSpeedPPPoE = varBinds[0][1]._value
                    DownloadSpeedPPPoE = varBinds[1][1]._value                     
#####################################################
##
##  DOWNLOAD SPEED
##
#####################################################

            # for (errorIndication,errorStatus,errorIndex,varBinds) in getCmd(SnmpEngine(), 
            # CommunityData(comunity_read), UdpTransportTarget((Host, 161)), ContextData(), 
            # ObjectType(ObjectIdentity(downloadOID)),lookupMib=False,lexicographicMode=False):
                # if errorIndication:
                    # self.log("########### ERROR ###########", level = 'DEBUG')
                    # print(errorIndication, file=sys.stderr)
                    # break
                # elif errorStatus:
                    # self.log("########### ERROR STATUS###########", level = 'DEBUG')				
                    # print('%s at %s' % (errorStatus.prettyPrint(),
                                        # errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
                                        # file=sys.stderr)             
                    # break
                # else:
                    # for varBind in varBinds:
                        # DownloadSpeedPPPoE = varBind[1]._value


            self.log(UploadSpeedPPPoE, level = 'DEBUG')
            self.log(DownloadSpeedPPPoE, level = 'DEBUG')

            data_time = datetime.now()

            self.set_state(self.args["ha_upload_entity"], 
                                state="{}".format(UploadSpeedPPPoE), 
                                attributes = {"retrieve_date": data_time})

            self.set_state(self.args["ha_download_entity"], 
                                state="{}".format(DownloadSpeedPPPoE), 
                                attributes = {"retrieve_date": data_time})

          except Exception as inst:
            self.log(inst, level = 'ERROR')
            return
