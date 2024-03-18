
## read in model documentation and only grab models for Aquatics theme
library(tidyverse)
library(arrow)
library(stac4cast)
library(reticulate)
library(rlang)
library(RCurl)

source('R/stac_functions.R')

theme = 'beetles'

#get model ids
s3 <- s3_bucket("neon4cast-inventory", endpoint_override="data.ecoforecast.org", anonymous = TRUE)
paths <- open_dataset(s3$path("neon4cast-forecasts")) |> collect()
models_df <- paths |> filter(...1 == "parquet", ...2 == theme) |> distinct(...3)

theme_models <- models_df |>
  tidyr::separate(...3, c('name','model.id'), "=")


## just read in example forecast to extract schema information -- ask about better ways of doing this
reference_datetime <- '2022-08-22'
site_id <- 'ABBY'
model_id <- 'mean'
#variable_name <- 'temperature'

s3_schema <- arrow::s3_bucket(
  bucket = glue::glue("neon4cast-forecasts/parquet/{theme}/",
                      "model_id={model_id}/",
                      "reference_datetime={reference_datetime}/"),
  endpoint_override = "data.ecoforecast.org",
  anonymous = TRUE)
theme_df <- arrow::open_dataset(s3_schema) %>%
  filter(site_id == site_id)

## CREATE table for column descriptions
description_create <- data.frame(datetime = 'ISO 8601(ISO 2019)datetime the forecast starts from (a.k.a. issue time); Only needed if more than one reference_datetime is stored in a single file. Forecast lead time is thus datetime-reference_datetime. In a hindcast the reference_datetime will be earlier than the time the hindcast was actually produced (see pubDate in Section3). Date times are allowed to be earlier than the reference_datetime if a reanalysis/reforecast is run before the start of the forecast period. This variable was called start_time before v0.5 of the EFI standard.',
                                 site_id = 'For forecasts that are not on a spatial grid, use of a site dimension that maps to a more detailed geometry (points, polygons, etc.) is allowable. In general this would be documented in the external metadata (e.g., alook-up table that provides lon and lat); however in netCDF this could be handled by the CF Discrete Sampling Geometry data model.',
                                 family = 'For ensembles: “ensemble.” Default value if unspecified for probability distributions: Name of the statistical distribution associated with the reported statistics. The “sample” distribution is synonymous with “ensemble.”For summary statistics: “summary.”If this dimension does not vary, it is permissible to specify family as avariable attribute if the file format being used supports this (e.g.,netCDF).',
                                 parameter = 'ensemble member',
                                 variable = 'forecast variable',
                                 prediction = 'predicted forecast value',
                                 pubDate = 'date of publication',
                                 date = 'ISO 8601 (ISO 2019) datetime being predicted; follows CF convention http://cfconventions.org/cf-conventions/cf-conventions.html#time-coordinate. This variable was called time before v0.5 of the EFI convention. For time-integrated variables (e.g., cumulative net primary productivity), one should specify the start_datetime and end_datetime as two variables, instead of the single datetime. If this is not provided the datetime is assumed to be the MIDPOINT of the integration period.')



## READ IN MODEL METADATA

neon_docs <- read_csv('NEON_Challenge_Registration_2023-05-23.csv')


new_columns <- c('first.name.one',
                 'last.name.one',
                 'affiliation.one',
                 'email.one',
                 'team.name',
                 'first.name.two',
                 'last.name.two',
                 'affiliation.two',
                 'email.two',
                 'first.name.three',
                 'last.name.three',
                 'affiliation.three',
                 'email.two.three',
                 'first.name.four',
                 'last.name.four',
                 'affiliation.four',
                 'email.four',
                 'first.name.five',
                 'last.name.five',
                 'affiliation.five',
                 'email.five',
                 'first.name.six',
                 'last.name.six',
                 'affiliation.six',
                 'email.six',
                 'first.name.seven',
                 'last.name.seven',
                 'affiliation.seven',
                 'email.seven',
                 'first.name.eight',
                 'last.name.eight',
                 'affiliation.eight',
                 'email.eight',
                 'first.name.nine',
                 'last.name.nine',
                 'affiliation.nine',
                 'email.nine',
                 'first.name.ten',
                 'last.name.ten',
                 'affiliation.ten',
                 'email.ten',
                 'team.category',
                 'theme',
                 'model.id',
                 'model.description',
                 'model.uncertainty'
)

neon_docs <- neon_docs |>
  filter(theme == 'Beetles') |>
  select(`First Name`:`Email address`,
         `team-name`,
         `Team Member 2 - First Name` :`Team Member 10 - Email`,
         Team.Category:`model-uncertainty`)

names(neon_docs) <- new_columns

neon_docs <- neon_docs |>
  mutate(model.description = ifelse(is.na(model.description),'',model.description))


s3_df <- get_grouping(s3, theme)


info_extract <- arrow::s3_bucket("neon4cast-forecasts/parquet/", endpoint_override = "data.ecoforecast.org", anonymous = TRUE)


forecast_sites <- c()

#test_models <- c(aquatic_models$model.id[1:2], 'tg_arima')
## loop over model ids and extract components if present in metadata table
for (m in theme_models$model.id[1:2]){
  print(m)
  model_date_range <- s3_df |> filter(model_id == m) |> dplyr::summarise(min(date),max(date))
  model_min_date <- model_date_range$`min(date)`
  model_max_date <- model_date_range$`max(date)`

  model_var_site_info <- generate_vars_sites(m_id = m, theme = theme)
  # print(model_var_site_info[[1]])
  # print(model_var_site_info[[2]])

  forecast_sites <- append(forecast_sites,  get_site_coords(theme = theme, bucket = NULL, m_id = m)[[2]])

  if (m %in% neon_docs$model.id){
    print('has metadata')

    idx = which(neon_docs$model.id == m)

    build_model(model_id = neon_docs$model.id[idx],
                theme_id = theme,
                team_name = neon_docs$team.name[idx],
                model_description = neon_docs[idx,'model.description'][[1]],
                start_date = model_min_date,
                end_date = model_max_date,
                use_metadata = TRUE,
                var_values = model_var_site_info[[1]],
                var_keys = model_var_site_info[[3]][[1]],
                site_values = model_var_site_info[[2]],
                model_documentation = neon_docs,
                destination_path = "stac/beetles/forecasts/models",
                description_path = "stac/beetles/forecasts/models/asset-description.Rmd",
                aws_download_path = 'neon4cast-forecasts/beetles/phenology',
                theme_title = "Forecasts",
                collection_name = 'forecasts',
                thumbnail_image_name = 'latest_forecast.png',
                table_schema = theme_df,
                table_description = description_create)
  } else{

    build_model(model_id = m,
                theme_id = theme,
                team_name = 'pending',
                model_description = 'pending',
                start_date = model_min_date,
                end_date = model_max_date,
                use_metadata = FALSE,
                var_values = model_var_site_info[[1]],
                var_keys = model_var_site_info[[3]][[1]],
                site_values = model_var_site_info[[2]],
                model_documentation = neon_docs,
                destination_path = "stac/beetles/forecasts/models",
                description_path = "stac/beetles/forecasts/asset-description.Rmd",
                aws_download_path = 'neon4cast-forecasts/parquet/beetles',
                theme_title = "Forecasts",
                collection_name = 'forecasts',
                thumbnail_image_name = 'latest_forecast.png',
                table_schema = theme_df,
                table_description = description_create)
  }

  rm(model_var_site_info)
}

forecast_sites <- unique(forecast_sites)
forecast_sites_df <- data.frame(site_id = forecast_sites)

write.csv(forecast_sites_df, 'stac/beetles/forecasts/all_forecast_sites.csv', row.names = FALSE)
