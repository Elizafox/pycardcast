#!/usr/bin/env python3

from setuptools import setup

long_description = (
    """A flexible wrapper around the Cardcast API. It has been designed to be
    portable to multiple I/O backends with minimal effort."""
)

setup(name="pycardcast",
      version="1.0a1",
      description="A Python wrapper around the Cardcast API",
      long_description=long_description,
      keywords="cardcast cardsagainsthumanity cah development",
      author="Elizabeth Myers",
      author_email="elizabeth@interlinked.me",
      url="https://github.com/Elizafox/pycardcast",
      packages=["pycardcast", "pycardcast.net"],
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Developers",
          "Topic :: Games/Entertainment",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.4",
          "Operating System :: OS Independent",
          "License :: DFSG approved",
      ]
)
