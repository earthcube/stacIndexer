

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

    doc['@type'] = 'Place'
    doc['geo'] = geo
    doc['additionalProperty'] = additional_property

    return doc