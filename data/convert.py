from pyld import jsonld
import json

def read_file_to_string(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    return content

jld = read_file_to_string('./output/1d9b61cc21.json')

doc = json.loads(jld)

normalized = jsonld.normalize(
    doc, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})

print(normalized)