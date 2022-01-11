# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from rpi_ws281x import *


class NeopixellightcontrolPlugin(octoprint.plugin.StartupPlugin,
                                 octoprint.plugin.SettingsPlugin,
                                 octoprint.plugin.AssetPlugin,
                                 octoprint.plugin.TemplatePlugin,
                                 octoprint.plugin.SimpleApiPlugin):

    def __init__(self):
        self.strip = None
        self.colorPin = 18
        self.powerPin = 20
        self.color = '#FFFFFF'
        self.ledCount = 0
        self.dmaChannel = 10
        self.freqHz = 800000
        self.brightness = 0
        self.ledChannel = 0
        self.invert = False
        self.is_on = False

    def init_rgb(self):
        try:
            self.deinit_rgb()
            self.strip = Adafruit_NeoPixel(
                self.ledCount, self.colorPin, self.freqHz, self.dmaChannel, self.invert, self.brightness, self.ledChannel)
            self.strip.begin()
            self._logger.info("LEDs initialized")
        except:
            self._logger.error("Error occurred while initializing LEDs")

    def deinit_rgb(self):
        try:
            if(self.strip is not None):
                self.strip._cleanup()
                self.led = None
                self._logger.info("LEDs deinitialized")
        except:
            self._logger.error("Error occurred while deinitializing LEDs")

    def update_rgb(self, colorHex, is_on):
        if(self.strip is not None):
            col = Color(self.hex_to_rgb(colorHex)[0], self.hex_to_rgb(
                colorHex)[1], self.hex_to_rgb(colorHex)[2])
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, col)
                self.strip.show()
        else:
            self._logger.error("Error occurred while updating RGB state")

    def on_after_startup(self):
        colorPin = self._settings.get_int(["color_pin"])
        if colorPin is not None:
            self.colorPin = colorPin
        powerPin = self._settings.get_int(["power_ctrl"])
        if powerPin is not None:
            self.powerPin = powerPin
        color = self._settings.get(["color"])
        if color is not None:
            self.color = color
        ledCount = self._settings.get_int(["led_count"])
        if ledCount is not None:
            self.ledCount = ledCount
        dmaChannel = self._settings.get_int(["led_dma"])
        if dmaChannel is not None:
            self.dmaChannel = dmaChannel
        brightness = self._settings.get_int(["led_brightness"])
        if brightness is not None:
            self.brightness = brightness
        ledChannel = self._settings.get_int(["led_channel"])
        if ledChannel is not None:
            self.ledChannel = ledChannel
        is_on = self._settings.get_boolean(["is_on"])
        if is_on is not None:
            self.is_on = is_on
        if colorPin is not None and color is not None and ledCount is not None and dmaChannel is not None and brightness is not None and ledChannel is not None:
            self.init_rgb()
        if is_on is not None and color is not None:
            self.update_rgb(self.color, self.is_on)
        #self._plugin_manager.send_plugin_message(self._identifier, dict(is_on=self.is_on, color=self.color))

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        colorPin = self._settings.get_int(["color_pin"])
        if colorPin is not None:
            self.colorPin = colorPin
        powerPin = self._settings.get_int(["power_ctrl"])
        if powerPin is not None:
            self.powerPin = powerPin
        color = self._settings.get(["color"])
        if color is not None:
            self.color = color
        ledCount = self._settings.get_int(["led_count"])
        if ledCount is not None:
            self.ledCount = ledCount
        dmaChannel = self._settings.get_int(["led_dma"])
        if dmaChannel is not None:
            self.dmaChannel = dmaChannel
        brightness = self._settings.get_int(["led_brightness"])
        if brightness is not None:
            self.brightness = brightness
        ledChannel = self._settings.get_int(["led_channel"])
        if ledChannel is not None:
            self.ledChannel = ledChannel
        is_on = self._settings.get_boolean(["is_on"])
        if is_on is not None:
            self.is_on = is_on
        if colorPin is not None and color is not None and ledCount is not None and dmaChannel is not None and brightness is not None and ledChannel is not None:
            self.init_rgb()
        if is_on is not None and color is not None:
            self.update_rgb(self.color, self.is_on)

    def get_settings_defaults(self):
        return dict(
            strip=None,
            colorPin=18,
            powerPin=20,
            color='#FFFFFF',
            ledCount=0,
            dmaChannel=10,
            freqHz=800000,
            brightness=0,
            ledChannel=0,
            invert=False,
            is_on=False
        )

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/neopixellightcontrol.js",  "js/jscolor.min.js"],
            css=["css/neopixellightcontrol.css"],
            less=["less/neopixellightcontrol.less"]
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_api_commands(self):
        return dict(
            update_color=["color"],
            turn_on=[],
            turn_off=[]
        )

    def on_api_command(self, command, data):
        if command == "update_color":
            color = data.get('color', None)
            if color != None:
                self.color = color
        elif command == "turn_on":
            self.is_on = True
        elif command == "turn_off":
            self.is_on = False
        self.update_rgb(self.color, self.is_on)

    def hex_to_rgb(value):
        value = value.lstrip('#')
        value = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    # ~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "neopixellightcontrol": {
                "displayName": "Neopixellightcontrol Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "lucashaertel",
                "repo": "OctoPrint-Neopixellightcontrol",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/lucashaertel/OctoPrint-Neopixellightcontrol/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Neopixellightcontrol Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = NeopixellightcontrolPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
