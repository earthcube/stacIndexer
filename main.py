import argparse

from defs import walkstac as ws

# TODO
# Look at making a connection between the variables and wikidata  (ProtoOKN connection)
# s2 grid cells (also protoOKN connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read the config file.')
    parser.add_argument('--configfile', type=str, help='The config file')
    parser.add_argument('--branch', type=str, default='master', help='github branch')
    parser.add_argument('--sitemap', action='store_false', help='just generate sitemap')
    args = parser.parse_args()
    configfile = args.configfile
    if not args.sitemap:
        ws.generate_sitemap("data/output", "data/output/sitemap", "test")
        exit(0)
    ws.walk_stac(args)

