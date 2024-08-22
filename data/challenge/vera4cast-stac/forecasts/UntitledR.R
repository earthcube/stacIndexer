all_results <- arrow::open_dataset("s3://anonymous@bio230121-bucket01/vera4cast/forecasts/parquet/?endpoint_override=renc.osn.xsede.org")

t <- all_results |>
  filter(site_id == 'fcre') |>
  filter(variable == 'Temp_C_mean') |>
  collect()

met_results <- arrow::open_dataset("s3://anonymous@bio230121-bucket01/flare/drivers/met/gefs-v12/stage2?endpoint_override=renc.osn.xsede.org")
df <- met_results |>
  distinct(variable) |>
  dplyr::collect()

met_s3_future <- arrow::s3_bucket(file.path("bio230121-bucket01/flare/drivers/met/gefs-v12/stage2",paste0("reference_datetime=2024-03-01"),paste0("site_id=fcre")),
                                  endpoint_override = 'renc.osn.xsede.org',
                                  anonymous = TRUE)
df <- arrow::open_dataset(met_s3_future) |>
  distinct(variable) |>
  dplyr::collect()


## water temp
s3_path <- arrow::s3_bucket(paste0("scores/parquet"),
                            endpoint_override = "s3.flare-forecast.org",
                            anonymous = TRUE)

df_future <- arrow::open_dataset(s3_path) |>
  dplyr::filter(site_id == 'fcre',
         variable == 'Temp_C_mean') |>
  dplyr::collect()

min(df_future$reference_datetime)


# old_forecasts <- arrow::s3_bucket(file.path("bio230121-bucket01/vt_backup/forecasts",paste0("reference_datetime=2024-03-01"),paste0("site_id=fcre")),
#                                                    endpoint_override = 'renc.osn.xsede.org',
#                                                    anonymous = TRUE)

old_bucket_forecasts <- arrow::s3_bucket(file.path("bio230121-bucket01/vt_backup/forecasts/parquet/site_id=fcre/"),
                                  endpoint_override = 'renc.osn.xsede.org',
                                  anonymous = TRUE)

df_old <- arrow::open_dataset(old_forecasts) |>
  filter(variable == 'salt') |>
  distinct(variable) |>
  dplyr::collect()

## old met
old_met_bucket <- arrow::s3_bucket(file.path("bio230121-bucket01/vt_backup/drivers/noaa/gefs-v12-reprocess/"),
                                         endpoint_override = 'renc.osn.xsede.org',
                                         anonymous = TRUE)

df_old_met <- arrow::open_dataset(old_met_bucket) |>
  dplyr::filter(site_id == 'fcre') |>
  distinct(variable) |>
  dplyr::collect()


  #,
         #reference_datetime > lubridate::as_datetime('2023-08-01')) |>
  #dplyr::distinct(variable) |>
  dplyr::collect()
