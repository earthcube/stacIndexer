import logging
import os
import shutil

import pystac
import requests
from pystac import Catalog, STACObjectType
from icecream import ic
import hashlib

from archive.s2cells import bb2s2
from archive.spatial import sdo_box
from pystac_client import Client

# from convertas import convert_array_to_string
from defs import convertas
from defs import datacitation


def save_dict_to_file(repo, root, collection, item):
    # At this point I have three elements:  root_catalog, item and asset (from below)
    props = item.properties
    assets = item.assets

    ic(root.id)
    ic(root.title)
    ic(root.description)

    ic(collection.to_dict())
    ic(collection.description)

    ic(item.geometry)
    ic(item.bbox)
    ic(item.datetime)
    ic(item.collection_id)
    ic(item.get_collection())
    ic(item.common_metadata.instruments)
    ic(item.common_metadata.platform)
    ic(item.common_metadata.gsd)
    ic(item.stac_extensions)

    #ic(asset)

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
    idhash_obj.update(str(item.id + item.collection_id).encode())
    idhash_string = idhash_obj.hexdigest()
    idshort_hash = idhash_string[:10]

    doc["@context"] = context
    doc["@type"] = "Dataset"
    doc["@id"] = "urn:" + repo.id + ":{}".format(idshort_hash)
    doc["name"] = str(props.get("title"))
    doc["description"] = str(props.get("description"))
    doc["datePublished"] = props.get("datetime")[:10]
    doc["datetime"] = props.get("datetime")[:10]
    doc["updated"] = props.get("updated")
    doc["start_datetime"] = props.get("start_datetime")
    doc["end_datetime"] = props.get("end_datetime")
    doc["keywords"] = props.get("keywords", [])

    # TODO WARNING
    # this is hard coded here, need to pass down from the main, but I would like to make
    # the whole process https based, so just bring this value here to test in the JSON-LD
    # root_catalog_url = "https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json"
    # doc["offers"] = offer(root_catalog_url)   ## comment back in when the catalog URL properly passed up from main

    doc["citation"] = datacitation.citation()

    dists = []
    for asset_key in assets:
        asset = assets[asset_key].to_dict()
        dist = {"@type": "DataDownload"}
        dist["contentUrl"] = asset.get("href")
        dist["encodingFormat"] = asset["type"]
        dist["description"] = asset["description"]
        dist["name"] = asset["title"]

        varmes = []
        if asset.get("type") == "application/x-parquet":
            # if asset["type"] == "image/png":
            ext = item.stac_extensions
            if 'https://stac-extensions.github.io/table/v1.2.0/schema.json' in ext:
                try:
                    cols = item.ext.table.columns
                except AttributeError:
                    print("'Item' object has no attribute 'ext'. Continuing...")
                else:
                    if len(cols) > 0:
                        for col in cols:
                            col_dc = col.to_dict()
                            prop = {}
                            prop["@type"] = "PropertyValue"
                            prop["name"] = col_dc["name"]
                            prop["description"] = col_dc["description"]
                            varmes.append(prop)
                    doc["variableMeasured"] = varmes

        dists.append(dist)

    # TODO WARNING static element, comment out for now
    # doc["isPartOf"] = "https://datasets-server.huggingface.co/croissant?dataset=eco4cast/neon4cast-scores&full=true"
    doc["distribution"] = dists
    doc["spatialCoverage"] = sdo_box(convertas.convert_array_to_string(item.bbox), item.geometry, cells)

    # Rest of code remains unchanged...

    # if asset["type"] == "application/x-parquet":
        # read_parquet(asset["href"])

    # compacted = jsonld.compact(doc, context)
    # dataset_string = json.dumps(compacted, indent=4)

    dataset_string = json.dumps(doc, indent=4)

    hash_obj = hashlib.sha256()
    hash_obj.update(dataset_string.encode())
    hash_string = hash_obj.hexdigest()
    short_hash = hash_string[:10]

    create_folder_if_not_exist("./data/output/" + repo.id)
    filename = "./data/output/" + repo.id + "/{}.json".format(short_hash)
    with open(filename, 'w') as f:
        f.write(dataset_string)
    # print(f"Dictionary saved to file: {filename}")

def walk_item(repo, root_catalog, collection, itemid):
    try:
        item = root_catalog.get_item(itemid, recursive=True)
    except Exception as e:
        # print(f"An error occurred: {e}")  # Prints the error message

        return  # Leaves the function early

    save_dict_to_file(repo, root_catalog, collection, item)

def walk_collection(repo, root_catalog, collection):
    # collectionid = root_catalog.get_child(collection.id,recursive=True)
    # if collectionid is None:
    #     print("Collection is Empty. Check your downloads and try again.")
    #     return
    # else:
    #     print("Collection has a root child. You may proceed to the following steps.")
    #
    # items = list(collectionid.get_all_items())
    items = list(collection.get_all_items())
    for item in items:
        # print(f"- {item.id}")
        walk_item(repo, root_catalog, collection, item.id)

def safe_convert_to_int(value):
    """ Attempts to convert a value to an integer, handling errors gracefully. """
    try:
        return int(value)
    except ValueError:
        logging.error(f"Invalid data for conversion to int: {value}")
        return None  # or return a default value, or raise a custom error

import json

def validate_collection(file_path):
    collection = pystac.Collection.from_file(file_path)

    # Validate the collection
    try:
        collection.validate()
        print(f"      The collection is valid according to the STAC specifications.")
    except Exception as e:
        print(f"      Validation error:", e)
    # stac = stac_validator_module.StacValidate(file_path, extensions=True)
    # stac.run()
    # print(stac.message)
    # [
    #     {
    #         "version": "1.0.0-beta.1",
    #         "path": file_path,
    #         "schema": [
    #             "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
    #             "https://stac-extensions.github.io/item-assets/v1.0.0/schema.json",
    #             "https://stac-extensions.github.io/table/v1.2.0/schema.json"
    #         ],
    #         "valid_stac": True,
    #         "asset_type": "COLLECTION",
    #         "validation_method": "extensions"
    #     }
    # ]

def validate_catalog(file_path):
    catalog = pystac.Catalog.from_file(file_path)

    # Validate the collection
    try:
        catalog.validate()
        return "VALID catalog"
    except Exception as e:
        logging.error("Validation error:", e)
        return "INVALID catalog"

def process_catalog(catalog, base):
    try:
        # Check if the catalog has a method or attribute to get its href (URL or path)
        catalog_url = catalog.get_self_href()  # This is just an example; adjust based on actual methods available

        # Now open a client with the correct URL or path
        client = Client.open(catalog_url)

        # Process items
        for item in client.get_child_links():
            if item.rel=="child":
                print(f"    Processing item: {base}/{item.target}")
                filepath = f"{base}/{item.target}"
                validate_collection(filepath)
    except Exception as e:
        print(f"    An error occurred: {e}")


def walk_catalog(root_catalog):
    child_items = list(root_catalog.get_children())
    for child in child_items:
        if child.STAC_OBJECT_TYPE == STACObjectType.ITEM: # aka Feature
            logging.info(f" do something with FEATURE(aka STACObjectType.ITEM): {child}")
        elif child.STAC_OBJECT_TYPE == STACObjectType.CATALOG:
            l2_child_catalogs = list(child.get_children())
            for l2 in l2_child_catalogs:
                walk_catalog(child)
        elif child.STAC_OBJECT_TYPE == STACObjectType.COLLECTION:
            try:
                collections = list(child.get_all_collections())
                print(f"Number of collections: {len(collections)}")
                print("Collections IDs:")
                for collection in collections:
                    print(f"- {collection.id}")
                    walk_collection(root_catalog, child, collection)
            except Exception as e:
                print(f"    An error occurred: {e}")
        else:
            logging.error(f"uknonwn type")




def generate_sitemap(folder_path, sitemap_path, repo):
    if not os.path.exists("." + folder_path):
        return
    # Specify the directory you want to list
    base_url = 'https://raw.githubusercontent.com/earthcube/stacIndexer/master' + folder_path + '/'
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # List all files and directories in the folder
    items = os.listdir("." + folder_path)

    # Print the items
    for item in items:
        xml_content += '    <url><loc>'+base_url + item + '</loc></url>\n'

    xml_content += '</urlset>'
    # Path to the file
    file_path = '.' + sitemap_path + '/sitemap_' + repo + '.xml'
    create_folder_if_not_exist('.' + sitemap_path)

    # Write to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(xml_content)

def clear_output_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove all the contents of the folder
        shutil.rmtree(folder_path)
    # Create the folder (it will also recreate if it was deleted)
    os.makedirs(folder_path)

def create_folder_if_not_exist(folder_path):
    os.makedirs(folder_path, exist_ok=True)

def adjust_bbox(bbox):
    # Check if the bbox has an extra pair of square brackets
    while isinstance(bbox, list) and len(bbox) == 1 and isinstance(bbox[0], list):
        # Flatten the list by removing the outer list
        return bbox[0]
    return bbox


def process_file(file_path, old_string, new_string):
    try:
        # Read the contents of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace the target string
        new_content = content.replace(old_string, new_string)

        # Ensure the content is valid JSON after replacement
        try:
            json_content = json.loads(new_content)
        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON file after replacement: {file_path} ({e})")
            return

        # Check if 'bbox' is in the JSON and adjust if necessary
        if "bbox" in json_content:
            json_content["bbox"] = adjust_bbox(json_content["bbox"])

        # Write the modified JSON back to the file
        with open(file_path, 'w') as file:
            json.dump(json_content, file, indent=4)

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")


def replace_in_folder(folder_path, old_string, new_string):
    # Walk through all files in the directory
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            # Check if the file is a JSON file
            if file_name.endswith('.json'):
                # Construct full file path
                file_path = os.path.join(root, file_name)

                # Process the file
                process_file(file_path, old_string, new_string)

def download_file_from_github(file_url, local_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded: {local_path}")
    else:
        print(f"Failed to download file: {response.status_code}")

def download_folder_from_github(repo, folder_path, local_folder_path):
    clear_output_folder(local_folder_path)

    api_url = f"https://api.github.com/repos/{repo}/contents/{folder_path}"

    github_token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                file_url = item['download_url']
                local_file_path = os.path.join(local_folder_path, item['name'])
                download_file_from_github(file_url, local_file_path)
            elif item['type'] == 'dir':
                new_local_folder_path = os.path.join(local_folder_path, item['name'])
                os.makedirs(new_local_folder_path, exist_ok=True)
                download_folder_from_github(repo, item['path'], new_local_folder_path)
    else:
        print(f"Failed to retrieve folder contents: {response.status_code}")
        return

def walk_stac(cf):

    # Use a breakpoint in the code line below to debug your script.
    clear_output_folder("./data/output/")

    download_folder_from_github("eco4cast/neon4cast-ci", "catalog", "./data/challenge/neon4cast-stac")
    download_folder_from_github("LTREB-reservoirs/vera4cast", "catalog", "./data/challenge/vera4cast-stac")
    download_folder_from_github("eco4cast/usgsrc4cast-ci", "catalog", "./data/challenge/usgsrc4cast-stac")

    # Resolve schema issues
    replace_in_folder('./data/challenge', '"href": []', '"href": "https://github.com/radiantearth"')
    replace_in_folder('./data/challenge', '"href": null', '"href": "https://github.com/radiantearth"')
    replace_in_folder('./data/challenge', '"href": {}', '"href": "https://github.com/radiantearth"')
    replace_in_folder('./data/challenge', 'InfT00:00:00Z', '2023-10-01T00:00:00Z')
    replace_in_folder('./data/challenge', '-InfT00:00:00Z', '2024-09-05T00:00:00Z')
    replace_in_folder('./data/challenge', '-2023-10-01T00:00:00Z', '2023-10-01T00:00:00Z')


    root_catalog = Catalog.from_file(href=cf)
    ic(root_catalog)

    #child_catalogs = list(root_catalog.get_children())
    walk_catalog(root_catalog)
    # Debugging for challenge only
    # print(f"Number of child catalogs: {len(child_catalogs)}")
    # for child in child_catalogs:
    #     print(f"  - {child.id}")
    #     child_cf = f"data/challenge/{child.id}/catalog.json"
    #     print(f"    - {child_cf} [{validate_catalog(child_cf)}]")
    #
    #     child_catalog = Catalog.from_file(href=child_cf)
    #     process_catalog(child_catalog, f"data/challenge/{child.id}")
    #
    # original block
    # for child in child_catalogs:
    #     if child.STAC_OBJECT_TYPE == STACObjectType.ITEM: # aka Feature
    #         logging.info(f" do something with FEATURE(aka STACObjectType.ITEM): {child}")
    #     elif child.STAC_OBJECT_TYPE == STACObjectType.CATALOG:
    #         l2_child_catalogs = list(child.get_children())
    #         for l2 in l2_child_catalogs:
    #             process_catalog(l2, l2.get_self_href())
    #     elif child.STAC_OBJECT_TYPE == STACObjectType.COLLECTION:
    #        # collections = list(child.get_all_collections())
    #         collections = list(child.get_collections())
    #         print(f"Number of collections: {len(collections)}")
    #         print("Collections IDs:")
    #         for collection in collections:
    #             print(f"- {collection.id}")
    #             walk_collection(child, collection)
    #     else:
    #         logging.error(f"uknonwn type")
    generate_sitemap("/data/output/neon4cast-stac", "/data/output/sitemap", "neon4cast")
    generate_sitemap("/data/output/vera4cast-stac", "/data/output/sitemap", "vera4cast")
    generate_sitemap("/data/output/usgsrc4cast-stac", "/data/output/sitemap", "usgsrc4cast")
