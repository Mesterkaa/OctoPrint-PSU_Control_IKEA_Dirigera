$(function() {
    function PSUDirigeraViewModel(parameters) {

        this.settings = parameters[0];

        this.code = ""
        this.code_verifier = ""

        this.Token = ko.observable();
        this.IP = ko.observable();
        this.Outlet_Name = ko.observable();


        this.SendChallengeSuccess = ko.observable("");
        this.SendChallengeSent = ko.observable("false");
        this.sendChallengeResponse = ko.observable("");
        this.GetTokenSuccess = ko.observable("");
        this.getTokenSent = ko.observable("false");
        this.getTokenResponse = ko.observable("");

        this.sendChallenge = function() {
            if (this.IP() == undefined || this.IP() == "") {
                console.warn("IP is empty");
                return;
            }


            this.ClearGetToken();
            this.ClearSendChallenge();
            this.SendChallengeSent("true");

            OctoPrint.simpleApiCommand('psucontrol_ikea_dirigera', 'sendChallenge', {ip_address: this.IP()})
            .done((response) => {

                this.sendChallengeResponse(JSON.stringify(response));
                this.SendChallengeSuccess("true");

                this.code = response["code"];
                this.code_verifier = response["code_verifier"];
            })
            .fail((response) => {
                console.log(response);
                var error = response.responseJSON.error;
                this.sendChallengeResponse(JSON.stringify(error));
                this.SendChallengeSuccess("false");
            });

        };
        this.getToken = function() {
            if (this.IP() == undefined || this.IP() == "") {
                console.warn("IP is empty");
                return;
            }
            this.ClearGetToken()
            this.getTokenSent("true");

            OctoPrint.simpleApiCommand('psucontrol_ikea_dirigera', 'getToken', {ip_address: this.IP(), code: this.code, code_verifier: this.code_verifier})
            .done((response) => {
                this.getTokenResponse(JSON.stringify(response));
                this.GetTokenSuccess("true");

                this.Token(response["token"]);
                this.Token(response["token"])
            })
            .fail((response) => {
                var error = response.responseJSON.error;
                this.getTokenResponse(JSON.stringify(error));
                this.GetTokenSuccess("false");
            });

        }

        this.ClearSendChallenge = function() {
            this.SendChallengeSuccess("");
            this.SendChallengeSent("false");
            this.sendChallengeResponse("");
        }
        this.ClearGetToken = function() {
            this.GetTokenSuccess("");
            this.getTokenSent("false");
            this.getTokenResponse("");
        }


        this.testConnectionSent = ko.observable("false");
        this.testConnectionResponse = ko.observable("");
        this.testConnectionSuccess = ko.observable("");
        this.testConnectionIsOutletOn = ko.observable("");
        this.testConnection = function() {

            this.testConnectionSuccess("");
            this.testConnectionResponse("");
            this.testConnectionIsOutletOn("");
            this.testConnectionSent("true");

            OctoPrint.simpleApiCommand('psucontrol_ikea_dirigera', 'testConnection', {ip_address: this.IP(), token: this.Token(), outlet_name: this.Outlet_Name()})
            .done((response) => {
                this.testConnectionResponse(JSON.stringify(response));
                this.testConnectionSuccess("true");
                this.testConnectionIsOutletOn(response["is_on"]);
                console.log(response);
            })
            .fail((response) => {
                var error = response.responseJSON.error;

                this.testConnectionResponse(JSON.stringify(error));
                this.testConnectionSuccess("false");
            });
        }
        // This will get called before the HelloWorldViewModel gets bound to the DOM, but after its
        // dependencies have already been initialized. It is especially guaranteed that this method
        // gets called _after_ the settings have been retrieved from the OctoPrint backend and thus
        // the SettingsViewModel been properly populated.
        this.onBeforeBinding = function() {
            this.IP(this.settings.settings.plugins.psucontrol_ikea_dirigera.IP());
            this.Outlet_Name(this.settings.settings.plugins.psucontrol_ikea_dirigera.Outlet_Name());
            this.Token(this.settings.settings.plugins.psucontrol_ikea_dirigera.Token());
        }
        this.onSettingsBeforeSave = function() {
            this.settings.settings.plugins.psucontrol_ikea_dirigera.IP(this.IP())
            this.settings.settings.plugins.psucontrol_ikea_dirigera.Outlet_Name(this.Outlet_Name())
            this.settings.settings.plugins.psucontrol_ikea_dirigera.Token(this.Token())
            console.log("onSettingsBeforeSave IKEA");
        }


    }

    // This is how our plugin registers itthis with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push({
        // This is the constructor to call for instantiating the plugin
        construct: PSUDirigeraViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        dependencies: ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        elements: ["#settings_plugin_psucontrol_ikea_dirigera"]
    });
});
