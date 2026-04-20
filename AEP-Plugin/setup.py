# -*- coding: utf-8 -*-
from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name="pioreactor-aep-plugin",
    version="0.1.0",
    license="MIT",
    license_files=("LICENSE.txt",),
    description="CO₂ sparging and electrolysis power control for the Aseptic ElectroPioreactor.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Martin Currie",
    author_email="martin@amybo.org",
    url="https://github.com/amybo-org/pioreactor-aep-plugin",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "pioreactor.plugins": "pioreactor_aep_plugin = pioreactor_aep_plugin"
    },
)
