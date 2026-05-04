# -*- coding: utf-8 -*-
from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name="pioreactor-electropioreactor-plugin",
    version="0.6.5",
    license="MIT",
    license_files=("LICENSE.txt",),
    description="Electrolysis and CO₂ sparging control for electroPioreactors.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Martin Currie",
    author_email="martin@amybo.org",
    url="https://github.com/amy-bo/electroPioreactor",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click"],
    extras_require={"dev": ["pytest>=7"]},
    entry_points={
        "pioreactor.plugins": "pioreactor_electropioreactor_plugin = pioreactor_electropioreactor_plugin"
    },
)
