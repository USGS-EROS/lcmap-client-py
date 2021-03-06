import logging


from lcmap.client import tile
from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

context = routes.data_context + "/tiles"


class Data(base.APIComponent):

    def tiles(self, band, x, y, t1, t2, mask=True, shape=True, unscale=True):
        "Get spec and tiles for given band, x, y, and times"
        log_msg = "getting tiles ubid: {0}, point: ({1},{2}), time: {3}/{4}"
        log.debug(log_msg.format(band, x, y, t1, t2))
        point = "{0},{1}".format(x, y)
        time = "{0}/{1}".format(t1, t2)
        resp = self.http.get(
                context,
                params={"band": band, "point": point, "time": time})
        if resp.result:
            spec = resp.result.get("spec")
            tiles = resp.result.get("tiles")
        else:
            spec = {}
            tiles = []
        return (spec, [tile.Tile(t, spec, mask, shape, unscale) for t in tiles])

    def rod(self, band, x, y, t1, t2, mask=True, shape=True, unscale=True):
        "Get spec and rod for given band, point, x, y and times"
        (spec, tiles) = self.tiles(band, x, y, t1, t2, mask, shape, unscale)
        ubid = spec['ubid']
        time_and_value = [
                {'value': t[x, y],
                 'acquired': t.acquired,
                 'source': t.source, 'ubid':ubid} for t in tiles]
        return (spec, time_and_value)

    def save(self, tile):
        resp = self.http.post(context, json = tile)
        return resp

    def specs(self, band):
        ""
        path = routes.data_context + "/specs"
        params = {"band": band}
        response = self.http.get(path, params=params)
        return response.result

    def scenes(self, scene_id):
        ""
        path = routes.data_context + "/scenes"
        params = {"scene": scene_id}
        response = self.http.get(path, params=params)
        return response.result
