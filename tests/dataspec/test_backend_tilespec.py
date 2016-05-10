'''test_backend_tilespec.py - test the tilespec backend'''

import cv2
import dataspec
import dataspec.loader
import json
import numpy as np
import os
import tempfile
import urllib
import unittest


class TestBackendTilespec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        os.mkdir(os.path.join(cls.tempdir, "tilespecs"))
        m0t1_path = os.path.abspath(os.path.join(cls.tempdir, "m0t1.bmp"))
        m2t1_path = os.path.abspath(os.path.join(cls.tempdir, "m2t1.bmp"))
        m0t2_path = os.path.abspath(os.path.join(cls.tempdir, "m0t2.bmp"))
        cv2.imwrite(
            m0t1_path, np.arange(128*256).reshape(128, 256).astype(np.uint8))
        cv2.imwrite(m2t1_path, np.ones((32, 64), np.uint8))
        cv2.imwrite(m0t2_path, np.ones((128, 256), np.uint8))
        cls.tilespec_path = os.path.join(cls.tempdir, "tilespecs",
                                         "W01_Sec001.json")
        tilespec = [
            {
                "bbox": [
                    37739.197000000626,
                    40867.197000000626,
                    10421.167000000365,
                    13145.167000000365
                    ],
                "height": 2724,
                "layer": 2,
                "maxIntensity": 255.0,
                "mfov": 1,
                "minIntensity": 0.0,
                "mipmapLevels": {
                    "0": {
                        "imageUrl": "file://" + urllib.pathname2url(m0t1_path)
                        },
                    "2": {
                        "imageUrl": "file://" + urllib.pathname2url(m2t1_path)
                    }
                    },
                "tile_index": 1,
                "transforms": [
                    {
                        "className":
                            "mpicbg.trakem2.transform.TranslationModel2D",
                        "dataString": "37739.197 10421.167"
                    }
                    ],
                "width": 3128
                },
            {
                "bbox": [
                    40744.574000000954,
                    43872.574000000954,
                    10419.305999999866,
                    13143.305999999866
                    ],
                "height": 2724,
                "layer": 2,
                "maxIntensity": 255.0,
                "mfov": 1,
                "minIntensity": 0.0,
                "mipmapLevels": {
                    "0": {
                        "imageUrl": "file://" + urllib.pathname2url(m0t2_path)
                    }
                    },
                "tile_index": 2,
                "transforms": [
                    {
                        "className":
                            "mpicbg.trakem2.transform.TranslationModel2D",
                        "dataString": "40744.574 10419.306"
                    }
                    ],
                "width": 3128
                },
        ]
        with open(cls.tilespec_path, "w") as fp:
            json.dump(tilespec, fp)
        cls.old_loader_name = dataspec.loader.get_loader_name()
        dataspec.set_loader_name("tilespec")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.tilespec_path)
        os.rmdir(os.path.dirname(cls.tilespec_path))
        for filename in os.listdir(cls.tempdir):
            os.remove(os.path.join(cls.tempdir, filename))
        os.rmdir(cls.tempdir)
        dataspec.set_loader_name(cls.old_loader_name)

    def test_01_load_dir(self):
        #
        # Load the tilespec and succeed if there was no exception
        #
        result = dataspec.load(os.path.dirname(self.tilespec_path))
        self.assertEqual(len(result), 1)

    def test_02_load_file(self):
        #
        # Load a tilespec file and succeed if there was no exception
        #
        result = [list(_) for _ in dataspec.load(self.tilespec_path)]
        self.assertEqual(len(result), 1)

    def test_03_cant_load(self):
        #
        # Make sure loader fails correctly on unreadable
        #
        self.assertRaises(dataspec.LoaderCannotReadException,
                          dataspec.load, "/foo/bar")

    def test_04_metadata(self):
        #
        # Read through a tilespec's metadata
        #
        for section in dataspec.load(self.tilespec_path):
            for ts in section:
                self.assertEqual(ts.mfov, 1)
                self.assertEqual(ts.layer, 2)
                self.assertEqual(ts.width, 3128)
                self.assertEqual(ts.height, 2724)
                self.assertEqual(ts.min_intensity, 0)
                self.assertEqual(ts.max_intensity, 255)
                self.assertIn(ts.tile_index, (1, 2))
                if ts.tile_index == 1:
                    self.assertAlmostEqual(ts.bbox.x0, 37739.197,
                                           delta=0.001)
                    transforms = ts.transforms
                    self.assertEqual(len(transforms), 1)
                    self.assertEqual(
                        transforms[0]["className"],
                        "mpicbg.trakem2.transform.TranslationModel2D")
                    self.assertEqual(
                        transforms[0]["dataString"],
                        "37739.197 10421.167")

    def test_05_read(self):
        ts = list(list(dataspec.load(self.tilespec_path))[0])[0]
        img = ts.imread()
        np.testing.assert_array_equal(
            img, np.arange(128*256).reshape(128, 256).astype(np.uint8))

    def test_06_read_mipmap_0(self):
        ts = list(list(dataspec.load(self.tilespec_path))[0])[0]
        img = ts.imread(mipmap_level=0)
        np.testing.assert_array_equal(
            img, np.arange(128*256).reshape(128, 256).astype(np.uint8))

    def test_07_read_mipmap_1(self):
        ts = list(list(dataspec.load(self.tilespec_path))[0])[0]
        img = ts.imread(mipmap_level=1)
        expected = np.arange(128*256).reshape(128, 256)\
            .astype(np.uint8)[::2, ::2]
        np.testing.assert_array_equal(img, expected)

    def test_08_read_mipmap_2(self):
        ts = list(list(dataspec.load(self.tilespec_path))[0])[0]
        img = ts.imread(mipmap_level=2)
        np.testing.assert_array_equal(img, 1)
        self.assertSequenceEqual(img.shape, (32, 64))

    def test_09_read_crop(self):
        ts = list(list(dataspec.load(self.tilespec_path))[0])[0]
        bbox = dataspec.BoundingBox(10, 20, 20, 30)
        expected = np.arange(128*256).reshape(128, 256)\
            .astype(np.uint8)[20:30, 10:20]
        np.testing.assert_array_equal(ts.imread(bounding_box=bbox), expected)
