import logging
import os
import shutil
from urllib.parse import urlparse

import pystac
import requests
from pystac import Catalog, STACObjectType, Item, Collection
from icecream import ic
import hashlib

from archive.s2cells import bb2s2
from archive.spatial import sdo_box
from pystac_client import Client

# from convertas import convert_array_to_string
from defs import convertas
from defs import datacitation
from pathlib import Path
from sys import gettrace
import re

def find_asset_by_title(assets, title):
    for asset_key, asset in assets.items():
        if asset.title == title:
            return asset
    return None


def save_dict_to_file(repo, root, collection, item, breadcrumb, repoPath="missing"):
    # At this point I have three elements:  root_catalog, item and asset (from below)
    props = item.properties
    assets = item.assets
    if gettrace() or os.getenv("DEBUG", 'FALSE').upper() == "TRUE":
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

    max_lng, max_lat, min_lng, min_lat = item.bbox
    level = 13

    cells = bb2s2(min_lat, max_lat, min_lng, max_lng, level)
    # if asset "Model Sites" is present, then use its description to define the name for teh @Place for the spatial coverage

    doc = {}
    context = {"@vocab": "https://schema.org/"}

    idhash_obj = hashlib.sha256()

    idhash_obj.update(breadcrumb.encode())
    idhash_string = idhash_obj.hexdigest()
    idshort_hash = idhash_string[:10]

    doc["@context"] = context
    doc["@type"] = "Dataset"
    doc["@id"] = "urn:" + repoPath + ":{}".format(idshort_hash)
    doc['identifier']=breadcrumb
    doc["name"] = str(props.get("title"))
    doc["description"] = str(props.get("description"))
    doc["datePublished"] = props.get("datetime")[:10]
    doc["datetime"] = props.get("datetime")[:10]
    doc["updated"] = props.get("updated")
    doc["start_datetime"] = props.get("start_datetime")
    doc["end_datetime"] = props.get("end_datetime")
    doc["keywords"] = props.get("keywords", [])
    doc["providers"] = props.get("providers", [])



    # TODO WARNING
    # this is hard coded here, need to pass down from the main, but I would like to make
    # the whole process https based, so just bring this value here to test in the JSON-LD
    # root_catalog_url = "https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json"
    # doc["offers"] = offer(root_catalog_url)   ## comment back in when the catalog URL properly passed up from main

    doc["citation"] = datacitation.citation(doc["providers"] )

    dists = []

    baseStacUI = "https://radiantearth.github.io/stac-browser/#/external"
    fileurl = item.get_self_href()
    if fileurl.startswith("http"):
        filepath = fileurl.split("/",maxsplit=1)[1]
        doc["url"] = f'{baseStacUI}{filepath}'

        stacDist = {"@type": "DataDownload"}
        stacDist["contentUrl"] =  item.get_self_href()
        stacDist["encodingFormat"] = 'application/json'
        stacDist["description"] = "Stac Item JSON"
        stacDist["name"] = "Stac Item JSON"
        dists.append(stacDist)
        stacHtml = {"@type": "DataDownload"}
        stacHtml["contentUrl"] =  f'{baseStacUI}{filepath}'
        stacHtml["encodingFormat"] = 'text/html'
        stacHtml["description"] = "Stac Item in Radiantearth STAC Browser"
        stacHtml["name"] = "Stac Item in Radiantearth STAC Browser"
        dists.append(stacHtml)
    for asset_key in assets:
        try:
            asset = assets[asset_key].to_dict()
            asset_obj = assets[asset_key]
            dist = {"@type": "DataDownload"}
            href = asset_obj.get_absolute_href() or asset_obj.get_href()
            dist["contentUrl"] = href
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
        except Exception as e:
            logging.error(f"Error processing asset {asset_key} for item {item.id}: {e}")
            continue

    # TODO WARNING static element, comment out for now
    # doc["isPartOf"] = "https://datasets-server.huggingface.co/croissant?dataset=eco4cast/neon4cast-scores&full=true"
    doc["distribution"] = dists

    # if asset "Model Sites" is present, then use its description to define the name for teh @Place for the spatial coverage
    ms =  find_asset_by_title(assets, "Model Sites")
    placename= ms.description if ms and ms.description else None
    doc["spatialCoverage"] = sdo_box(convertas.convert_array_to_string(item.bbox), item.geometry, cells, name=placename)

    # Rest of code remains unchanged...

    # if asset["type"] == "application/x-parquet":
    # read_parquet(asset["href"])

    # compacted = jsonld.compact(doc, context)
    # dataset_string = json.dumps(compacted, indent=4)

    dataset_string = json.dumps(doc, indent=4)
    #
    # hash_obj = hashlib.sha256()
    # # lets us amore stable @id for the filenames
    # #hash_obj.update(dataset_string.encode())
    # hash_obj.update(doc["@id"].encode())
    # hash_string = hash_obj.hexdigest()
    # short_hash = hash_string[:10]

    create_folder_if_not_exist("./data/output/" + repoPath)
    filename = "./data/output/" + repoPath + "/{}.json".format( idshort_hash)
    if os.path.exists(filename):
        print(f"duplicate hash for : {idshort_hash} {breadcrumb}")
    with open(filename, 'w') as f:
        f.write(dataset_string)
    # print(f"Dictionary saved to file: {filename}")


def walk_item(repo, root_catalog: Catalog, collection: Collection, itemid, breadcrumb, repoPath="missing"):
    try:
        item = root_catalog.get_item(itemid, recursive=True)
    except Exception as e:
        # print(f"An error occurred: {e}")  # Prints the error message

        return  # Leaves the function early
    #breadcrumb = f"{breadcrumb}/{item.id}"
    save_dict_to_file(repo, root_catalog, collection, item, breadcrumb,repoPath)


def walk_collection(repo, root_catalog: Catalog, collection: Collection, breadcrumb, repoPath="/"):
    # collectionid = root_catalog.get_child(collection.id,recursive=True)
    # if collectionid is None:
    #     print("Collection is Empty. Check your downloads and try again.")
    #     return
    # else:
    #     print("Collection has a root child. You may proceed to the following steps.")
    #
    # items = list(collectionid.get_all_items())
    baseStacUI = "https://radiantearth.github.io/stac-browser/#/external"

    try:
        if collection is None:
            print(
                f"    Collection is None... for get_all_items collection:")

            return

        #items = collection.get_all_items()
        items = collection.get_items(recursive=True)
        # removing None still had issues, just using the iterator
        #filtered_data = [item for item in items if item is not None]

        for item in items:
            breadcrumb_item = f"{breadcrumb}/{item.id}"
            # print(f"- {item.id}")
            try:
                walk_item(repo, root_catalog, collection, item.id, breadcrumb_item, repoPath)
            except Exception as e:
                ic(item)
                print(
                    f"    An error occurred in item {item.id} collection: {collection.id}  root: {root_catalog.id} repo: {repo.id}: {e}")
    except  Exception as e:
        ic(collection)
        print(
            f"    An error occurred at get_all_items collection: {collection.id}  root: {root_catalog.id} repo: {repo.id}: {e}")
        if str(e).startswith('HREF:'):
            # This is a specific error related to the href not being found
            # It might be due to an empty collection or a missing href
            print(f"    Collection {collection.id} might be empty or href is missing.")
            match = re.search(r"https?://[^\s']+", str(e))
            if match:
                url = match.group()
                if url.startswith("http"):
                    url = url.split("/", maxsplit=1)[1]
                    print(f" in chrome see if source is valid: {baseStacUI}{url}")



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


def validate_catalog(file_path_or_url):
    # Support both URL and file path
    if file_path_or_url.startswith('http'):
        # Fetch and clean catalog from URL
        catalog_dict = fetch_and_clean_catalog_from_url(file_path_or_url)
        catalog = pystac.Catalog.from_dict(catalog_dict)
    else:
        # Use file-based approach for local files
        catalog = pystac.Catalog.from_file(file_path_or_url)

    # Validate the catalog
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
            if item.rel == "child":
                print(f"    Processing item: {base}/{item.target}")
                filepath = f"{base}/{item.target}"
                validate_collection(filepath)
    except Exception as e:
        print(f"    An error occurred: {e}")

def repoPath(catalog, previousCatalogs):
    rootPath = ""
    if previousCatalogs is not None:
        for p in previousCatalogs:
            rootPath = f"{p.id}"
    rootPath = f"{rootPath}/{catalog.id}"
    return rootPath

def walk_catalog(root_catalog: Catalog, breadcrumb, previousCatalogs=None):

    child_items = root_catalog.get_children()

    for child in child_items:
        if previousCatalogs is None:
            previousCatalogs = []
        breadcrumb_new = f"{breadcrumb}/{child.id}"

        if child.STAC_OBJECT_TYPE == STACObjectType.ITEM:  # aka Feature
            logging.info(f" do something with FEATURE(aka STACObjectType.ITEM): {child}")
        elif child.STAC_OBJECT_TYPE == STACObjectType.CATALOG:

            previousCatalogs.append(child)
            try:
                l2_child_catalogs = child.get_children()
                for l2 in l2_child_catalogs:
                    breadcrumb_catalog = f"{breadcrumb_new}/{l2.id}"
                    try:
                        walk_catalog(l2, breadcrumb_catalog, previousCatalogs=previousCatalogs)
                    except   pystac.errors.STACError as e:
                        print(f"    An error occurred chlid: {child.id} root {root_catalog.id}: {e}")
                    except Exception as e:
                        print(f"    An error occurred chlid: {child.id} root {root_catalog.id}: {e}")
            except   pystac.errors.STACError as e:
                print(f"    An error occurred chlid: {child.id} root {root_catalog.id}: {e}")
            except  Exception as e:
                print(f"    An error occurred chlid: {child.id} root {root_catalog.id}: {e}")
        elif child.STAC_OBJECT_TYPE == STACObjectType.COLLECTION:
            try:
                collections = child.get_all_collections()
                #print(f"Number of collections: {len(collections)}")
                print("Collections IDs:")
                for collection in collections:
                    breadcrumb_collection = f"{breadcrumb_new}/{collection.id}"
                    print(f"- {collection.id}")
                    try:

                        walk_collection(root_catalog, child, collection, breadcrumb_collection, repoPath(root_catalog, previousCatalogs))
                    except Exception as e:
                        print(
                            f"    An error occurred in child: {child.id} collection {collection.id}: root:{root_catalog.id} {e}")
            except Exception as e:
                print(
                    f"    An error occurred for STACObjectType.COLLECTION child: {child.id}  root:{root_catalog.id}: {e}")
        else:
            logging.error(f"uknonwn type")


def generate_sitemap(folder_path, sitemap_path, repo, branch="master"):
    base_path = Path(".")

    target_directory = base_path.joinpath(folder_path)
    if not os.path.exists(target_directory):
        return
    # Specify the directory you want to list
    base_url = f'https://raw.githubusercontent.com/earthcube/stacIndexer/{branch}/'
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # List all files and directories in the folder
     #items= os.listdir("." + folder_path)

    items = [item for item in target_directory.rglob("*") if item.is_file()]

    # Print the items
    for item in items:

        xml_content += '    <url><loc>' + base_url + str(item) + '</loc></url>\n'

    xml_content += '</urlset>'
    # Path to the file
    sm_path = base_path.joinpath(sitemap_path)
    create_folder_if_not_exist(sm_path)
    file_path = sm_path.joinpath( f"sitemap_{repo}.xml")
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


def clean_catalog_content(content):
    """
    Apply the same cleaning operations that replace_in_folder applies,
    but to a string content instead of files in a folder.
    """
    # Apply the same replacements as used in walk_stac()
    replacements = [
        ('"href": []', '"href": "https://github.com/radiantearth"'),
        ('"href": null', '"href": "https://github.com/radiantearth"'),
        ('"href": {}', '"href": "https://github.com/radiantearth"'),
        ('InfT00:00:00Z', '2023-10-01T00:00:00Z'),
        ('-InfT00:00:00Z', '2024-09-05T00:00:00Z'),
        ('-2023-10-01T00:00:00Z', '2023-10-01T00:00:00Z'),
        ('2017-02-01 15:00:00T00:00:00Z', '2017-02-01T00:00:00Z')
    ]

    cleaned_content = content
    for old_string, new_string in replacements:
        cleaned_content = cleaned_content.replace(old_string, new_string)

    return cleaned_content


def fetch_and_clean_catalog_from_url(url):
    """
    Fetch catalog JSON from a URL, apply content cleaning, and return a dictionary
    suitable for pystac.Catalog.from_dict()
    """
    try:
        # Fetch content from URL
        response = requests.get(url)
        response.raise_for_status()

        # Clean the content using the same logic as replace_in_folder
        cleaned_content = clean_catalog_content(response.text)

        # Parse to JSON dictionary
        catalog_dict = json.loads(cleaned_content)

        # Apply bbox adjustment if needed
        if "bbox" in catalog_dict:
            catalog_dict["bbox"] = adjust_bbox(catalog_dict["bbox"])

        return catalog_dict

    except requests.RequestException as e:
        print(f"Error fetching catalog from URL {url}: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from URL {url}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error processing catalog from URL {url}: {e}")
        raise


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


def local_path_to_stac_browser_url(local_path: str) -> str:
    marker = "raw.githubusercontent.com/"
    idx = local_path.find(marker)
    if idx == -1:
        raise ValueError("raw.githubusercontent.com not found in path")
    raw_path = local_path[idx:]
    return f"https://radiantearth.github.io/stac-browser/#/external/{raw_path}"


def walk_stac(args):
    # Use a breakpoint in the code line below to debug your script.

    cf= args.configfile
    # Use URL-based approach with content cleaning
    if not args.sitemap_only:
        clear_output_folder("./data/output/")
        if cf.startswith('http'):
            # Fetch and clean catalog from URL
            catalog_dict = fetch_and_clean_catalog_from_url(cf)
            root_catalog = Catalog.from_dict(catalog_dict)
            root_catalog.set_self_href(cf)
        else:
            if os.getenv('GITHUB_TOKEN') is None:
                logging.error('GITHUB_TOKEN env is not set')
                return
            # Fallback to file-based approach for local files
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
            replace_in_folder('./data/challenge', '2017-02-01 15:00:00T00:00:00Z', '2017-02-01T00:00:00Z')

            root_catalog = Catalog.from_file(href=cf)
        ic(root_catalog)

        #child_catalogs = list(root_catalog.get_children())
        breadcumb=root_catalog.id

        walk_catalog(root_catalog, breadcumb)
    generate_sitemap("data/output/neon4cast-stac", "data/output/sitemap", "neon4cast", branch=args.branch)
    generate_sitemap("data/output/vera4cast-stac", "data/output/sitemap", "vera4cast", branch=args.branch)
    generate_sitemap("data/output/usgsrc4cast-stac", "data/output/sitemap", "usgsrc4cast", branch=args.branch)


