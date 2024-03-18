
source("R/catalog-common.R")
source('R/stac_functions.R')

build_catalog <- function(){
catalog <- list(
  "type"= "Catalog",
  "id"= "efi-stac",
  "title"= "Ecological Forecasting Initiative STAC API",
  "description"= "Searchable spatiotemporal metadata describing forecasts by the Ecological Forecasting Initiative",
  "stac_version"= "1.0.0",
  "conformsTo"= 'conformsTo',
  "links"= list(
    list(
      "rel"= "self",
      "type"= "application/json",
      "href" = 'catalog.json'
    ),
    list(
      "rel"= "root",
      "type"= "application/json",
      "href" = 'catalog.json'
    ),

    # list(
    #   "rel"= "child",
    #   "type"= "application/json",
    #   "title"= "NOAA Global Ensemble Forecast System",
    #   "href" = 'noaa/collection.json'
    # ),
    list(
      "rel"= "child",
      "type"= "application/json",
      "title"= "Aquatics Forecast Challenge",
      "href" = 'aquatics/collection.json'),
    list(
      "rel"= "child",
      "type"= "application/json",
      "title"= "NEON Site Information",
      "href" = 'sites/collection.json'),
  list(
    "rel"= "child",
    "type"= "application/json",
    "title"= "Phenology Forecast Challenge",
    "href" = 'phenology/collection.json'),
  list(
    "rel"= "child",
    "type"= "application/json",
    "title"= "Beetles Forecast Challenge",
    "href" = 'beetles/collection.json'
  ),
  list(
    "rel"= "child",
    "type"= "application/json",
    "title"= "Terrestrial Forecast Challenge (30min)",
    "href" = 'terrestrial_30min/collection.json'
  ),
  list(
    "rel"= "child",
    "type"= "application/json",
    "title"= "Terrestrial Forecast Challenge (Daily)",
    "href" = 'terrestrial_daily/collection.json'
  ),
  list(
    "rel"= "child",
    "type"= "application/json",
    "title"= "Ticks Forecast Challenge",
    "href" = 'ticks/collection.json'
  )
  )
)
    # ),
    # list(
    #   "rel"= "child",
    #   "type"= "application/json",
    #   "title"= "Terrestrial Forecast Challenge",
    #   "href" = 'terrestrial/collection.json'
    #
    # ),
#)

dest <- "stac/"
jsonlite::write_json(catalog, file.path(dest, "catalog.json"),
                     pretty=TRUE, auto_unbox=TRUE)
stac4cast::stac_validate(file.path(dest, "catalog.json"))

}

build_catalog()
