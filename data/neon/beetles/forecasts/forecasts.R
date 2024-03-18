library(arrow)
library(dplyr)

source('R/stac_functions.R')

## CREATE table for column descriptions
description_create <- data.frame(datetime = 'ISO 8601(ISO 2019)datetime the forecast starts from (a.k.a. issue time); Only needed if more than one reference_datetime is stored in a single file. Forecast lead time is thus datetime-reference_datetime. In a hindcast the reference_datetime will be earlier than the time the hindcast was actually produced (see pubDate in Section3). Date times are allowed to be earlier than the reference_datetime if a reanalysis/reforecast is run before the start of the forecast period. This variable was called start_time before v0.5 of the EFI standard.',
                                 site_id = 'For forecasts that are not on a spatial grid, use of a site dimension that maps to a more detailed geometry (points, polygons, etc.) is allowable. In general this would be documented in the external metadata (e.g., alook-up table that provides lon and lat); however in netCDF this could be handled by the CF Discrete Sampling Geometry data model.',
                                 family = 'For ensembles: “ensemble.” Default value if unspecified for probability distributions: Name of the statistical distribution associated with the reported statistics. The “sample” distribution is synonymous with “ensemble.”For summary statistics: “summary.”If this dimension does not vary, it is permissible to specify family as avariable attribute if the file format being used supports this (e.g.,netCDF).',
                                 parameter = 'ensemble member',
                                 variable = 'forecast variable',
                                 prediction = 'predicted forecast value',
                                 pubDate = 'date of publication',
                                 date = 'ISO 8601 (ISO 2019) datetime being predicted; follows CF convention http://cfconventions.org/cf-conventions/cf-conventions.html#time-coordinate. This variable was called time before v0.5 of the EFI convention. For time-integrated variables (e.g., cumulative net primary productivity), one should specify the start_datetime and end_datetime as two variables, instead of the single datetime. If this is not provided the datetime is assumed to be the MIDPOINT of the integration period.')

## just read in example forecast to extract schema information -- ask about better ways of doing this
theme <- 'beetles'
reference_datetime <- '2022-08-15'
site_id <- 'ABBY'
model_id <- 'mean'
variable_name <- 'temperature'

s3_schema <- arrow::s3_bucket(
  bucket = glue::glue("neon4cast-forecasts/parquet/{theme}/",
                      "model_id={model_id}/",
                      "reference_datetime={reference_datetime}/"),
  endpoint_override = "data.ecoforecast.org",
  anonymous = TRUE)
theme_df <- arrow::open_dataset(s3_schema) %>%
  filter(site_id == site_id)

## identify model ids from bucket -- used in generate model items function
s3 <- s3_bucket("neon4cast-inventory", endpoint_override="data.ecoforecast.org", anonymous = TRUE)
paths <- open_dataset(s3$path("neon4cast-forecasts")) |> collect()
models_df <- paths |> filter(...1 == "parquet", ...2 == theme) |> distinct(...3)
theme_models <- models_df |>
  tidyr::separate(...3, c('name','model.id'), "=")

## use s3_inventory to access min and max dates
s3_df <- get_grouping(s3, theme)
s3_df <- s3_df |> filter(model_id != 'null')

forecast_max_date <- max(s3_df$date)
forecast_min_date <- min(s3_df$date)


build_description <- "The catalog contains forecasts for the NEON Ecological Forecasting beetles theme. The forecasts are the raw forecasts that include all ensemble members (if a forecast represents uncertainty using an ensemble).  Due to the size of the raw forecasts, we recommend accessing the scores (summaries of the forecasts) to analyze forecasts (unless you need the individual ensemble members). You can access the forecasts at the top level of the dataset where all models, variables, and dates that forecasts were produced (reference_datetime) are available. The code to access the entire dataset is provided as an asset. Given the size of the forecast catalog, it can be time-consuming to access the data at the full dataset level. For quicker access to the forecasts for a particular model (model_id), we also provide the code to access the data at the model_id level as an asset for each model."

build_forecast_scores(table_schema = theme_df,
                      theme_id = theme,
                      table_description = description_create,
                      start_date = forecast_min_date,
                      end_date = forecast_max_date,
                      id_value = "beetles-forecasts",
                      description_string = build_description,
                      about_string = 'https://projects.ecoforecast.org/neon4cast-docs/',
                      about_title = "NEON Ecological Forecasting Challenge Documentation",
                      theme_title = "Forecasts",
                      model_documentation ="https://raw.githubusercontent.com/eco4cast/neon4cast-targets/main/NEON_Field_Site_Metadata_20220412.csv",
                      destination_path = "stac/beetles/forecasts/",
                      description_path = 'stac/aquatics/beetles/asset-description.Rmd',
                      aws_download_path = 'neon4cast-scores/beetles/phenology')

