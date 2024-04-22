from goblin_fetcher.goblin_fetcher import DataFetcher
import os 

def main():
    data_path ="./data/"
    path = [os.path.join("./data", "instance_0.db"), os.path.join("./data", "instance_1.db")]

    fetch = DataFetcher(path)

    fetch.get_air_quality_animal_emissions_by_category().to_csv(os.path.join(data_path, "air_quality_animal_emissions_by_category.csv"))

    fetch.get_crop_national_inputs().to_csv(os.path.join(data_path, "crop_national_inputs.csv"))

if __name__ == "__main__":  
    main()