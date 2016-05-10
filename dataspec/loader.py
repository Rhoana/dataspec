'''loader.py - pick the correct backend for loading a tilespec'''

import pkg_resources

'''Entry point group name for registering tilespec loaders'''
DATASPEC_GROUP = 'org.rhoana.dataspec'

loader_name = None


def set_loader_name(name):
    '''Set the name of a specific entry point to always be used for loading

    By default, all loaders registered as entry points using the DATASPEC_GROUP
    group name are tried, in undefined order, until one is found that can open
    the path. Call this to restrict it to a single entry point.

    :param name: the loader name as defined in setuptools.setup's entry_points.
        Set the loader name to None to restore the default behavior.
    '''
    global loader_name
    loader_name = name


def get_loader_name():
    '''Return the current loader name'''
    return loader_name


def load(path):
    '''Given a path of some kind, try every backend to load it

    :param path: the URL of the tilespec to be loaded

    :returns: a sequence (or generator) of sequences of tiles (the top-level
        sequence represents a sequence of sections)
    '''
    working_set = pkg_resources.WorkingSet()
    for entry_point in working_set.iter_entry_points(DATASPEC_GROUP):
        if loader_name is not None and entry_point.name != loader_name:
            continue
        fn = entry_point.resolve()
        result = fn(path)
        if result is not None:
            return result
    raise NotImplementedError("No loader for tilespec %s" % path)

all = [DATASPEC_GROUP, load, set_loader_name]
