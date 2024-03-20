# Notes

```text
9291041754864156672
```

https://stko-kwg.geog.ucsb.edu/browse/#kwgr:s2.level11.9291041754864156672

https://stko-kwg.geog.ucsb.edu/browse/#kwgr:smokeplumesnapshot.3135.2018-08-02.7


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