from s2sphere import Cell, CellId, LatLngRect, LatLng, RegionCoverer
from icecream import ic


def bboxsplit(a):
    return None

# Note, level is not a min max, just a single level
def bb2s2(min_lat, max_lat, min_lng, max_lng, level):
    p1 = LatLng.from_degrees(33, -122)
    p2 = LatLng.from_degrees(33.1, -122.1)
    rect = LatLngRect.from_point_pair(p1, p2)

    r = RegionCoverer()
    r.max_level = level
    r.max_level = level

    cellids = r.get_covering(rect)
    cl =  []
    for c in cellids:
        cl.append(c.id())

    return cl