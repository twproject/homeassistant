# AppDaemon app to query via pysnmp network interface for download/upload data.

I created this app due on my Ubiquiti usg box the pppoe interface OID change every time the connection is estabilished.
The app look on the _OID_ + _ReplaceNode_ address for an interface with Interface value name and retrive it's node value. _UploadNode_ or _DownloadNode_ will be set on behalf _ReplaceNode_ and it create the new OID string for upload and download adding the InterfaceNode value

### Example
```
Interface: pppoe0
ReplaceNode: '18'
UploadNode: '10'
DownloadNode: '06'
```

```
snmpwalk -v 2c -c clavister_public 192.168.189.157 1.3.6.1.2.1.31.1.1.1.18
iso.3.6.1.2.1.31.1.1.1.18.1 = STRING: "lo"
iso.3.6.1.2.1.31.1.1.1.18.2 = STRING: "WAN"
iso.3.6.1.2.1.31.1.1.1.18.3 = STRING: "LAN"
iso.3.6.1.2.1.31.1.1.1.18.4 = STRING: "eth2"
iso.3.6.1.2.1.31.1.1.1.18.5 = STRING: "imq0"
iso.3.6.1.2.1.31.1.1.1.18.6 = STRING: "eth1.100@eth1"
iso.3.6.1.2.1.31.1.1.1.18.18 = STRING: "eth1.1001@eth1"
iso.3.6.1.2.1.31.1.1.1.18.308 = STRING: "pppoe0"
```

InterfaceNode is 308

> UploadOID will be (OID+UploadNode+InterfaceNode) --> 1.3.6.1.2.1.31.1.1.1.10.308
 
> DownloadOID will be (OID+DownloadNode+InterfaceNode) --> 1.3.6.1.2.1.31.1.1.1.10.308
 
 App will retrieve the data from OIDs and write to Home Assistant entities

### How to use the app

Change on yaml file the data with yours

```yaml
  Host: '192.168.0.1'
  comunity_read: 'public'
  ScanInterval: 30

  Interface: 'wan'  #set the name of the interface you want to monitor, you can discover with an snmpwalk from linux command line
  OID: '1.3.6.1.2.1.31.1.1.1'  #this is the main OID after that there is the Node of your interface
  ReplaceNode: '18'
  UploadNode: '10'
  DownloadNode: '06'

  ha_download_entity: input_text.unifi_wan_downloadspeed  #Home assistant entities to write download data
  ha_upload_entity: input_text.unifi_wan_uploadspeed  #Home assistant entities to write upload data
```
