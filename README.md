# OctoPrint Plugin PSU Control IKEA Dirigera

<img src="./assets/img/OctoPrintXIKEA.png" width="400">


IKEA Dirigera sub-plugin for [PSU Control](https://github.com/kantlivelong/OctoPrint-PSUControl) in [Octoprint](https://octoprint.org/)

Add the ability to control any IKEA smart outlet connected to IKEA Dirigera Hub, via the PSU Control Plugin.

- Choose this plugin for Switching/Sensing in [PSU Control](https://github.com/kantlivelong/OctoPrint-PSUControl) settings.
- Input IKEA Dirigera IP address, Outlet Name and generate a token, and you are ready to go.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/Mesterkaa/OctoPrint-PSU_Control_IKEA_Dirigera/archive/main.zip

## Configuration

Follow the Step-by-Step guide in the Plugin settings.
1. **Enter Outlet Name**
    - The Outlet Name is the name given to the device in the IKEA "Home Smart" App.
        - [Apple](https://apps.apple.com/us/app/ikea-home-smart/id1633226273)
        - [Android](https://play.google.com/store/apps/details?id=com.ikea.inter.homesmart.system2)
    - The name needs to be unique and can be edited in the app.
2. **Enter IP Address**
    - IP Address of the IKEA Dirigera Hub. The app sadly doesn't show it, so it has to be found in other ways e.g. your router settings.
3. **Send Challenge**
    - Click the **Send Challenge** button and await a success.
    - A **fail** will be followed by some error data that might give a hint of the problem.
4. **Press the Action Button**
    - The **Action** button can be found labeled on the bottom of the IKEA Dirigera device.
5. **Generate Token**
    - Click the **Get Token** button and await a success.
    - A successful call will result in a **token** in the "Generated Token" field.
    - A **fail** will be followed by some error data that might give a hint of the error.
6. **Test Connection (Optional)**
    - Click the **Test Connection** button and await a success.
    - On a success you should see the current status of the outlet.
7. **Remember to Save**
    - The token has been fetched from the IKEA Dirigera but has yet to be saved.
    - **Remember to save!**

## Screenshots
### Plugin Settings
<img src="./assets/img/Plugin.png" width="600">

### IKEA Homesmart App
<img src="./assets/img/IKEAHomeSmart1.png" width="400">

<img src="./assets/img/IKEAHomeSmart2.png" width="400">
