# dataspec
Tilespec data model

This package provides an abstraction of the image and analysis data for
EM analysis. The baseline for this is the tilespec - a JSON file of the
locations of image tiles along with their transforms mapping into a 3D space.

Usage:

    import dataspec
    spec = dataspec.load("/data/Analysis/tilespecs")
    for section in spec:
        for mfov in section:
            for tilespec in mfov:
                img = tilespec.imread()
                # do something

The package comes with a default loader for JSON tilespecs. Additional loaders
can be used if they are registered as entry points for the `org.rhoana.dataspec`
group. The signature of a loader is the same as dataspec.load - the input
is a path and the output should yield a sequence of sequences of Tilespec
objects. If a loader cannot load tilespecs from a path, it should raise the
LoaderCannotReadException and dataspec.load will try additional registered
entry points until it finds one that can.
