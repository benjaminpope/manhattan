from numpy.distutils.core import setup, Extension
from numpy.distutils.misc_util import Configuration
import distutils.sysconfig as ds

long_description = ''

setup(name='csperiodograms',
      version='0.5',
      description='Compressed Sensing Periodograms',
      long_description=long_description,
      author='Benjamin Pope',
      author_email='benjamin.pope@nyu.edu',
      url='',
      package_dir={'csper':'src'},
      packages=['csper'],
      install_requires=["numpy", "astropy", "scipy"],
      license='GPLv3',
      classifiers=[
          "Topic :: Scientific/Engineering",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Programming Language :: Python"
      ]
     )
