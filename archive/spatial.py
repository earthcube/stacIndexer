

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


def sdo_box(bbox, geometry, cells):
    doc = {}
    additional_property = []

    geoshape = {"@type": "GeoShape", "box": bbox}
    geometry = {"@type": "MultiPoint", "points": geometry.get("coordinates")}

    geo = [geoshape, geometry]

    for c in cells:
        geos2 = {}
        geos2["@type"] = ["PropertyValue", "https://stko-kwg.geog.ucsb.edu/lod/ontology#S2Cell"]
        geos2["additionalType"] = {"@id": "https://stko-kwg.geog.ucsb.edu/lod/ontology#S2Cell"}
        geos2["name"] = "s2Level13"
        geos2["description"] = "S2 cell at level 13"
        geos2["value"] = c
        additional_property.append(geos2)

    doc['@type'] = 'Place'
    doc['geo'] = geo
    doc['additionalProperty'] = additional_property

    return doc