Integrate Aernova FanCoils systems into HomeAssistant (https://www.aernovagroup.it/it/prodotti/ventilconvettori.html)

Copy aernova_fancoil folder into custom_components and reboot Home Assistant

Edit configuration.yaml

```
aernova_fancoil:
  - type: tcp
    host: <modbus controller ip>
    port: 9998
    name: EW11_aernova_fancoil
    climates: !include_dir_merge_list modbus/climates
```

Create a folder under config: modbus\climates and create a new yaml file

```
  - name: Kitchen
    slave: <slave id>
    address: 02
    target_temp_register: 003
    hvac_mode_register:
      address: 12
      values:
        "state_cool": 7
        "state_heat": 3
        "state_off": 1
    precision: 1
    max_temp: 30
    min_temp: 15
    temp_step: 0.1	
    data_type: int16
    count: 1
    scale: 0.1
    offset: 0
    humidity_register: 199  # Optional if you have a TH thermostat version (https://www.aernovagroup.it/it/prodotti/termostati/th.html)
    unique_id: "climate_kitchen"
```

![immagine](https://github.com/twproject/homeassistant/assets/7046065/35b9f1ed-982b-4bea-a02d-32bbb741c8f7)

![immagine](https://github.com/twproject/homeassistant/assets/7046065/a5e0d883-b611-4cef-8f13-104bda7cb8b6)


If you want another graphics install from hacs simple-thermostat


![immagine](https://github.com/twproject/homeassistant/assets/7046065/e5c1ac5a-2970-4f24-9b8c-cb1d57c03fb8)


```
control:
  _headings: false
entity: climate.kitchen
hide:
  state: true
  temperature: true
icon:
  cool: mdi:snowflake
  heat: mdi:fire
  'off': mdi:power
sensors:
  - attribute: current_temperature
    entity: climate.kitchen
    icon: mdi:home-thermometer-outline
    name: Temperature
  - entity: sensor.kitchen_motor_speed
    icon: mdi:fan
    name: Motor Speed
step_size: 0.1
type: custom:simple-thermostat
```


