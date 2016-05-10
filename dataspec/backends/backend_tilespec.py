'''backend_tilespec.py - a dataspec backend for loading tilespec .json files

'''

import cv2
from dataspec import Tilespec, BoundingBox, LoaderCannotReadException
from dataspec.utils import url_to_file
import json
import os

class TSTilespec(Tilespec):
    '''JSON tilespec backend'''
    
    def __init__(self, d):
        '''Initialize with dictionary from the JSON file'''
        self.__d = d
    
    def get_bounding_box(self):
        return BoundingBox(*self.__d["bbox"])
    
    def imread(self, bounding_box=None, mipmap_level=0):
        mipmap_levels = self.__d["mipmapLevels"]
        best_level = -1
        for level, d in mipmap_levels.items():
            level = int(level)
            if level <= mipmap_level and level > best_level:
                best_level = level
                image_url = d["imageUrl"]
        if best_level == -1:
            raise IndexError(
                "Unable to find suitable mipmap level <= %d in %s" %
                (mipmap_level, repr(self)))
        w = 2**(mipmap_level - best_level)
        with url_to_file(image_url) as filename:
            img = cv2.imread(filename, flags=cv2.IMREAD_GRAYSCALE)
            if bounding_box is None:
                return img[::w, ::w]
            return img[bounding_box.y0:bounding_box.y1:w,
                       bounding_box.x0:bounding_box.x1:w]
        
    def get_tile_index(self):
        return self.__d["tile_index"]
    
    def get_mfov(self):
        return self.__d["mfov"]
    
    def get_layer(self):
        return self.__d["layer"]
    
    def get_max_intensity(self):
        return self.__d["maxIntensity"]
    
    def get_min_intensity(self):
        return self.__d["minIntensity"]
    
    def get_transforms(self):
        return self.__d["transforms"]
    
    def get_width(self):
        return self.__d["width"]
    
    def get_height(self):
        return self.__d["height"]
    
    def get_dataset(self, filename):
        # TODO: standardize locations for analysis files relative to tilespec dir
        super(self, TSTilespec).get_dataset(self, filename)
        
    def get_data(self, filename):
        # TODO: standardize locations for analysis files relative to tilespec dir
        super(self, TSTilespec).get_data(self, filename)

def load_tilespec(path):
    '''Load a single tilespec file
    
    A generator, yielding the tilespecs in the file in turn
    '''
    with open(path, "r") as fp:
        try:
            tss = json.load(fp)
        except ValueError:
            raise LoaderCannotReadException()
        for ts in tss:
            yield TSTilespec(ts)

def load(path):
    '''Load all tilespecs in the given directory or single tilespec
    
    :param path: path to tilespec
    '''
    if os.path.isdir(path):
        return [load_tilespec(os.path.join(path, filename))
                for filename in os.listdir(path)]
    elif os.path.isfile(path):
        return [load_tilespec(path)]
    else:
        raise LoaderCannotReadException()
