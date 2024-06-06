from goblin_fetcher.goblin_fetcher import DataFetcher
import os 

def main():
    data_path ="./data/"
    path = [os.path.join("./data", "instance_0.db"), os.path.join("./data", "instance_1.db")]

    fetch = DataFetcher(path)

    #get total abated climate change emissions 
    baseline_year = 2020
    target_year = 2050

    time_series = fetch.get_climate_landuse_totals_time_series(baseline_year, target_year)

    #save to csv
    time_series.to_csv(os.path.join(data_path, "climate_landuse_totals_time_series.csv"))

    #time series livestock 
    time_series_livestock = fetch.get_climate_livestock_totals_time_series(baseline_year, target_year)

    #save to csv
    time_series_livestock.to_csv(os.path.join(data_path, "climate_livestock_totals_time_series.csv"))

    #time series forests
    time_series_forests = fetch.get_climate_forest_totals_time_series(baseline_year, target_year)

    #save to csv
    time_series_forests.to_csv(os.path.join(data_path, "climate_forest_totals_time_series.csv"))

    #get totals time series data 
    time_series_totals = fetch.get_climate_totals_time_series(baseline_year, target_year)

    #save to csv
    time_series_totals.to_csv(os.path.join(data_path, "climate_totals_time_series.csv"))

    rate = 0.3

    #get abated totals 
    abated_totals = fetch.get_abated_climate_totals_time_series(baseline_year, target_year, rate)

    #save to csv
    abated_totals.to_csv(os.path.join(data_path, "abated_climate_totals_time_series.csv"))


if __name__ == "__main__":  
    main()