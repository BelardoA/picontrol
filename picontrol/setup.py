#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""imports"""
from pathlib import Path

from setuptools import find_packages, setup

from picontrol import __version__

CWD = Path(__file__).resolve().parent
long_description = (CWD / "README.md").read_text(encoding="utf-8")


def _strip(file_name: str) -> str:
    """
    Strip text from a file

    :param str file_name: path to the filename to strip
    :return: stripped text from the provided file
    :rtype: str
    """
    return (CWD / file_name).read_text(encoding="utf-8").strip()


INSTALL_REQUIRES = [
    "wheel",
    "setuptools" "Adafruit-GPIO",
]

# Define requirement lists
PI3_REQUIRES = _strip("pi3-requirements.txt").split()
PI4_REQUIRES = [
    "flask<2.3",
    "jinja2",
]
PI5_REQUIRES = [
    "flask<2.3",
    "jinja2",
]

setup(
    name="PiControl",
    version=__version__,
    author="Anthony Belardo",
    author_email="anthonybelardo@gmail.com",
    license="MIT",
    description="PiControl is a Raspberry Pi using RetroPie & uses NFC tags to launch games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BelardoA/picontrol",
    packages=find_packages(),
    include_package_data=True,
    package_data={"regscale.core.server": ["static/**/*", "templates/*"]},
    setup_requires=["pyaml==21.10.1", "rich==12.6.0", "cython"],
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "PI3": PI3_REQUIRES,
        "PI4": PI4_REQUIRES,
        "PI5": PI5_REQUIRES,
    },
    python_requires=">=3.7",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
