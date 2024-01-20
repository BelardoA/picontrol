#!/usr/bin/python3
# fan.py
"""Enables fan control for PiControl."""
# import RPi.GPIO as GPIO
import os
import asyncio
import multiprocessing
from typing import Union

from config import Config


class Fan:
    """
    Class to control fan based on CPU temperature.
    """
    def __init__(self, queue: multiprocessing.Queue):
        _instance = None
        # Prevent multiple instances of Fan from being created

        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(Fan, cls).__new__(cls, *args, **kwargs)
            return cls._instance

        self.pi_version = Config().get_pi_model()
        self.cpu_temp = self.get_cpu_temp()
        self.fan_settings = Config().fan_settings
        self.threshold_on = self.fan_settings["threshold_on"]
        self.threshold_off = self.fan_settings["threshold_off"]
        self.interval = self.fan_settings["interval"]
        self.gpio_fan = 18
        # self.set_gpio()
        self.fan_on = False
        self.queue = queue
        self.loop = multiprocessing.Process(target=self.run)
        self.loop.start()

    def run(self):
        """
        Run the fan control loop.

        :return: None
        """
        asyncio.run(self.start_loop())

    def return_dict(self) -> dict:
        """
        Return current fan settings as a dictionary.

        :return: Dictionary of current fan settings.
        :rtype: dict
        """
        return {
            "threshold_on": self.threshold_on,
            "threshold_off": self.threshold_off,
            "interval": self.interval,
            "cpu_temp": self.cpu_temp,
            "fan_on": self.fan_on,
        }

    # def set_gpio(self) -> None:
    #     """
    #     Set GPIO mode and pin.
    #
    #     :return: None
    #     """
    #     if self.pi_version >= 4:
    #         self.gpio_fan = 17
    #     GPIO.setwarnings(False)
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(self.gpio_fan, GPIO.OUT)

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

    def get_cpu_temp(self) -> Union[float, str]:
        """
        Get CPU temperature from vcgencmd.

        :return: CPU temperature as a float.
        :rtype: float
        """
        import platform
        if not self.pi_version and platform.system() == "Linux":
            import psutil
            res = psutil.sensors_temperatures()["coretemp"][0].current
            return float(res)
        if self.pi_version and self.pi_version >= 4:
            import psutil
            res = psutil.sensors_temperatures()["cpu_thermal"][0].current
            return float(res)
        else:
            res = os.popen('vcgencmd measure_temp').readline()
            return res.replace("temp=", "").replace("'C\n", "")

    async def start_loop(self) -> None:
        """
        Start the fan control loop for detecting CPU temperature and controlling the fan.

        :return: None
        """
        while True:
            self.refresh_fan()
            if self.cpu_temp >= self.threshold_on:
                # GPIO.output(self.gpio_fan, 1)
                self.fan_on = True
            elif self.fan_on is True and self.cpu_temp <= self.threshold_off:
                # GPIO.output(self.gpio_fan, 0)
                self.fan_on = False

            # Put the updated values into the queue
            self.queue.put((self.cpu_temp, self.fan_on, self.interval))
            await asyncio.sleep(self.interval)
