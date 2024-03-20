import json
from pyld import jsonld
import random
import string
from icecream import ic
import pandas as pd
import hashlib

from s2cells import bb2s2
from spatial import sdo_box
from service import service_instance, offer

from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension

# TODO
# Look at making a connection between the variables and wikidata  (ProtoOKN connection)
# s2 grid cells (also protoOKN connection)

def convert_array_to_string(array):
    return ' '.join(str(x) for x in array)

def read_parquet(s3_path):
    df = pd.read_parquet(s3_path)
    column_names = df.columns.tolist()
    ic(column_names)

def save_dict_to_file(root, collection, item, asset):
    # At this point I have three elements:  root_catalog, item and asset (from below)
    #

    # TODO WARNING
    # this is hard coded here, need to pass down from the main, but I would like to make
    # the whole process https based, so just bring this value here to test in the JSON-LD
    root_catalog_url = "https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json"


    # ic(root.id)
    # ic(root.title)
    # ic(root.description)
    #
    # ic(collection.to_dict())
    # ic(collection.description)
    #
    # ic(item.geometry)
    # ic(item.bbox)
    # ic(item.datetime)
    # ic(item.collection_id)
    # ic(item.get_collection())
    # ic(item.common_metadata.instruments)
    # ic(item.common_metadata.platform)
    # ic(item.common_metadata.gsd)
    # ic(item.stac_extensions)
    #
    # ic(asset)

    max_lng, max_lat, min_lng, min_lat = item.bbox
    level = 13

    cells = bb2s2(min_lat, max_lat, min_lng, max_lng, level)
    # ic(cells)

    # print('{} ({})'.format( asset["href"], asset["type"]))

    # NOTE: note really needed since the table extension is used.
    # if asset["type"] == "application/x-parquet":
    #     read_parquet(asset["href"])

    # asset = item.assets['parquet_items']
    # ic(asset.to_dict())

    doc = {}
    context = {"@vocab": "https://schema.org/"}

    idhash_obj = hashlib.sha256()
    idhash_obj.update(asset["href"].encode())
    idhash_string = idhash_obj.hexdigest()
    idshort_hash = idhash_string[:10]


    doc["@context"] = context
    doc["@type"] = "Dataset"
    doc["@id"] = "https://example.org/id/{}".format(idshort_hash)
    doc["name"] = root.id
    doc["description"] = root.description + " " +  collection.description
    doc["offers"] = offer(root_catalog_url)

    dist = {"@type": "DataDownload" }
    dist["contentUrl"] = asset["href"]
    dist["encodingFormat"] = asset["type"]

    # TODO WARNING static element
    dist["isPartOf"] = "https://datasets-server.huggingface.co/croissant?dataset=eco4cast/neon4cast-scores&full=true"

    doc["distribution"] = dist
    doc["spatialCoverage"] = sdo_box(convert_array_to_string(item.bbox), cells)


    varmes = []

    if asset["type"] == "application/x-parquet":
    # if asset["type"] == "image/png":
        ext = item.stac_extensions
        if 'https://stac-extensions.github.io/table/v1.2.0/schema.json' in ext:
            cols = item.ext.table.columns
            if len(cols) > 0:
                for col in cols:
                    col_dc = col.to_dict()
                    prop = {}
                    prop["@type"] = "PropertyValue"
                    prop["name"] = col_dc["name"]
                    prop["description"] = col_dc["description"]
                    varmes.append(prop)
                    # print(col_dc["type"])  # mimetype

            doc["variableMeasured"] = varmes

    # if asset["type"] == "application/x-parquet":
        # read_parquet(asset["href"])

    # compacted = jsonld.compact(doc, context)
    # dataset_string = json.dumps(compacted, indent=4)

    dataset_string = json.dumps(doc, indent=4)

    hash_obj = hashlib.sha256()
    hash_obj.update(dataset_string.encode())
    hash_string = hash_obj.hexdigest()
    short_hash = hash_string[:10]

    filename = "./data/output/{}.json".format(short_hash)
    with open(filename, 'w') as f:
        f.write(dataset_string)
    # print(f"Dictionary saved to file: {filename}")

def walk_item(root_catalog, collection, itemid):
    try:
        item = root_catalog.get_item(itemid, recursive=True)
    except Exception as e:
        # print(f"An error occurred: {e}")  # Prints the error message
        return  # Leaves the function early

    for asset_key in item.assets:
        asset = item.assets[asset_key]
        save_dict_to_file(root_catalog, collection, item, asset.to_dict())

def walk_collection(root_catalog, collection):
    collectionid = root_catalog.get_child(collection.id)
    if collectionid is None:
        print("Collection is Empty. Check your downloads and try again.")
        return
    else:
        print("Collection has a root child. You may proceed to the following steps.")

    items = list(collectionid.get_all_items())
    for item in items:
        # print(f"- {item.id}")
        walk_item(root_catalog, collection, item.id)

def walk_stac():
    # Use a breakpoint in the code line below to debug your script.

    root_catalog_url = "https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json"
    root_catalog = Catalog.from_file('/home/fils/src/Projects/DeCODER/stacIndexer/data/neon/catalog.json')
    ic(root_catalog)

    collections = list(root_catalog.get_collections())

    print(f"Number of collections: {len(collections)}")
    print("Collections IDs:")
    for collection in collections:
        # print(f"- {collection.id}")
        walk_collection(root_catalog, collection)

if __name__ == '__main__':
    walk_stac()
