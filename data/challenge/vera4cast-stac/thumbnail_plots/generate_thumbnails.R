library(arrow)
library(tidyverse)
library(ggplot2)
library(minioclient)

#theme <- 'beetles'

#get model ids
# s3 <- s3_bucket("neon4cast-inventory", endpoint_override="data.ecoforecast.org", anonymous = TRUE)
# paths <- open_dataset(s3$path("neon4cast-scores")) |> collect()
# models_df <- paths |> filter(...1 == "parquet", ...2 == theme) |> distinct(...3)
#
# theme_models <- models_df |>
#   tidyr::separate(...3, c('name','model.id'), "=")

# info_extract <- arrow::s3_bucket("neon4cast-scores/parquet/", endpoint_override = "data.ecoforecast.org", anonymous = TRUE)


theme_models <- duckdbfs::open_dataset(glue::glue("s3://{config$inventory_bucket}/catalog"),
                                         s3_endpoint = "amnh1.osn.mghpcc.org", anonymous=TRUE) |>
  collect()

theme_models <- theme_models |>
  distinct(model_id)


## save climatology data
#aquatics / phenology
# baseline_df <- arrow::open_dataset(info_extract$path(glue::glue("{theme}/model_id=climatology/"))) |>
#   # filter(reference_datetime == latest_forecast_date,
#   #        datetime %in% latest_forecast$datetime) |>
#   collect()


baseline_df <- scores_theme_df <- arrow::open_dataset(arrow::s3_bucket(config$scores_bucket, endpoint_override = "amnh1.osn.mghpcc.org", anonymous = TRUE)) |>
  filter(model_id == 'climatology')


#test_models <- c(aquatic_models$model.id[1:2], 'tg_arima')

for (m_id in theme_models$model_id[1:2]){
  print(m_id)

  info_df <- arrow::open_dataset(info_extract$path(glue::glue("{theme}/model_id={m_id}/"))) |>
    collect()

  # latest_forecast_date <- max(info_df$reference_datetime)
  #
  # latest_forecast <- info_df |>
  #  filter(reference_datetime == latest_forecast_date)

  #latest_forecast$horizon <- as.Date(latest_forecast$datetime) - as.Date(latest_forecast$reference_datetime)


  for (site in unique(info_df$site_id)){
    print(site)

    ## FORECAST
    latest_forecast_df <- info_df |>
      filter(site_id == site,
             reference_datetime == max(reference_datetime))

    ## check if path for image exists locally
    img_save_path <- file.path("thumbnail_store",m_id,theme,site)

    if (file.exists(img_save_path) == FALSE){
      print('creating new dir')
      dir.create(img_save_path, recursive = TRUE)
    }

    # Forecast Plot -- uses scores data. Raw forecasts might not be useful
    forecast_plot <- ggplot(data = latest_forecast_df, aes(datetime, mean)) +
      geom_line(color = "steelblue", linewidth = 1) +
      ggplot2::geom_ribbon(aes(ymin = quantile10, ymax = quantile90), alpha = 0.2) +
      labs(title = paste0("Latest Forecast for ", site," (",unique(latest_forecast_df$reference_datetime),')'),
           subtitle = "(plots include the mean and the +- 90% CI)",
           y = "Forecast value", x = "Date") +
      facet_grid(variable ~ ., scales = "free_y") +
      theme_bw() +
      theme(plot.title = element_text(hjust = 0.5),
            plot.subtitle=element_text(hjust=0.5))

    forecast_img_path <- paste0(img_save_path,'/latest_forecast.png')

    ggsave(filename = forecast_img_path, plot = forecast_plot,height = 6, width = 8)

    mc_cp(forecast_img_path, glue::glue("efi/neon4cast-catalog/{theme}/{m_id}/{site}/latest_forecast.png"))


    ## SCORES --  CHECK TO SEE IF CLIMATOLOGY EXISTS

    latest_scores_site <- info_df |>
      filter(site_id == site,
             reference_datetime < (as.Date(Sys.Date()) - days(30))) |>
      group_by(reference_datetime) |>
      mutate(max_horizon = max(as.Date(datetime)) - as.Date(reference_datetime)) |>
      ungroup() |>
      distinct(reference_datetime, .keep_all = TRUE) |>
      filter(max_horizon == max(max_horizon)) |>
      filter(reference_datetime == max(reference_datetime))

    baseline_site_df <- baseline_df |>
      filter(site_id == site) |>
      filter(reference_datetime == latest_scores_site$reference_datetime) |>
      #filter(datetime %in% latest_scores_site$date) |>
      rename(clim_crps = crps) |>
      select(datetime,variable, clim_crps)

    if (nrow(baseline_site_df) == 0){
      print(paste0('no climatology forecast for ',{site}, ' on ', {latest_scores_site$reference_datetime}))
      next
    }

    latest_scores_df <- info_df |>
      filter(site_id == site,
             reference_datetime == latest_scores_site$reference_datetime) |>
      right_join(baseline_site_df, by = c('datetime','variable'))

    # Scores plot
    scores_plot <- ggplot(data = latest_scores_df, aes(datetime, crps)) +
      geom_line(color = "steelblue", linewidth = 1) +
      geom_line(aes(y = clim_crps), color = 'darkred', linetype = 'dashed') +
      labs(title = paste0("Latest Scores for ", site," (",latest_scores_site$reference_datetime,')'),
           subtitle = "modeled CRPS score (blue) and the climatology CRPS score (red)",
           y = "CRPS Score", x = "Horizon (Days)") +
      facet_grid(variable ~ ., scale = "free_y") +
      theme_bw() +
      theme(plot.title = element_text(hjust = 0.5),
            plot.subtitle=element_text(hjust=0.5))

    ##save plot
    scores_img_path <- paste0(img_save_path,'/latest_scores.png')

    ggsave(filename = scores_img_path, plot = scores_plot, height = 6, width = 8)

    mc_cp(scores_img_path, glue::glue("efi/neon4cast-catalog/{theme}/{m_id}/{site}/latest_scores.png"))

    print('--- done ---')


    #mc_alias_set("efi", endpoint="data.ecoforecast.org", access='austin', secret='RokQD3E8mJUFpUbn') # needed only once per machine
  }

}


#
#
# ## MAKE NEW SCORES PLOT (average crps for all reference datetimes from model/site)
#
# info_df <- arrow::open_dataset(info_extract$path(glue::glue("{theme}/model_id={m_id}/"))) |>
#   collect()
#
# latest_forecast_date <- max(info_df$reference_datetime)
#
# latest_forecast_site <- info_df |>
#   filter(reference_datetime == latest_forecast_date,
#          site_id == site)
#
# ## for loop (model)
# info_df <- arrow::open_dataset(info_extract$path(glue::glue("{theme}/model_id={m_id}/"))) |>
#   collect()
#
# latest_forecast_date <- max(info_df$reference_datetime)
#
# # for loop (site)
#
# latest_forecast$horizon <- as.Date(latest_forecast$datetime) - as.Date(latest_forecast$reference_datetime)
#
# # site_df <- info_df |>
# #   filter(site_id == site) |>
# #   group_by(variable, reference_datetime) |>
# #   mutate(crps_mean = mean(crps, na.rm = TRUE)) |>
# #   ungroup() |>
# #   distinct(variable, reference_datetime, .keep_all = TRUE) |>
# #   select(reference_datetime, site_id, variable, crps_mean)
# #
# # clim_site_df <- climatology_df |>
# #   filter(site_id == site,
# #          reference_datetime %in% site_df$reference_datetime) |>
# #   group_by(variable, reference_datetime) |>
# #   mutate(crps_mean = mean(crps, na.rm = TRUE)) |>
# #   ungroup() |>
# #   distinct(variable, reference_datetime, .keep_all = TRUE)
#
#
# info_df <- arrow::open_dataset(info_extract$path(glue::glue("{theme}/model_id={m_id}/"))) |>
#   collect()
#
# site <- 'BARC'
# today <- Sys.Date()
#
# latest_forecast_site <- info_df |>
#   filter(site_id == site,
#          reference_datetime < (as.Date(Sys.Date()) - days(30))) |>
#   group_by(reference_datetime) |>
#   mutate(max_horizon = max(as.Date(datetime)) - as.Date(reference_datetime)) |>
#   ungroup() |>
#   distinct(reference_datetime, .keep_all = TRUE) |>
#   filter(max_horizon == max(max_horizon)) |>
#   filter(reference_datetime == max(reference_datetime))
