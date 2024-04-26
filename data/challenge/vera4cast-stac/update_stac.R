library(jsonlite)
library(arrow)
library(dplyr)
library(lubridate)

#reticulate::miniconda_path() |>
#  reticulate::use_miniconda()

#Generate EFI model metadata
source('catalog/model_metadata.R')

# catalog
source('catalog/catalog.R')

# forecasts
source('catalog/forecasts/forecast_models.R')

rm(list = ls()) # remove all environmental vars between forecast and scores

# scores
source('catalog/scores/scores_models.R')

rm(list = ls())

# inventory
source('catalog/inventory/create_inventory_page.R')

rm(list = ls())

# summaries
source('catalog/summaries/summaries_models.R')

rm(list = ls())

# targets
source('catalog/targets/create_targets_page.R')

rm(list = ls())

# noaa
source('catalog/noaa_forecasts/noaa_forecasts.R')


## Call healthcheck
#RCurl::url.exists("https://hc-ping.com/3ca7c26c-243e-4405-a3e9-a8381a923def", timeout = 5)
