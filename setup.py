from setuptools import setup
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

setup(
    name = 'freecad.estimateWB',
    version = "0.1.4",
    packages = ['freecad',
        'freecad.estimateWB'],
    maintainer = "error on line 1",
    maintainer_email = "dev@erroronline.one",
    url = "https://github.com/erroronline1/estimateWB",
    description = "estimate the volume & weight of parts",
    install_requires = [],  # should be satisfied by FreeCAD's system dependencies already
    include_package_data = True)
