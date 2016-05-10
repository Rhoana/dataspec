from dataspec import BoundingBox
import unittest


class TestBoundingBox(unittest.TestCase):

    def test_01_extents(self):
        bb = BoundingBox(1, 2, 3, 4)
        self.assertEqual(bb.x0, 1)
        self.assertEqual(bb.x1, 2)
        self.assertEqual(bb.y0, 3)
        self.assertEqual(bb.y1, 4)

    def test_02_width(self):
        bb = BoundingBox(1, 4, 9, 16)
        self.assertEqual(bb.width, 3)

    def test_03_height(self):
        bb = BoundingBox(1, 4, 9, 16)
        self.assertEqual(bb.height, 7)
