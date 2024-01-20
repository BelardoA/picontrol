#!/usr/bin/python3
# fan.py
"""Enables fan control for PiControl."""
import RPi.GPIO as GPIO
import os
import time
from config import Config


class Fan:
    """
    Class to control fan based on CPU temperature.
    """
    def __init__(self):
        self.cpu_temp = 0
        self.fan_settings = Config().fan_settings
        self.threshold_on = self.fan_settings["threshold_on"]
        self.threshold_off = self.fan_settings["threshold_off"]
        self.interval = self.fan_settings["interval"]
        self.gpio_fan = 18
        self.set_gpio()
        self.fan_on = False
        self.start_loop()

    def set_gpio(self) -> None:
        """
        Set GPIO mode and pin.

        :return: None
        """
        model = Config().get_pi_model()
        if model >= 4:
            self.gpio_fan = 17
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_fan, GPIO.OUT)

    def refresh_fan(self) -> None:
        """
        Refresh CPU temperature and fan settings from Config.

        :return: None
        """
        config = Config()
        self.threshold_on = config.fan_settings["threshold_on"]
        self.threshold_off = config.fan_settings["threshold_off"]
        self.interval = config.fan_settings["interval"]
        self.cpu_temp = self.get_cpu_temp()

    @staticmethod
    def get_cpu_temp() -> float:
        """
        Get CPU temperature from vcgencmd.

        :return: CPU temperature as a float.
        :rtype: float
        """
        res = os.popen('vcgencmd measure_temp').readline()
        return float(res.replace("temp=", "").replace("'C\n", ""))

    def start_loop(self) -> None:
        """
        Start the fan control loop for detecting CPU temperature and controlling the fan.

        :return: None
        """
        while True:
            self.refresh_fan()
            if self.cpu_temp >= self.threshold_on:
                GPIO.output(self.gpio_fan, 1)
                self.fan_on = True
            else:
                if self.fan_on is True and self.cpu_temp <= self.threshold_off - 5:
                    GPIO.output(self.gpio_fan, 0)

            time.sleep(self.interval)
