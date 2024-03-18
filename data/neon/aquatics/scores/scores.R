library(arrow)
library(dplyr)

source('R/stac_functions.R')

## CREATE table for column descriptions
description_create <- data.frame(reference_datetime ='ISO 8601(ISO 2019) datetime the forecast starts from (a.k.a. issue time); Only needed if more than one reference_datetime is stored in a single file. Forecast lead time is thus datetime-reference_datetime. In a hindcast the reference_date time will be earlier than the time the hindcast was actually produced (see pubDate in Section 3). Datetimes are allowed to be earlier than the reference_datetime if analysis/reforecast is run before the start of the forecast period. This variable was called start_time before v0.5 of the EFI standard.',
                                 site_id = 'For forecasts that are not on a spatial grid, use of a site dimension that maps to a more detailed geometry (points, polygons, etc.) is allowable. In general this would be documented in the external metadata (e.g., alook-up table that provides lon and lat); however in netCDF this could be handled by the CF Discrete Sampling Geometry data model.',
                                 datetime = 'ISO 8601(ISO 2019) datetime the forecast starts from (a.k.a. issue time); Only needed if more than one reference_datetime is stored in a single file. Forecast lead time is thus datetime-reference_datetime. In a hindcast the reference_date time will be earlier than the time the hindcast was actually produced (see pubDate in Section 3). Datetimes are allowed to be earlier than the reference_datetime if analysis/reforecast is run before the start of the forecast period. This variable was called start_time before v0.5 of the EFI standard.',
                                 family = 'For ensembles: “ensemble.” Default value if unspecified For probability distributions: Name of the statistical distribution associated with the reported statistics. The “sample” distribution is synonymous with “ensemble.” For summary statistics: “summary.”If this dimension does not vary, it is permissible to specify family as a variable attribute if the file format being used supports this (e.g.,netCDF).',
                                 variable = 'aquatic forecast variable',
                                 pubDate = 'ISO 8601 (ISO 2019) datetime being predicted; follows CF convention http://cfconventions.org/cf-conventions/cf-conventions.html#time-coordinate. This variable was called time before v0.5of the EFI convention.For time-integrated variables (e.g., cumulative net primary productivity), one should specify the start_datetime and end_datetime as two variables, instead of the single datetime. If this is not provided the datetime is assumed to be the MIDPOINT of the integration period.',
                                 observation = 'observational data',
                                 crps = 'crps forecast score',
                                 logs = 'logs forecast score',
                                 mean = 'mean forecast prediction for all ensemble members',
                                 median = 'median forecast prediction for all ensemble members',
                                 sd = 'standard deviation of all enemble member forecasts',
                                 quantile97.5 = 'upper 97.5 percentile value of ensemble member forecasts',
                                 quantile02.5 = 'upper 2.5 percentile value of ensemble member forecasts',
                                 quantile90 = 'upper 90 percentile value of ensemble member forecasts',
                                 quantile10 = 'upper 10 percentile value of ensemble member forecasts',
                                 date = 'ISO 8601 (ISO 2019) datetime being predicted; follows CF convention http://cfconventions.org/cf-conventions/cf-conventions.html#time-coordinate. This variable was called time before v0.5of the EFI convention. For time-integrated variables (e.g., cumulative net primary productivity), one should specify the start_datetime and end_datetime as two variables, instead of the single datetime. If this is not provided the datetime is assumed to be the MIDPOINT of the integration period.')

## just read in example forecast to extract schema information -- ask about better ways of doing this
theme <- 'aquatics'
reference_date <- '2023-05-01'
site_id <- 'BARC'
model_id <- 'flareGLM'
variable_name <- 'temperature'

s3_schema <- arrow::s3_bucket(
  bucket = glue::glue("neon4cast-scores/parquet/{theme}/",
                      "model_id={model_id}/"),
  endpoint_override = "data.ecoforecast.org",
  anonymous = TRUE)

theme_df <- arrow::open_dataset(s3_schema) %>%
  filter(reference_datetime == reference_date)

## identify model ids from bucket
s3 <- s3_bucket("neon4cast-inventory", endpoint_override="data.ecoforecast.org", anonymous = TRUE)
paths <- open_dataset(s3$path("neon4cast-scores")) |> collect()
models_df <- paths |> filter(...1 == "parquet", ...2 == "aquatics") |> distinct(...3)
aquatic_models <- models_df |>
  tidyr::separate(...3, c('name','model.id'), "=")

## identify model ids from bucket -- used in generate model items function
s3_inventory <- s3_bucket("neon4cast-inventory", endpoint_override="data.ecoforecast.org", anonymous = TRUE)
paths <- open_dataset(s3_inventory$path("neon4cast-scores")) |> collect()
models_df <- paths |> filter(...1 == "parquet", ...2 == "aquatics") |> distinct(...3)
aquatic_models <- models_df |>
  tidyr::separate(...3, c('name','model.id'), "=")

## use s3_inventory to access min and max dates
s3_df <- get_grouping(s3_inventory, "aquatics")
s3_df <- s3_df |> filter(model_id != 'null')

forecast_max_date <- max(s3_df$date)
forecast_min_date <- min(s3_df$date)

build_description <- "The catalog contains scores for the NEON Ecological Forecasting aquatics theme.  The scores are summaries of the forecasts (i.e., mean, median, confidence intervals), matched observations (if available), and scores (metrics of how well the model distribution compares to observations). You can access the scores at the top level of the dataset where all models, variables, and dates that forecasts were produced (reference_datetime) are available. The code to access the entire dataset is provided as an asset. Given the size of the scores catalog, it can be time-consuming to access the data at the full dataset level. For quicker access to the scores for a particular model (model_id), we also provide the code to access the data at the model_id level as an asset for each model."

build_forecast_scores(table_schema = theme_df,
                      theme_id = theme,
               table_description = description_create,
               start_date = forecast_min_date,
               end_date = forecast_max_date,
               id_value = "aquatics-scores",
               description_string = build_description,
               about_string = 'https://projects.ecoforecast.org/neon4cast-docs/',
               about_title = "NEON Ecological Forecasting Challenge Documentation",
               theme_title = "Scores",
               model_documentation ="https://raw.githubusercontent.com/eco4cast/neon4cast-targets/main/NEON_Field_Site_Metadata_20220412.csv",
               destination_path = "stac/aquatics/scores/",
               description_path = 'stac/aquatics/scores/asset-description.Rmd',
               aws_download_path = 'neon4cast-scores/parquet/aquatics')

