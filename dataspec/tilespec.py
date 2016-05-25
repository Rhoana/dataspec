'''tilespec.py - metadata for a tile'''


class Tilespec(object):
    '''Abstract tilespec

    '''

    def get_bounding_box(self):
        '''Get the bounding box around the tile

        :returns: A BoundingBox giving the global extents of the tile
        '''
        raise NotImplementedError()

    @property
    def bbox(self):
        return self.get_bounding_box()

    def imread(self, bounding_box=None, mipmap_level=0):
        '''Read the image associated with this tile

        :param bounding_box: the bounding box to read relative to the tile's
            image (e.g. (0, 0, 100, 200) gets a tile starting at the image's
            origin having width of 100 and  height of 200)
        :param mipmap_level: the decimation level - shrink the image by
            2 ** mipmap_level.
        '''
        raise NotImplementedError()

    def get_tile_index(self):
        '''Return the index of the tile within the MFOV'''
        raise NotImplementedError()

    @property
    def tile_index(self):
        '''Return the index of the tile within the MFOV'''
        return self.get_tile_index()

    def get_mfov(self):
        '''Return the mfov index within the section'''
        raise NotImplementedError()

    @property
    def mfov(self):
        '''Return the mfov index within the section'''
        return self.get_mfov()

    def get_layer(self):
        '''Return the Z layer of the tile's section'''
        raise NotImplementedError()

    @property
    def layer(self):
        return self.get_layer()

    def get_max_intensity(self):
        '''Return the maximum intensity value possible in an image'''
        raise NotImplementedError

    @property
    def max_intensity(self):
        '''Return the maximum intensity value possible in an image'''
        return self.get_max_intensity()

    def get_min_intensity(self):
        '''Return the minimum intensity value possible in the image'''
        raise NotImplementedError()

    @property
    def min_intensity(self):
        '''Return the minimum intensity value possible in the image'''
        return self.get_min_intensity()

    def get_transforms(self):
        '''Get the transforms that map the tile into the global image space

        :returns: a sequence of Transform instances
        '''
        raise NotImplementedError()

    @property
    def transforms(self):
        '''Get the transforms that map the tile into the global image space

        :returns: a sequence of transforms in the tilespec data format
             used by rh_renderer.models.Transforms
        '''
        return self.get_transforms()

    def get_width(self):
        '''Return the width of the tile in pixels'''
        raise NotImplementedError()

    @property
    def width(self):
        '''Return the width of the tile in pixels'''
        return self.get_width()

    def get_height(self):
        '''Return the height of the tile in pixels'''
        raise NotImplementedError()

    @property
    def height(self):
        '''Return the height of the tile in pixels'''
        return self.get_height()

    def get_dataset(self, filename):
        '''Read and return a dataset from within an HDF5 file

        :param filename: a relative-path filename of some data item. The
             driver should know how to use the filename and tilespec context
             to retrieve the file.

        :returns: a numpy array containing the dataset
        '''
        raise NotImplementedError()

    def get_data(self, filename):
        '''Read and return the data from within a file

        :param filename: a relative-path filename of some data item.

        :returns: a buffer containing the file's data
        '''
        raise NotImplementedError()

    def __repr__(self):
        return "Tilespec %d:%d:%d" % (self.layer, self.mfov, self.tile_index)
