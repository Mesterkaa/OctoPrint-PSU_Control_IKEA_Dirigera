---
layout: plugin

id: PSU_Control_IKEA_Dirigera
title: OctoPrint-Psu_control_ikea_dirigera
description: Adds IKEA Dirigera connected smart Outlet support to OctoPrint-PSUControl as a sub-plugin
authors:
- Mesterkaa
license: AGPLv3

# TODO
date: 2024-10-03

homepage: https://github.com/Mesterkaa/OctoPrint-Psu_control_ikea_dirigera
source: https://github.com/Mesterkaa/OctoPrint-Psu_control_ikea_dirigera
archive: https://github.com/Mesterkaa/OctoPrint-Psu_control_ikea_dirigera/archive/master.zip

# TODO
tags:
- control
- power
- psu
- psucontrol
- psucontrol subplugin
- ikea

# TODO
# When registering a plugin on plugins.octoprint.org, all screenshots should be uploaded not linked from external sites.
screenshots:
- url: /assets/img/Plugin
  alt: Plugin Settings
  caption: The PSU Control - IKEA Dirigera plugin settings
- url: /assets/img/IKEAHomeSmart1
  alt: IKEA Homesmart Device Name
  caption: IKEA Homesmart Device name.
- url: /assets/img/IKEAHomeSmart2
  alt: IKEA Homesmart Device Settings
  caption: IKEA Homesmart device settings

# TODO
featuredimage: /assets/img/Plugin

# TODO
# You only need the following if your plugin requires specific OctoPrint versions or
# specific operating systems to function - you can safely remove the whole
# "compatibility" block if this is not the case.

compatibility:
  python: ">=3,<4"

---
# IKEA Dirigera PSU Control
## About

IKEA Dirigera subplugin for [PSU Control](https://github.com/kantlivelong/OctoPrint-PSUControl).

Add the ability to control any IKEA Smart outlet connected to IKEA Dirigera Hub, via the PSU Control Plugin.

- Choose this plugin for Switching and/or sensing in [PSU Control](https://github.com/kantlivelong/OctoPrint-PSUControl) Settings.
- Input Ikea Dirigera IP address, Outlet Name and generate a token and you are ready to go.

## Configuration

Follow the Step-To-Step guide in the Plugin settings.
1. **Enter Outlet Name**
    - The outlet name is the name given to the device in the IKEA "Home Smart" App.
        - [Apple](https://apps.apple.com/us/app/ikea-home-smart/id1633226273)
        - [Android](https://play.google.com/store/apps/details?id=com.ikea.inter.homesmart.system2)
    - The name needs to be unique and can be edited in the app.
2. **Enter IP Address**
    - IP Address of the IKEA Dirigera Hub. The app sadly doesn't show it so it has be found in other ways e.g. your router settings.
3. **Send Challenge**
    - Click the button and await a succes.
    - A **fail** will be followed by some error data that might give a hint of the error.
4. **Click Action Button**
    - On the buttom of the IKEA Dirigera device is a button label **Action**.
    - Click this on.
5. **Generate Token**
    - Click the button and await a succes.
    - A succesfull call will result in **token** in the "Generated Token" field.
    - A **fail** will be followed by some error data that might give a hint of the error.
6. **Test Connection (Optional)**
    - Optionally you can test the connection
    - On a succes you should see the current status of the outlet
7. **Remeber to Save**
    - The token has been fetched from the IKEA Dirigera but has yet to be saved.
    - **Remeber to save!!**
