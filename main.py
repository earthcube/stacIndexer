import argparse

from defs import walkstac as ws

# TODO
# Look at making a connection between the variables and wikidata  (ProtoOKN connection)
# s2 grid cells (also protoOKN connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read the config file.')
    parser.add_argument('--configfile', type=str, help='The config file')

    args = parser.parse_args()
    configfile = args.configfile
    ws.walk_stac(configfile)
