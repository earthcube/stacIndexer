source('R/stac_functions.R')


## READ S3 INVENTORY FOR DATES
s3_inventory <- arrow::s3_bucket("neon4cast-inventory",
                                 endpoint_override = "data.ecoforecast.org",
                                 anonymous = TRUE)

s3_df <- get_grouping(s3_inventory, "beetles")

s3_df <- s3_df |> filter(model_id != 'null')

theme_max_date <- max(s3_df$date)
theme_min_date <- min(s3_df$date)

build_description <- "The catalog contains forecasts and scores for the NEON Ecological Forecasting Beetles theme.  The forecasts are the raw forecasts that include all ensemble members (if a forecast represents uncertainty using an ensemble).  The scores are summaries of the forecasts (i.e., mean, median, confidence intervals), matched observations (if available), and scores (metrics of how well the model distribution compares to observations). Due to the size of the raw forecasts, we recommend accessing the scores to analyze forecasts (unless you need the individual ensemble members).\nYou can access the forecasts or the scores at the top level of the dataset where all models, variables, and dates that forecasts were produced (reference_datetime) are available.  The code to access the entire dataset is provided as an asset in the forecast or scores catalog. Given the size of the forecast catalog, it can be time-consuming to access the data at the full dataset level.  For quicker access to the forecasts and scores for a particular model (model_id), we also provide the code to access the data at the model_id level as an asset for each model."

build_theme(start_date = theme_min_date,
            end_date = theme_max_date,
            id_value = 'efi-beetles',
            theme_description = build_description,
            theme_title = 'Beetles',
            destination_path = "stac/beetles/",
            thumbnail_link = 'https://www.neonscience.org/sites/default/files/styles/max_width_1170px/public/image-content-images/Beetles_pinned.jpg',
            thumbnail_title = 'Beetle Image')
