library(arrow)
library(dplyr)
library(gsheet)
library(readr)

#source('catalog/R/stac_functions.R')
config <- yaml::read_yaml('challenge_configuration.yaml')
catalog_config <- config$catalog_config

## CREATE table for column descriptions
site_description_create <- data.frame(site = 'unique site name',
                                         site_id = 'unique site identifier',
                                         max_depth_m = 'maximum depth of the site in meters',
                                         surface_area_km2 = 'surface area of the site in square kilometers',
                                         latitude = 'site latitude',
                                         longitude = 'site longitude')

#inventory_theme_df <- arrow::open_dataset(glue::glue("s3://{config$inventory_bucket}/catalog/forecasts/project_id={config$project_id}"), endpoint_override = config$endpoint, anonymous = TRUE) #|>

#target_url <- "https://renc.osn.xsede.org/bio230121-bucket01/vera4cast/targets/project_id=vera4cast/duration=P1D/daily-insitu-targets.csv.gz"
site_df <- read_csv(config$site_table, show_col_types = FALSE)

# inventory_theme_df <- arrow::open_dataset(arrow::s3_bucket(config$inventory_bucket, endpoint_override = config$endpoint, anonymous = TRUE))
#
# inventory_data_df <- duckdbfs::open_dataset(glue::glue("s3://{config$inventory_bucket}/catalog"),
#                                             s3_endpoint = config$endpoint, anonymous=TRUE) |>
#   collect()
#
# theme_models <- inventory_data_df |>
#   distinct(model_id)

# target_date_range <- targets |> dplyr::summarise(min(datetime),max(datetime))
# target_min_date <- as.Date(target_date_range$`min(datetime)`)
# target_max_date <- as.Date(target_date_range$`max(datetime)`)

build_description <- paste0("The catalog contains site metadata for the ", config$challenge_long_name)


stac4cast::build_sites(table_schema = site_df,
                         table_description = site_description_create,
                         # start_date = target_min_date,
                         # end_date = target_max_date,
                         id_value = "sites",
                         description_string = build_description,
                         about_string = catalog_config$about_string,
                         about_title = catalog_config$about_title,
                         theme_title = "Site Metadata",
                         destination_path = config$site_path,
                         #link_items = stac4cast::generate_group_values(group_values = names(config$variable_groups)),
                         link_items = NULL,
                         thumbnail_link = config$site_thumbnail,
                         thumbnail_title = config$site_thumbnail_title)
