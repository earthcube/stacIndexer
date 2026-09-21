

# A box is the area enclosed by the rectangle
# formed by two points. The first point is the lower
# corner, the second point is the upper corner.
# A box is expressed as two points separated
# by a space character.

# {
#     "@type": ["PropertyValue", "https://stko-kwg.geog.ucsb.edu/lod/ontology#S2Cell"],
#     "additionalType": {
#         "@id": "https://stko-kwg.geog.ucsb.edu/lod/ontology#S2Cell"
#     },
#     "name": "s2Level13",
#     "description": "S2 cell at level 13",
#     "value": "{{CellID13}}"
# }


def sdo_box(bbox, geometry, cells, name=None):
    doc = []
    place_coords = {}
    additional_property = []
    geo = []

    geoshape = {"@type": "GeoShape", "box": bbox}
    geo.append(geoshape)

    coordinates = geometry.get("coordinates")
    for c in coordinates:
        geometry_item = {}
        geometry_item["@type"] = "GeoCoordinates"
        geometry_item["latitude"] = c[1]
        geometry_item["longitude"] = c[0]
        geo.append(geometry_item)

    for c in cells:
        geos2 = {}
        geos2["@type"] = ["PropertyValue", "https://stko-kwg.geog.ucsb.edu/lod/ontology#S2Cell"]
        geos2["additionalType"] = {"@id": "https://stko-kwg.geog.ucsb.edu/lod/ontology#S2Cell"}
        geos2["name"] = "s2Level13"
        geos2["description"] = "S2 cell at level 13"
        geos2["value"] = c
        additional_property.append(geos2)

    place_coords['@type'] = 'Place'
    if name and ','  in name: # if it's got commas
        doc.append(build_place_list(name=name))
    else:
        place_coords['name'] = name
    place_coords['geo'] = geo
    place_coords['additionalProperty'] = additional_property
    doc.append(place_coords)

    return doc

# build place list
# model sites are a comma separated list of place names. This function takes the name string and splits it into a list of place names, then creates a list of Place objects for each name. If the name string does not contain any commas, it returns None.
def build_place_list(name=None):
    place_list = []
    if ','  in name:
        place_names = name.split(',')
        for place_name in place_names:
            place = {}
            place['@type'] = 'Place'
            place['name'] = place_name.strip()
            place_list.append(place)
    return place_list or None
