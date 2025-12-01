import argparse

from defs import walkstac as ws

# TODO
# Look at making a connection between the variables and wikidata  (ProtoOKN connection)
# s2 grid cells (also protoOKN connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read the config file.')
    parser.add_argument('--configfile', type=str, help='The config file')
    parser.add_argument('--branch', type=str, default='master', help='github branch')
    parser.add_argument('--sitemap_only', action='store_true', help='just generate sitemap')
    parser.add_argument('--validate', action='store_true', help='validate STAC catalog and generate error report')
    args = parser.parse_args()
    configfile = args.configfile

    if args.validate:
        ws.validate_stac_catalog(args)
    else:
        ws.walk_stac(args)

