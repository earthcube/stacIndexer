# Connections

## References

* [eco4cast / neon4cast](https://github.com/eco4cast/neon4cast)
* [eco4cast / neon4cast-catalog](https://github.com/eco4cast/neon4cast-catalog)

## Given that

We can now convert the [neon4cast-catalog STAC catalog.json](https://raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json) to JSON-LD ([example](./workingExample.json))
with an associated [sitemap.xml](../data/sitemap.xml) such that it could be indexed
by DeCODER, Google Dataset Search, or any other consumer using this approach.  

### relations

Some relations between the various documents are seen in the following.

![relations](./images/relations.svg)



### status

At present there are around 150 datasets generated, but this might be low due to some issues
I had with resolving all the assets of the various catalogs.  

An early view of the data follows and shows a typical case where datasets are well described
as atomic units but don't currently express any shared entities in a manner aligned
with graph analytics.  

![graph one](./images/neongraph1.png)

To provide a contrast we can introduce the concept of a globaly shared
concept like a related publication.  In this case, since all resources 
share that common relation, we get something like:

![graph_two](./images/graph.png)

This the other extreme, and now all the resources have a single shared
concept.  In the end, as more concepts are added that are not global, 
more structure will become expressed.  This structure is what might 
allow graph analytics to play some value add role.   Indeed, a global 
shared attribute might be better expressed at a higher order level 
like a collection or catalog. 


## DeCODER and General Structured Data on the Web

In converting the STAC catalog to an RDF (JSON-LD) based representation we really have
only changed from one catalog to another. So the question can be asked; __what is the value
of doing this?__

The STAC approach is more aligned for spatial analytics, so there seems little initial benefit
in the process.  However, exploring some of the features of linked open data may expose some
worthy value add concpets.  

It should be noted these approaches are not exclusionary and actually should be able to work together
to provide richer approach to things such as FAIR principles together. 

My inspection doesn't expose a great deal of web scale discovery for STAC catalogs.  Class web searches
can find them or there are community resources such as the [Radiant Earth STAC browser](https://radiantearth.github.io/stac-browser/#/).

These approaches would lead people to things such as 
[Ecological Forecasting Initiative STAC API](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/eco4cast/neon4cast-catalog/main/stac/catalog.json?.language=en) or it's top level 
with the top level entry point at [STAC Browser](https://radiantearth.github.io/stac-browser/#/).

However, it should be noted that these resource are not something that can be located 
at [Google DataSet Search](https://datasetsearch.research.google.com/search?src=0&query=NEON%20Ecological%20Forecasting%20Challenge&docid=L2cvMTF2NGh6ZzBkag%3D%3D) or
[data.gov](https://catalog.data.gov/dataset?q=NEON+Ecological+Forecasting+Challenge).

Given, that, one could see converting STAC to JSON-LD + schema.org as a means to get 
representation in some of these more generalist indexes and leverage the structured
data on the web approach.  

One of the strength the RDF based approach would have over the STAC + extension approach
is in the area of linking to other resources in a linked open data manner.  Though it
is interesting to consider a STAC extension that addresses some of these discovery 
aspects.

There are [STAC Extensions](https://stac-extensions.github.io/ ) but these don't look
like they allow, currently, for more general resource linking like in DCAT or 
[schema.org/Dataset](https://schema.org/Dataset).  

### Classic data on web best practices 

Some concepts we might think about bringing to the previously linked
([example](./workingExample.json)) file include connections to;

* related datasets or metadata (like those at Hugging Face)
* publications 
* people
* principles like UN SDGs

In general, the goal would be to express connections to the 
broader open science graph community.  

> Question:  Are UNESCO SDGs worthy links?


### Proto-OKN

ref: [Proto-OKN](https://www.proto-okn.net/)

A possible more formal connection target might be the current NSF, and broader, funded
effort for Open Knowledge Networks (OKNs).  

One example of this we can explore due to the spatial nature of STAC is connecting 
with [KnowWhereGraph](https://knowwheregraph.org/) (KWG).  Introducing KWG is out of scope for this document.
You can check [https://knowwheregraph.org/graph/](https://knowwheregraph.org/graph/) for more information about what is in KWG.

As a very basic level we can leverage the use of  [S2 grids](http://s2geometry.io/)  which are
a type of [OGC Discrete Grid](https://docs.ogc.org/as/20-040r3/20-040r3.html) approach and are used by KWG.  

> Note: Also, there is the leveraging of WikiData connections which should be explored

To do this I took the bounding box values in the STAC files and converted them to 
level 13 S2 Cell ids.  These level 13 cells are about 1 km on a side and used by
KWG in their graph.  Example links from cells related to NEON resources would look like: 

* https://stko-kwg.geog.ucsb.edu/browse/#kwgr:s2.level11.9291041754864156672

These would link out to resources expressed in the KWG graph.  Often these are
either historical weather events or socio-economic references.  However, this is 
growing and could be anything.  

> NOTE:  These same S2 cells can be used to query [Google Data Commons](https://datacommons.org/) as well.  

An example link to smoke plume data follows:

* https://stko-kwg.geog.ucsb.edu/browse/#kwgr:smokeplumesnapshot.3135.2018-08-02.7

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


KWG SPARQL call (as a service for later use in federation call)
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

Example SPARQL Federation Call
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

Another approach we can explore so to enable the Datasets to act as discovery proxies for the
STAC catalogs and also the software.  In this approach a discovery in the webspace might be 
able to expose the service in OGC space that is more appropriate for some users.  

> NOTE: the [CODATA CDIF](https://codata.org/cross-domain-interoperability-framework-cdif-discovery-module-v01-draft-for-public-consultation/) work may be of interest.  

The following section shows how we might express a link from the JSON-LD document back to the STAC catalog.
One could also put in the Radiant Earth browser link.  It might be interested to see if these links are typed
and also express that in the document.

```json
    "offers": {
        "@type": "Offer",
        "itemOffered": {
            "@type": "Service",
            "description": "A STAC Catalog Service",
            "potentialAction": {
                "@type": "Action",
                "target": "https://raw.githubusercontent.com/eco4cast/neon4cast-stac-catalog/main/stac/catalog.json"
            }
        }
    },
```

This is more placeholder than finished product.  It attempts to lay
the groundwork to enable the dataset to act as a discovery vector for the service.
Doing so begins to lay the foundation for something like the service layer of the FAIR 
Digital Objects concept and so raises the question of if resources like these can
be considered a FDOs.  

### FAIR Digital Objects

> Either make the current website enabled with signposting and or make a new repo that can be placed in Zenodo that 
> is also signposted or a FDO object in some manner.  Would be nice if this was a model that worked for both neon
> and also the hydrography group as well. 

It is also interesting to explore how this approach, JSON-LD, compares
to the STAC approach in the context of FAIR data principles and other factors.

This is, it seems, a similar issue to the notebooks and research / scholarly objects discusion.  


#### STAC vs. FAIR Digital Objects

| Feature                 | STAC                               | FAIR Digital Objects (FDO) |
|-------------------------|------------------------------------|----------------------------|
| **Purpose**              | Standardizes metadata for Earth observation assets | Enhances discoverability, accessibility, interoperability, and reusability of digital objects |
| **Focus**                | Earth observation data (imagery, radar, LiDAR, etc.) | Broad range of digital objects (scientific data, code, workflows, etc.) |
| **Schema**               | JSON-based schema                  | Flexible schema (can be domain-specific) |
| **Properties**           | Extensive properties for Earth observation data | Core properties focus on identification, access, reuse |
| **Extensions**           | Supports extensions for specific domains | Can be extended through profiles |
| **Community**            | Earth science community            | Broad scientific community   |


