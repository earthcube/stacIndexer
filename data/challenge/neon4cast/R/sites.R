
source('R/stac_functions.R')
config <- yaml::read_yaml('challenge_configuration.yaml')
catalog_config <- config$catalog_config

## READ S3 INVENTORY FOR DATES
# s3_inventory <- arrow::s3_bucket("neon4cast-inventory",
#                                  endpoint_override = "data.ecoforecast.org",
#                                  anonymous = TRUE)

# s3_inventory <- arrow::s3_bucket(config$inventory_bucket,
#                                  endpoint_override = config$endpoint,
#                                  anonymous = TRUE)

s3_df <- duckdbfs::open_dataset(glue::glue("s3://anonymous@{config$inventory_bucket}/catalog?endpoint_override=",config$endpoint)) |>
  #dplyr::filter(...1 == "parquet", ...2 == {theme}) |>
  dplyr::select(model_id, reference_date, date) |>
  # dplyr::mutate(model_id = gsub("model_id=", "", model_id),
  #               reference_datetime =
  #                 gsub("reference_datetime=", "", reference_datetime),
  #               date = gsub("date=", "", date)) |>
  dplyr::collect()

#s3_df <- stac4cast::get_grouping(config$inventory_bucket, "aquatics")

s3_df <- s3_df |> filter(model_id != 'null')

theme_max_date <- max(s3_df$date)
theme_min_date <- min(s3_df$date)

theme_sites <- read_csv("https://raw.githubusercontent.com/eco4cast/neon4cast-targets/main/NEON_Field_Site_Metadata_20220412.csv", col_types = cols())
theme_sites$site_lat_lon <- lapply(1:nrow(theme_sites), function(i) c(theme_sites$field_longitude[i], theme_sites$field_latitude[i]))

build_description <- "This collection contains information to describe the NEON sites included in the forecasting challenge"

build_site_item(theme_id = 'sites',
                start_date = '2000-01-01',
                end_date = Sys.Date(),
                destination_path = 'stac/sites',
                theme_title = 'NEON Sites',
                collection_name = 'NEON Sites',
                #thumbnail_link = 'https://projects.ecoforecast.org/neon4cast-catalog/img/BONA_Twr.jpg',
                thumbnail_link = 'https://www.neonscience.org/sites/default/files/styles/max_2600x2600/public/2021-04/2021_04_graphic_Domain_Map_no-Titles-png.png?itok=7MsHPigZ',
                site_coords = theme_sites$site_lat_lon)

# build_site_theme(start_date = '2000-01-01',
#                  end_date = Sys.Date(),
#                  id_value = 'efi-sites',
#             theme_description = build_description,
#             theme_title = 'NEON Sites',
#             destination_path = "stac/sites/",
#             thumbnail_link = "https://projects.ecoforecast.org/neon4cast-catalog/img/BONA_Twr.jpg",
#             thumbnail_title = 'NEON Sites')
