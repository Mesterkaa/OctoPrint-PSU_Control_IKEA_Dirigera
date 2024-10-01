$(function() {
    function PSUDirigeraViewModel(parameters) {

        this.settings = parameters[0];

        this.code = ""
        this.code_verifier = ""

        this.Token = ko.observable();
        this.IP = ko.observable();
        this.Outlet_Name = ko.observable();

        // this will be called when the user clicks the "Go" button and set the iframe's URL to
        // the entered URL
        this.goToUrl = function() {
            this.currentUrl(this.newUrl());
        };
        this.sendChallenge = function() {
            console.log("Sending challenge");
            console.log(this.IP());
            if (this.IP() == undefined || this.IP() == "") {
                console.log("IP is empty");
                alert("IP is empty. Please enter the IP of the IKEA Dirigera device.");
                return;
            }
            OctoPrint.simpleApiCommand('PSU_Control_IKEA_Dirigera', 'sendChallenge', {ip_address: this.IP()})
            .done(function(result) {
                console.log(result);
                if (result["error"] != undefined) {
                    alert(result["error"]);
                }
                this.code = result["code"];
                this.code_verifier = result["code_verifier"];
            })
            .fail(function(error) {
                console.error("Failed to send challenge: ", error);
            });

        };
        this.getToken = function() {
            console.log("Getting token");
            console.log(this.IP());
            if (this.IP() == undefined || this.IP() == "") {
                console.log("IP is empty");
                alert("IP is empty. Please enter the IP of the IKEA Dirigera device.");
                return;
            }
            OctoPrint.simpleApiCommand('PSU_Control_IKEA_Dirigera', 'getToken', {ip_address: this.IP()})
            .done(function(result) {
                console.log(result);
                if (result["error"] != undefined) {
                    alert(result["error"]);
                }
                this.Token(result["token"]);
            })
            .fail(function(error) {
                console.error("Failed to get token: ", error);
            });

        }
        // This will get called before the HelloWorldViewModel gets bound to the DOM, but after its
        // dependencies have already been initialized. It is especially guaranteed that this method
        // gets called _after_ the settings have been retrieved from the OctoPrint backend and thus
        // the SettingsViewModel been properly populated.
        this.onBeforeBinding = function() {
            this.IP(this.settings.settings.plugins.psu_control_ikea_dirigera.IP());
            this.Outlet_Name(this.settings.settings.plugins.psu_control_ikea_dirigera.Outlet_Name());
            this.Token(this.settings.settings.plugins.psu_control_ikea_dirigera.Token());
            console.log(this);
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
        elements: ["#settings_plugin_psu_control_ikea_dirigera"]
    });
});
