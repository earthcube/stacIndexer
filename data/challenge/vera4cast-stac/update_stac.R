library(jsonlite)
library(arrow)
library(dplyr)
library(lubridate)

#reticulate::miniconda_path() |>
#  reticulate::use_miniconda()

#Generate EFI model metadata
print('METADATA')
source('catalog/model_metadata.R')

# catalog
print("CATALOG TOP")
source('catalog/catalog.R')

# forecasts
print('FORECASTS')
source('catalog/forecasts/forecast_models.R')

rm(list = ls()) # remove all environmental vars between forecast and scores

# scores
print('SCORES')
source('catalog/scores/scores_models.R')

rm(list = ls())

# inventory
print('INVENTORY')
source('catalog/inventory/create_inventory_page.R')

rm(list = ls())

# summaries
print('SUMMARIES')
source('catalog/summaries/summaries_models.R')

rm(list = ls())

# targets
print('TARGETS')
source('catalog/targets/create_targets_page.R')

rm(list = ls())

# noaa
print('NOAA')
source('catalog/noaa_forecasts/noaa_forecasts.R')


## Call healthcheck
#RCurl::url.exists("https://hc-ping.com/3ca7c26c-243e-4405-a3e9-a8381a923def", timeout = 5)
