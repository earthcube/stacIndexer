import json
from icecream import ic

from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension

def walk_stac():
    # Use a breakpoint in the code line below to debug your script.
    root_catalog = Catalog.from_file('/home/fils/src/Projects/DeCODER/stacIndexer/data/neon/catalog.json')
    ic(root_catalog)

    # root_catalog.describe()

    print(f"ID: {root_catalog.id}")
    print(f"Title: {root_catalog.title or 'N/A'}")
    print(f"Description: {root_catalog.description or 'N/A'}")

    collections = list(root_catalog.get_collections())

    print(f"Number of collections: {len(collections)}")
    print("Collections IDs:")
    for collection in collections:
        print(f"- {collection.id}")

    collection = root_catalog.get_child("efi-aquatics")
    if collection is None:
        print("Collection is Empty. Check your downloads and try again.")
    else:
        print("Collection has a root child. You may proceed to the following steps.")

    items = list(collection.get_all_items())

    print(f"Number of items: {len(items)}")
    for item in items:
        print(f"- {item.id}")

    item = root_catalog.get_item("xgboost_temp_oxygen_chla_parallel", recursive=True)
    ic(item.geometry)
    ic(item.bbox)
    ic(item.datetime)
    ic(item.collection_id)
    ic(item.get_collection())

    ic(item.common_metadata.instruments)
    ic(item.common_metadata.platform)
    ic(item.common_metadata.gsd)
    ic(item.stac_extensions)

    print("-----------------")
    for asset_key in item.assets:
        asset = item.assets[asset_key]
        print('{}: {} ({})'.format(asset_key, asset.href, asset.media_type))
    print("-----------------")

    asset = item.assets['analytic']
    ic(asset.to_dict())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    walk_stac()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
