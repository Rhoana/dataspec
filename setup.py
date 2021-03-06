import setuptools

from dataspec.loader import DATASPEC_GROUP

VERSION = "1.1.2"

setuptools.setup(
    description="Tilespec data model",
    dependency_links=[
        'http://github.com/Rhoana/rh_renderer/tarball/master'
        '#egg=rh_renderer-0.0.1'],
    entry_points={
        DATASPEC_GROUP: {
            "tilespec = dataspec.backends.backend_tilespec:load"
        }
    },
    install_requires=[
        "h5py>=2.5",
        "numpy>=1.6"
    ],
    name="dataspec",
    packages=["dataspec", "dataspec.backends"],
    url="https://github.com/Rhoana/dataspec",
    version=VERSION)
