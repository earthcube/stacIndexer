
def citation(p):
    citation_data = {
        "@type": "CreativeWork",
        "@id": "https://doi.org/10.1002/ecs2.4686",
        "url": p.get("url"),
        "name": p.get("name"),
        "description": "This paper summarizes the open community conventions developed by the Ecological Forecasting Initiative (EFI) for the common formatting and archiving of ecological forecasts and the metadata associated with these forecasts. ",
        "identifier":
            {
                "@type": "PropertyValue",
                "propertyID": "https://registry.identifiers.org/registry/doi",
                "value": "doi:10.1002/ecs2.4686",
                "url": "https://doi.org/10.1002/ecs2.4686"
            }
    }

    return citation_data
