# Connections

## References

* [eco4cast / neon4cast](https://github.com/eco4cast/neon4cast)
* [eco4cast / neon4cast-catalog](https://github.com/eco4cast/neon4cast-catalog)

## About

In converting the STAC catalog to an RDF (JSON-LD) based representation we really have
only changed from one catalog to another. So the question can be asked; what is the value
of doing this?

The STAC approach is more focused on the spatial workflow.  Discovery and other related 
facaets are best represented by interface like those at
[Ecological Forecasting Initiative STAC API](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json?.language=en) or it's top level 
with the top level entry point at [STAC Browser](https://radiantearth.github.io/stac-browser/#/).

However, it shuld be noted that these resource are not something that can be located 
at [Google DataSet Search](https://datasetsearch.research.google.com/search?src=0&query=NEON%20Ecological%20Forecasting%20Challenge&docid=L2cvMTF2NGh6ZzBkag%3D%3D) or
[data.gov](https://catalog.data.gov/dataset?q=NEON+Ecological+Forecasting+Challenge).

Given, that, one could see converting STAC to JSON-LD + schema.org as a means to get 
representation in some of these more generalist indexes and leverage the structured
data on the web approach.  

There are [STAC Extensions](https://stac-extensions.github.io/ ) but these don't look
like they allow, currently, for more general resource linking like in DCAT or 
[schema.org/Dataset](https://schema.org/Dataset).  

### Classic data on web best practices 

* link the datasets
* link to things like huggingace
* link publications (dois if there)
* link people (orcids if there)
* principles
* etc

* look to link to the broader open science graph community


### Proto-OKN

ref: [Proto-OKN](https://www.proto-okn.net/)

One of the strength the RDF based approach would have over the STAC + extension approach
is in the area of linking to other resources in a linked open data manner.  Though it
is interesting to consider a STAC extension that addresses some of these discovery 
aspects.  

One example of this we can explore due to the spatial nature of STAC is connecting 
with [KnowWhereGraph](https://knowwheregraph.org/) (KWG).  KWG is big and it is 
out of scope to introdcue it here.  You can check [https://knowwheregraph.org/graph/](https://knowwheregraph.org/graph/) for information about what is in KWG.

One interesting factor though is the use of [S2 grids](http://s2geometry.io/)  which are
a type of [OGC Discrete Grid](https://docs.ogc.org/as/20-040r3/20-040r3.html) approach.

> Note: Also, there is the leveraging of WikiData connections which should be explored

> Question:  Are UNESCO SDGs worthly links?

To do this I took the bounding box values in the STAC files and converted them to 
level 13 S2 Cell ids.  These level 13 cells are about 1 km on a side and used by
KWG in their graph.  Example links from cells related to NEON resources would look like: 

```
https://stko-kwg.geog.ucsb.edu/browse/#kwgr:s2.level11.9291041754864156672
```

These would link out to resources expressed in the KWG graph.  Often these are
either historical weather events or socio-economic references.  However, this is 
growing and could be anything.  

> NOTE:  These same S2 cells can be used to query [Google Data Commons](https://datacommons.org/) as well.  

An example link to smoke plume data follows:

```
https://stko-kwg.geog.ucsb.edu/browse/#kwgr:smokeplumesnapshot.3135.2018-08-02.7
```

Further, this sorts of relations can be done via the SPARQL query endpoints on the 
triplestores. Example SPARQL queries follow and can also be seen in action in the 
associated notebook in this repo.  

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://schema.org/>

SELECT ?s2l13 ?kwgs ?strings2l13 ?curl
WHERE {
  <https://example.org/id/de648e20a4> schema:spatialCoverage  ?sp .
  <https://example.org/id/de648e20a4> schema:distribution ?dist .
  ?dist schema:contentUrl ?curl .
  ?sp schema:geo ?geo .
  ?geo schema:name "s2Level13" .
  ?geo schema:value ?s2l13 .  
    BIND (STR(?s2l13) AS ?strings2l13)

}    
```

|   | Value                                    |
|---|------------------------------------------|
| 1 | "9291047252422295552"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 2 | "9291052200224620544"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 3 | "9291044503643226112"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 4 | "9291047802178109440"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 5 | "9291045878032760832"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 6 | "9291051650468806656"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 7 | "9291043953887412224"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 8 | "9291041754864156672"^^<http://www.w3.org/2001/XMLSchema#integer> |



```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://schema.org/>

SELECT ?kwgs WHERE {

  SERVICE <https://stko-kwg.geog.ucsb.edu/workbench/repositories/KWG> {
            select ?kwgs where {
	        ?kwgs ?kwgp "9291047252422295552" .
        }  
	}
  
}  
```

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://schema.org/>

SELECT ?s2l13 ?kwgs WHERE {
  <https://example.org/id/de648e20a4> schema:spatialCoverage  ?sp .
  ?sp schema:geo ?geo .
  ?geo schema:name "s2Level13" .
  ?geo schema:value ?s2l13 .
  
  BIND (STR(?s2l13) AS ?strings2l13)
  
  SERVICE <https://stko-kwg.geog.ucsb.edu/workbench/repositories/KWG> {
            select ?kwgs where {
	        ?kwgs ?kwgp ?strings2l13 .
        }  
	}
  
}    
```

### Huggingface and Croissant

Hugging Face is leveraging the [ML Commons](https://mlcommons.org/) 
[Croissant Working Group](https://mlcommons.org/working-groups/data/croissant/) 
work on standardizing datasets metadata for ML workflows.  

This format is able to describe tabular data like CSV and Parquet.  As such, 
it would be interesting to explore a crosswalk to the Croissant format to ensure
the table data, like exposed via the STAC extensions, can be mapped in.

Hugging Face is generating the Croissant files and has documentation 
on [how to access these files](https://huggingface.co/docs/datasets-server/en/croissant).

For cases where a group is coming in with explicate and vetted information I 
do not currently know how that is best handled. 

* https://huggingface.co/datasets/eco4cast/neon4cast-scores
* https://datasets-server.huggingface.co/croissant?dataset=eco4cast/neon4cast-scores&full=true



### Service links and CODATA CDIF

> Need to also link in the software here as well and think about how that relates to CDIF
> OIH patterns and also to FDOs

Also, the [CODATA CDIF](https://codata.org/cross-domain-interoperability-framework-cdif-discovery-module-v01-draft-for-public-consultation/) work may be of interest.   I added the section:

```json
    "offers": {
        "@type": "Offer",
        "itemOffered": {
            "@type": "Service",
            "description": "A STAC Catalog Service",
            "potentialAction": {
                "@type": "Action",
                "target": "https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json"
            }
        }
    },
```

to the JSON-LD files.  

This is more placeholder than finished product.  It attempts to lay
the groundwork to enable the dataset to act as a discovery vector for the service.
Do so begin to lay the foundation for something like the service layer of the FAIR 
Digital Objects concept.  It raises the question of if resources like these can
be considered a FDOs.  

### FAIR Digital Objects

> either make the current web site enabled with signposting and or make a new repo that can be placed in zemodo that 
> is also signposted or a FDO object in some manner.  Would be nice if this was a model that worked for both neon
> and also the hydrography group as well. 

It is also interesting to explore how this approach, JSON-LD, compares
to the STAC approach in the context of FAIR data principles and other factors.

This is, it seems, a simialar issue to the notebooks and research / scholarly objects discusion.  


#### STAC vs. FAIR Digital Objects

| Feature                 | STAC                               | FAIR Digital Objects (FDO) |
|-------------------------|------------------------------------|----------------------------|
| **Purpose**              | Standardizes metadata for Earth observation assets | Enhances discoverability, accessibility, interoperability, and reusability of digital objects |
| **Focus**                | Earth observation data (imagery, radar, LiDAR, etc.) | Broad range of digital objects (scientific data, code, workflows, etc.) |
| **Schema**               | JSON-based schema                  | Flexible schema (can be domain-specific) |
| **Properties**           | Extensive properties for Earth observation data | Core properties focus on identification, access, reuse |
| **Extensions**           | Supports extensions for specific domains | Can be extended through profiles |
| **Community**            | Earth science community            | Broad scientific community   |


