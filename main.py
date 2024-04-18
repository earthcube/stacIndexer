import json
from pyld import jsonld
import random
import string
from icecream import ic
import pandas as pd
import hashlib
import argparse

from defs import walkstac as ws

from s2cells import bb2s2
from spatial import sdo_box
from service import service_instance, offer
from citation import citation

from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension

# TODO
# Look at making a connection between the variables and wikidata  (ProtoOKN connection)
# s2 grid cells (also protoOKN connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read the config file.')
    parser.add_argument('--configfile', type=str, help='The config file')

    args = parser.parse_args()
    configfile = args.configfile
    ws.walk_stac(configfile)
