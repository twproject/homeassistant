Change on yaml file the data with yours

  Host: '192.168.0.1'
  comunity_read: 'public'
  ScanInterval: 30

  Interface: 'wan'  (set the name of the interface you want to monitor, you can discover with an snmpwalk from linux command line)
  OID: '1.3.6.1.2.1.31.1.1.1'  (this is the main OID after that there is the Node of your interface)
  ReplaceNode: '18'
  UploadNode: '10'
  DownloadNode: '06'

  ha_download_entity: input_text.unifi_wan_downloadspeed  (Home assistant entities to write download data)
  ha_upload_entity: input_text.unifi_wan_uploadspeed  (Home assistant entities to write upload data)
