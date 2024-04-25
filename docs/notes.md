# Notes


## Commands

The following works, but this is not the URL we should be using
```bash
python main.py --configfile ./data/neon/catalog.json
```

This one should be correct, but doesn't work.
```bash
python main.py --configfile ./data/challenge/catalog.json
```

URL test this time
```bash
python main.py --configfile https://raw.githubusercontent.com/eco4cast/challenge-catalogs/main/catalog.json
```

Broken: URL test this time
```bash
python main.py --configfile https://raw.githubusercontent.com/eco4cast/neon4cast-ci/main/catalog/catalog.json
```

Broken: URL test this time
```bash
python main.py --configfile https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json
```


## Errata 

See:  workingExample.json

Need to look at ODI-IN:
* https://github.com/iodepo/odis-in/blob/master/dataGraphs%2Fthematics%2Fservices%2Fgraphs%2Fservice.json
* https://docs.google.com/document/d/1ojBHA1_924lKTVK5LumVhL2UaQ-NWm15paIdx2gjHqU/edit
* https://github.com/iodepo/odis-arch/issues/222#issuecomment-2020733768



* Maybe I should make a DataCatalog at the top level, and link to the
dataset, but that is a bit trickier with respect to indexing and recovery
later.

Take a look at https://book.oceaninfohub.org/thematics/docs/index.html and
https://book.oceaninfohub.org/thematics/variables/index.html for
some ideas and examples.

Look at: https://schema.org/SoftwareSourceCode (CreativeWork)
via exampleOfWork

link to pubs like: https://esajournals.onlinelibrary.wiley.com/doi/full/10.1002/ecs2.4686



* license
* provider vs author etc

* GOAL:  Connect with the open science graphs (pid graphs?)

* make a zenodo release?  Does that make sense to do, I would link to that then
* people with ORCIDS

* STAC is a relsted service to the data (bidirectional)
* the Software is related to the dataset
* the activity can be related to publications
* the activity can be related to SDGs or other gov and NGO policy?
* the activity can be related to communities like ESIP or others?
* the activity can be related to classes or research projects?

Look at the Croissant editor as something we can use to build out
the SDO of an FDO based object.

I mean we have the web, why not just a webarchive file still?
It is a simple archive and if done with certain features and approaches
could be evaluated for FAIR (Fuji for example) or FDO (via shacl) or
something like this more appropriate. 


![relationsEvolved.svg](images%2FrelationsEvolved.svg)