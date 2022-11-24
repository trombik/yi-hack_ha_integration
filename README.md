# yi-hack Home Assistant integration
<p align="center">
<img src="https://github.com/roleoroleo/yi-hack_ha_integration/raw/main/images/icon.png">
</p>

## Overview
yi-hack Home Assistant is a custom integration for Yi cameras (or Sonoff camera) with one of the following custom firmwares:
- yi-hack-MStar - https://github.com/roleoroleo/yi-hack-MStar
- yi-hack-Allwinner - https://github.com/roleoroleo/yi-hack-Allwinner
- yi-hack-Allwinner-v2 - https://github.com/roleoroleo/yi-hack-Allwinner-v2
- yi-hack-v5 (partial support) - https://github.com/alienatedsec/yi-hack-v5
- sonoff-hack - https://github.com/roleoroleo/sonoff-hack
<br>
And make sure you have the latest version.
<br>

This integration is available from the Lovelace frontend without the need to configure the devices in the file configuration.yaml
The wizard will connect to your cam and will install the following entities:
- ffmpeg cam with stream and snapshot capabilities
- mqtt cam with the last frame saved during a motion detection event
- mqtt binary sensor for status (connection)
- mqtt binary sensor for motion detection
- mqtt binary sensor for ai human detection (there are known issues when enabling ai human detection) (*)
- mqtt binary sensor for sound detection (*)
- mqtt binary sensor for baby crying detection (*)
- media player entity useful to play Home Assistant standard tts service (*)
- switch to enable/disable privacy (this switch turns on or off the rtsp stream and the snapshot)
- ptz service (*)
- speak service (only available if you install the internal tts engine from here https://github.com/roleoroleo/yi-hack-utils)

(*) available only if your cam supports it.

If you configure motion detection in your camera and media source in your home assistant installation, you will be able to view the videos in the "Media" section (left panel of the main page).

## Installation
**(1)** Copy the  `custom_components` folder your configuration directory.
It should look similar to this:
```
<config directory>/
|-- custom_components/
|   |-- yi_hack/
|       |-- translations/
|       |-- __init__.py
|       |-- binary_sensor.py
|       |-- camera.py
|       |-- config.py
|       |-- config_flow.py
|       |-- const.py
|       |-- manifest.json
|       |-- media_player.py
|       |-- media_source.py
|       |-- services.yaml
|       |-- strings.json
|       |-- switch.py
|       |-- views.py
```
**(2)** Restart Home Assistant

**(3)** Configure device and entities:
- Go to Settings -> Integrations
- Click "Add Integration" in the lower-right corner
- Select "Yi Cam with yi-hack" integration
<p align="center">
<img src="https://user-images.githubusercontent.com/39277388/118390725-eadd7700-b630-11eb-87f9-9b03b1e587f4.png" width="400">
</p>

- Enter the settings to connect to the web interface of your cam: host, port, username, password and ffmpeg parameters
<p align="center">
<img src="https://user-images.githubusercontent.com/39277388/118390634-67bc2100-b630-11eb-8f73-008cad6b2b3d.png" width="400">
</p>

- Confirm and wait for the wizard completion
- Set the "Area" if you need it
- Enjoy your cam
<br><br>

## Add the stream to lovelace
If you want to add your live stream to lovelace, use this custom components: https://github.com/AlexxIT/WebRTC/

And add a simple configuration like this:
```
type: 'custom:webrtc-camera'
entity: camera.yi_hack_m_XXXXXX_cam
ui: true
```

## Requirements
This component requires MQTT integration to be installed.
Please be sure you added MQTT to you Home Assistant configuration.

If you want to browse mp4 files saved on your cam, add media source component to your home assistant installation.
Add the linw below to your configuration file:
```
# Example configuration.yaml entry
media_source:
```

## Supported Entities

The following entities are implemented (depending on the device model).

### Switches

| Name | Description |
|------|-------------|
| `motion_detection` | enable or disable motion detection |
| `human_detection` | enable or disable human detection (currently not working, see [yi-hack-Allwinner-v2#333](https://github.com/roleoroleo/yi-hack-Allwinner-v2/issues/333)) |
| `baby_crying` | enable or disable baby crying detection |
| `sound_detection` | enable or disable sound detection |
| `privacy` | enable or disable privacy mode by disabling camera |

## Donation
If you like this project, you can buy me a beer :) 
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=JBYXDMR24FW7U&currency_code=EUR&source=url)

---
### DISCLAIMER
**I AM NOT RESPONSIBLE FOR ANY USE OR DAMAGE THIS SOFTWARE MAY CAUSE. THIS IS INTENDED FOR EDUCATIONAL PURPOSES ONLY. USE AT YOUR OWN RISK.**
