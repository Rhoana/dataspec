from boundingbox import BoundingBox
from tilespec import Tilespec
from loader import can_load, load, set_loader_name, DATASPEC_GROUP
import utils


class LoaderCannotReadException(Exception):
    '''Indicates that a given loader cannot read tilespecs from a path

    loaders are tried in turn and each one should throw this exception if
    it is unable to read tilespecs from the given path
    '''
    pass
all = [DATASPEC_GROUP, can_load, load, set_loader_name, utils, BoundingBox,
       LoaderCannotReadException, Tilespec]
