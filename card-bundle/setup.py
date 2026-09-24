from setuptools import setup

setup(
    name="aep02-profile",
    version="1.0.0",
    description="AEP0.2 unit profile: XR photodiode channels and model, applied at install",
    packages=["aep02_profile"],
    include_package_data=True,
    package_data={"aep02_profile": ["additional_config.ini", "post_install.sh"]},
    entry_points={"pioreactor.plugins": "aep02_profile = aep02_profile"},
)
