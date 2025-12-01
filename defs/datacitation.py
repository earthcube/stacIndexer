def citation(p):
    if isinstance(p, list):
        return [citation(x) for x in p]  # list -> list of citations
    if not isinstance(p, dict):
        raise TypeError(f"citation() expects dict or list[dict], got {type(p)}")

    return {
        "@type": "CreativeWork",
        "@id": "https://doi.org/10.1002/ecs2.4686",
        "url": p.get("url"),
        "name": p.get("name"),
        "description": "This paper summarizes ...",
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "https://registry.identifiers.org/registry/doi",
            "value": "doi:10.1002/ecs2.4686",
            "url": "https://doi.org/10.1002/ecs2.4686"
        }
    }

