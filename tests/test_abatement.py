from goblin_fetcher.goblin_fetcher import DataFetcher
import os 

def main():
    data_path ="./data/"
    path = [os.path.join("./data", "instance_0.db"), os.path.join("./data", "instance_1.db")]

    fetch = DataFetcher(path)

    rate = 0.3

    abated_livestock = fetch.get_abated_climate_change_animal_emissions_aggregated(rate)
    abated_livestock.to_csv(os.path.join(data_path, "abated_climate_change_animal_emissions_aggregated.csv"))

    unabated_livestock = fetch.get_climate_change_animal_emissions_aggregated()
    unabated_livestock.to_csv(os.path.join(data_path, "climate_change_animal_emissions_aggregated.csv"))

    #get total abated climate change emissions 
    baseline_year = 2020
    target_year = 2050

    abated_climate_emissions_total =fetch.get_abated_climate_change_emissions_totals(baseline_year, target_year, rate)
    abated_climate_emissions_total.to_csv(os.path.join(data_path, "abated_climate_change_emissions_totals.csv"))

    #get total unabated climate change emissions
    unabated_climate_emissions_total = fetch.get_climate_change_emission_totals()
    unabated_climate_emissions_total.to_csv(os.path.join(data_path, "climate_change_emission_totals.csv"))

    #get land use 
    land_use = fetch.get_landuse_emissions_totals()
    land_use.to_csv(os.path.join(data_path, "land_use_emissions_totals.csv"))

    #get eutrophication totals
    eutrophication_totals = fetch.get_eutrophication_emission_totals()

    eutrophication_totals.to_csv(os.path.join(data_path, "eutrophication_emission_totals.csv"))

    #get abated eutrophication totals
    abated_eutrophication_totals = fetch.get_abated_eutrophication_emission_totals(rate)
    abated_eutrophication_totals.to_csv(os.path.join(data_path, "abated_eutrophication_emission_totals.csv"))



if __name__ == "__main__":  
    main()