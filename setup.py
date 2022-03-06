from setuptools import setup
import os
from freecad.estimateWB.version import __version__
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "freecad", "estimateWB", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.estimateWB',
      version=str(__version__),
      packages=['freecad',
                'freecad.estimateWB'],
      maintainer="error on line 1",
      maintainer_email="dev@erroronline.one",
      url="https://github.com/erroronline1/estimateWB",
      description="estimate material quantity",
      install_requires=[],  # should be satisfied by FreeCAD's system dependencies already
      include_package_data=True)
