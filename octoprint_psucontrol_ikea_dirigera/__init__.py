# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import dirigera
import dirigera.hub.auth as dirigera_auth
import string
import requests
import socket

ALPHABET = f"_-~.{string.ascii_letters}{string.digits}"
CODE_LENGTH = 128

class Psu_control_ikea_dirigeraPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SimpleApiPlugin
):

    def __init__(self):
        self.config = dict()
        self.hub = None

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            IP = '',
            Token = '',
            Outlet_Name = ''
        )

    def on_settings_save(self, data):
        self._logger.info(data)
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.reload_settings()

    def get_settings_version(self):
        return 1

    def on_settings_initialized(self):
        self.reload_settings()

    def reload_settings(self):
        for key, value in self.get_settings_defaults().items():
            if type(value) == str:
                value = self._settings.get([key])
            elif type(value) == int:
                value = self._settings.get_int([key])
            elif type(value) == float:
                value = self._settings.get_float([key])
            elif type(value) == bool:
                value = self._settings.get_boolean([key])

            self.config[key] = value
            self._logger.debug("{}: {}".format(key, value))

        self._logger.info(f"Config: {self.config}")
        self._init_hub()

    def on_settings_migrate(self, target, current=None):
        pass

    def on_startup(self, host, port):
        self._logger.info("Starting up PSU Control - IKEA Dirigera")
        psucontrol_helpers = self._plugin_manager.get_helpers("psucontrol")
        if not psucontrol_helpers or 'register_plugin' not in psucontrol_helpers.keys():
            self._logger.warning("The version of PSUControl that is installed does not support plugin registration.")
            return

        self._logger.debug("Registering plugin with PSUControl")
        psucontrol_helpers['register_plugin'](self)
        self.reload_settings()
        self._init_hub()

    def _init_hub(self):
        self._logger.info("Initializing Hub")
        if self.config['Token'] is not None and self.config['Token'] is not "" and self.config['IP'] is not None and self.config['IP'] is not "":
            self._logger.info("Hub initialized")
            self.hub = dirigera.Hub(
                token=self.config['Token'],
                ip_address=self.config['IP']
            )
        else:
            self._logger.info("Hub not initialized. Config not set")

    def turn_psu_on(self):
        if self.hub is not None and self.config['Outlet_Name'] is not None:
            smart_plug = self.hub.get_outlet_by_name(self.config['Outlet_Name'])
            smart_plug.set_on(outlet_on=True)
        pass

    def turn_psu_off(self):
        if self.hub is not None and self.config['Outlet_Name'] is not None:
            smart_plug = self.hub.get_outlet_by_name(self.config['Outlet_Name'])
            smart_plug.set_on(outlet_on=False)
        pass

    def get_psu_state(self):
        if self.hub is not None and self.config['Outlet_Name'] is not None:
            smart_plug = self.hub.get_outlet_by_name(self.config['Outlet_Name'])
            return smart_plug.attributes.is_on
        return False



    def get_api_commands(self):
        commands = dict(
            sendChallenge=["ip_address"],
            getToken=["ip_address", "code", "code_verifier"],
            testConnection=["ip_address", "token", "outlet_name"],
        )
        self._logger.info("commands: %s" % commands)
        return commands



    def on_api_command(self, command, data):
        self._logger.info("API command: %s" % command)
        self._logger.info("Data: %s" % data)
        import flask
        if command == "sendChallenge":
            if "ip_address" in data:
                ip = data['ip_address']
                self._logger.info("IP address provided for command: %s" % ip)

                sendChallengeResult = self.sendChallenge(ip)
                if "error" in sendChallengeResult:
                    errorResponse = flask.jsonify(error=sendChallengeResult["error"])
                    errorResponse.status_code = 400
                    return flask.abort(errorResponse)

                return flask.jsonify(code=sendChallengeResult["code"], code_verifier=sendChallengeResult["code_verifier"])
            else:
                self._logger.error("No IP address provided")
                return flask.abort(400, "No IP address provided")

        elif command == "getToken":
            if "ip_address" in data and "code" in data and "code_verifier" in data:

                ip = data['ip_address']
                code = data['code']
                code_verifier = data['code_verifier']
                getTokenResult = self.getToken(ip, code, code_verifier)

                if "error" in getTokenResult:
                    errorResponse = flask.jsonify(error=getTokenResult["error"])
                    errorResponse.status_code = 400
                    return flask.abort(errorResponse)

                return flask.jsonify(token=getTokenResult["token"])
            else:
                self._logger.error("Missing data for getToken")
                return flask.abort(400, "Error: Missing data for getToken")

        elif command == "testConnection":
            if "ip_address" in data and "token" in data and "outlet_name" in data:
                ip = data['ip_address']
                token = data['token']
                outlet_name = data['outlet_name']
                hub = dirigera.Hub(
                    token=token,
                    ip_address=ip
                )
                try:
                    smart_plug = hub.get_outlet_by_name(outlet_name)
                except AssertionError as e:
                    response = flask.jsonify(error=e.args[0])
                    response.status_code = 400
                    return flask.abort(response)

                except requests.exceptions.ConnectTimeout as e:
                    response = flask.jsonify(error="Timeout. Check that the IP address is correct and that the device is on")
                    response.status_code = 400
                    return flask.abort(response)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 401:
                        response = flask.jsonify(error="Not authorized. Try to regenerate token")
                        response.status_code = 400
                        return flask.abort(response)

                    response = flask.jsonify(error="Unknown error: %s" % e.args[0])
                    response.status_code = 400
                    return flask.abort(response)

                return flask.jsonify(success=True, is_on=smart_plug.attributes.is_on)
            else:
                return flask.abort(400, "Error: Missing data for testConnection")
        else:
            self._logger.error("Unknown command: %s" % command)



    def sendChallenge(self, ip_address):
        code_verifier = dirigera_auth.random_code(dirigera_auth.ALPHABET, dirigera_auth.CODE_LENGTH)
        auth_url = f"https://{ip_address}:8443/v1/oauth/authorize"
        params = {
            "audience": "homesmart.local",
            "response_type": "code",
            "code_challenge": dirigera_auth.code_challenge(code_verifier),
            "code_challenge_method": "S256",
        }
        error = "Unknown Error"
        response = {}
        try:
            response = requests.get(auth_url, params=params, verify=False, timeout=10)
        except requests.exceptions.ConnectTimeout as e:
            error = "Timeout. Check that the IP address is correct and that the device is on"
            return dict(
                error=error
            )
        except Exception as e:
            error = "Unexpected Error: %s" % e
            return dict(
                error=error
            )

        json = response.json()
        if response.status_code != 200:

            if "error" in json:
                error = "Error: %s" % json["error"]
            else:
                error = "Unexpected Error: %s" % json
            return dict(
                error=error
            )
        if "code" not in json:
            error = "Unexpected Response: %s" % json
        return dict(
            code=json["code"],
            code_verifier=code_verifier,
        )

    def getToken(self, ip_address, code, code_verifier):
        data = str(
            "code="
            + code
            + "&name="
            + socket.gethostname()
            + "&grant_type="
            + "authorization_code"
            + "&code_verifier="
            + code_verifier
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_url = f"https://{ip_address}:8443/v1/oauth/token"

        response = {}
        try:
            response = requests.post(token_url, headers=headers, data=data, verify=False, timeout=10)
        except requests.exceptions.ConnectTimeout as e:
            error = "Timeout. Check that the IP address is correct and that the device is on"
            return dict(
                error=error
            )
        except Exception as e:
            error = "Unexpected Error: %s" % e
            return dict(
                error=error
            )

        json = response.json()
        if response.status_code != 200:
            if "error" in json:
                error = "Error: %s" % json["error"]
            else:
                error = "Unexpected Error: %s" % json
            return dict(
                error=error
            )
        if "access_token" not in json:
            error = "Unexpected Response: %s" % json
        return dict(
            token=json["access_token"]
        )

    ##def get_template_configs(self):
    ##    return [
    ##        dict(type="settings", custom_bindings=False)
    ##    ]

    ##~~ Softwareupdate hook
    def get_assets(self):
        return dict(
            js=["js/psucontrol_ikea_dirigera.js"],
            css=["css/psucontrol_ikea_dirigera.css"]
        )
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "PSU_Control_IKEA_Dirigera": {
                "displayName": "PSU Control - IKEA Dirigera Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "Mesterkaa",
                "repo": "OctoPrint-PSU_Control_IKEA_Dirigera",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/Mesterkaa/OctoPrint-PSU_Control_IKEA_Dirigera/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "PSU Control - IKEA Dirigera"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Psu_control_ikea_dirigeraPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
