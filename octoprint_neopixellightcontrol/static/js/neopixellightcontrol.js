/*
 * View model for OctoPrint-Neopixellightcontrol
 *
 * Author: Lucas Haertel
 * License: GNU
 */
$(function() {
    function NeopixellightcontrolViewModel(parameters) {
        var self = this;
        self.settings = parameters[0]
        self.color = ko.observable()
        self.isOn = ko.observable(false)

        self.updateColor = function(picker, event) {
            var newColor = event.currentTarget.jscolor.toHEXString()
            if(newColor) {
                self.color(newColor)
                OctoPrint.simpleApiCommand('neopixellightcontrol', 'update_color', {'color': newColor})
            }
        }

        self.saveColor = function(picker, event) {
            var newColor = event.currentTarget.jscolor.toHEXString()
            if(newColor) {
                self.color(newColor)
                OctoPrint.simpleApiCommand('neopixellightcontrol', 'update_color', {'color': newColor})
                OctoPrint.settings.savePluginSettings('neopixellightcontrol', {'color': newColor})
            }
        }

        self.turnOn = function(){
            self.isOn(true)
            OctoPrint.simpleApiCommand('neopixellightcontrol', 'turn_on')
            OctoPrint.settings.savePluginSettings('neopixellightcontrol', {'is_on': true})
        }

        self.turnOff = function() {
            self.isOn(false)
            OctoPrint.simpleApiCommand('neopixellightcontrol', 'turn_off')
            OctoPrint.settings.savePluginSettings('neopixellightcontrol', {'is_on': false})
        }

        self.onBeforeBinding = function() {
            self.color(self.settings.settings.plugins.neopixellightcontrol.color())
            self.isOn(self.settings.settings.plugins.neopixellightcontrol.is_on()) 
            document.querySelector('#color-picker-control').jscolor.fromString(self.color())
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if(plugin != 'neopixellightcontrol') { return }
            if(data.hasOwnProperty('is_on')) {
                self.isOn(data.is_on)
            }
            if(data.hasOwnProperty('color')) {
                self.color(data.color)
                document.querySelector('#color-picker-control').jscolor.fromString(self.color())
            }
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: NeopixellightcontrolViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#sidebar_plugin_neopixellightcontrol"]
    });
});
