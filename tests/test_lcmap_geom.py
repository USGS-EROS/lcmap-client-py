import json
import unittest

from lcmap_fakes import FakeLCMAPHTTP, FakeLCMAPRESTResponse

from lcmap.client import geom, serializer
from lcmap.client.api.data import surface_reflectance


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        params = {
            'band': 'LANDSAT_8/OLI_TIRS/sr_band2',
            'x':    -1850865,
            'y':     2956785,
            't1':   '2013-01-01',
            't2':   '2015-01-01'
        }
        # Load the saved data that was originally returned by running the above
        # query against the LCMAP REST service.
        data = json.load(open("tests/data/tiles-result-payload.json"))
        fake_resp = FakeLCMAPRESTResponse(data)
        fake_http = FakeLCMAPHTTP(fake_resp)
        sr = surface_reflectance.SurfaceReflectance(fake_http)
        (self.spec, self.tiles) = sr.tiles(**params)
        self.tile = self.tiles[0]
        self.xform_matrix = geom.get_transform_matrix(self.tile, self.spec)


class FakeObjectsTestCase(BaseTestCase):
    "Make sure that all the bits are set up properly."

    def test_spec(self):
        self.assertEqual(self.spec["data_shape"], [256, 256])

    def test_tiles(self):
        self.assertEqual(len(self.tiles), 2)

    def test_tile(self):
        self.assertEqual(type(self.tile).__name__, "Tile")
        self.assertEqual(self.tile.spec, self.spec)

    def test_xform_matrix(self):
        self.assertEqual(type(self.xform_matrix).__name__, "list")
        self.assertEqual(self.xform_matrix[0], -1850865)


class PublicFunctionsTestCase(BaseTestCase):

    def test_transform_coord_map_to_image_upper_left(self):
        coord = (-1850865, 2956785)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0,0))

    def test_transform_coord_map_to_image_upper_right(self):
        coord = (-1850865+(30*255), 2956785)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (255,0))

    def test_transform_coord_map_to_image_lower_left(self):
        coord = (-1850865, 2956785 + ((-30)*(256-1)))
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0,255))

    def test_transform_coord_map_to_image_lower_right(self):
        coord = (-1850865+(30*255), 2956785+((-30)*255))
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (255,255))

    def test_transform_coord_map_to_image_offset(self):
        coord  = (-1850865+2, 2956785-2)
        point = geom.transform_coord(
                coord, self.xform_matrix, src="map", dst="image")
        self.assertEqual(point, (0,0))

    def test_rod(self):
        (x, y) = (-1850865, 2956785)
        rod = [(t.acquired, t[x,y]) for t in self.tiles]
        self.assertEqual(
            [('2014-08-07T00:00:00Z', 0.035099999113299418),
             ('2014-08-23T00:00:00Z', 0.027199999312870204)],
            rod)


class PrivateFunctionsTestCase(BaseTestCase):

    def test_upper_left_proj_point_to_tile_point(self):
        (px, py) = (-1850865, 2956785)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0,0))

    def test_upper_right_proj_point_to_tile_point(self):
        (px, py) = (-1850865+(30*255), 2956785)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (255,0))

    def test_lower_left_proj_point_to_tile_point(self):
        (px, py) = (-1850865, 2956785 + ((-30)*(256-1)))
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0,255))

    def test_lower_right_proj_point_to_tile_point(self):
        (px, py) = (-1850865+(30*255), 2956785+((-30)*255))
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (255,255))

    def test_proj_point_offset_from_pixel_grid(self):
        (px, py)  = (-1850865+2, 2956785-2)
        point = geom._proj_point_to_tile_point(px, py, self.xform_matrix)
        self.assertEqual(point, (0,0))


if __name__ == '__main__':
    unittest.main()
