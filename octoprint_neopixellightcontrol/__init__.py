# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from rpi_ws281x import *


class NeopixellightcontrolPlugin(octoprint.plugin.SettingsPlugin,
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
        self._logger.info("LEDs initialized")
        self._logger.info("count " + self._settings.get_int(["led_count"]))
        self._logger.info("pin " + self._settings.get_int(["color_pin"]))
        self._logger.info("freq " + self._settings.get_int(["freqHz"]))
        self._logger.info("dma " + self._settings.get_int(["led_dma"]))
        self._logger.info("invert " + self._settings.get_boolean(["invert"]))
        self._logger.info(
            "brightness " + self._settings.get_int(["led_brightness"]))
        self._logger.info(
            "ledChannel " + self._settings.get_int(["led_channel"]))
        # self.strip = Adafruit_NeoPixel(self._settings.get_int(["led_count"]), self._settings.get_int(["color_pin"]), self._settings.get_int(["freqHz"]),
        #                                self._settings.get_int(["led_dma"]), self._settings.get_boolean(["invert"]), self._settings.get_int(["led_brightness"]), self._settings.get_int(["led_channel"]))
        # self.strip.begin()
        # self._logger.info("LEDs initialized")

    def update_rgb(self, colorHex, is_on):
        if(self.strip is not None):
            rgb = self.hex_to_rgb(colorHex)
            self._logger.info("RGB Value: " + rgb)
            r = rgb[0]
            self._logger.info("R Value: " + r)
            g = rgb[1]
            b = rgb[2]
            col = Color(r, g, b)
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, col)
                self.strip.show()
        else:
            self._logger.error("Error occurred while updating RGB state")

    def get_settings_defaults(self):
        return dict(
            strip=None,
            color_pin=18,
            power_ctrl=20,
            color='#FFFFFF',
            led_count=0,
            led_dma=10,
            freqHz=800000,
            led_brightness=0,
            led_channel=0,
            invert=False,
            is_on=False
        )

    def on_settings_save(self, data):
        self._logger.info("on_settings_save")
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        is_on = self._settings.get_boolean(["is_on"])
        if is_on is not None:
                self.is_on = is_on
        self.init_rgb()

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
        self._logger.info("CMD: " + command)
        if command == "update_color":
            color = data.get('color', None)
            if color != None:
                self.color = color
        elif command == "turn_on":
            self.is_on = True
        elif command == "turn_off":
            self.is_on = False
        # self.update_rgb(self.color, self.is_on)

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
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
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = NeopixellightcontrolPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
