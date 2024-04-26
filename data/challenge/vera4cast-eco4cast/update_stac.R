library(jsonlite)
library(arrow)
library(dplyr)
library(lubridate)

#reticulate::miniconda_path() |>
#  reticulate::use_miniconda()

#Generate EFI model metadata
source('catalog/model_metadata.R')

# catalog
print('BUILDING CATALOG')
source('catalog/catalog.R')

# forecasts
print('BUILDING FORECASTS')
source('catalog/forecasts/forecast_models.R')

rm(list = ls()) # remove all environmental vars between forecast and scores
gc()

# scores
print('BUILDING SCORES')
source('catalog/scores/scores_models.R')

rm(list = ls())
gc()

# inventory
print('BUILDING INVENTORY')
source('catalog/inventory/create_inventory_page.R')

rm(list = ls())
gc()

# summaries
print('BUILDING FORECAST SUMMARIES')
source('catalog/summaries/summaries_models.R')

rm(list = ls())
gc()

# targets
print('BUILDING TARGETS')
source('catalog/targets/create_targets_page.R')

rm(list = ls())
gc()

# noaa
print('BUILDING NOAA')
source('catalog/noaa_forecasts/noaa_forecasts.R')

rm(list = ls())
gc()

# sites
print('BUILDING SITES')
source('catalog/sites/build_sites_page.R')

