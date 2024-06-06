import unittest
from goblin_fetcher.goblin_fetcher import DataFetcher
import os
import pandas as pd

class TestClimateAbateLivestock(unittest.TestCase):

    def setUp(self):
        self.path = [os.path.join("./data", "instance_0.db"), os.path.join("./data", "instance_1.db")]
        self.fetcher = DataFetcher(self.path)
        self.rate = 0.3


    def test_eutrophication_abate(self):
        abated_eutrophication = self.fetcher.get_abated_eutrophication_emission_totals(self.rate)
        unabated_eutrophication = self.fetcher.get_eutrophication_emission_totals()

        filter0_abated = abated_eutrophication[abated_eutrophication.Scenarios == -1].copy(deep=True)
        filter0_unabated = unabated_eutrophication[unabated_eutrophication.Scenarios == -1].copy(deep=True)

        categories = ["manure_management", "soils", "Total"]
        for cat in categories:
            abated_values = filter0_abated[cat]
            unabated_values = filter0_unabated[cat]

            # Check that values are almost equal
            for actual, expected in zip(abated_values, unabated_values):
                self.assertAlmostEqual(actual, expected, places=2)

        filter1_abated = abated_eutrophication[abated_eutrophication.Scenarios != -1].copy(deep=True)
        filter1_unabated = unabated_eutrophication[unabated_eutrophication.Scenarios != -1].copy(deep=True)

        # Assert that abated values are 30% less than unabated values
        for cat in categories:
            abated_values = filter1_abated[cat]
            unabated_values = filter1_unabated[cat]
            reduction_rate = 1 - self.rate

            # Creating a new series with the adjusted values
            expected_abated_values = unabated_values.copy()
            # Apply a 30% reduction to all except the first row
            expected_abated_values = unabated_values* reduction_rate

            # Check that values are almost equal
            for actual, expected in zip(abated_values, expected_abated_values):
                self.assertAlmostEqual(actual, expected, places=2)



    def test_climate_abate_livestock(self):
        abated_emissions = self.fetcher.get_abated_climate_change_animal_emissions_aggregated(self.rate)
        unabated_emissions = self.fetcher.get_climate_change_animal_emissions_aggregated()
        
        filter0_abated = abated_emissions[abated_emissions.Scenarios == -1].copy(deep=True)
        filter0_unabated = unabated_emissions[unabated_emissions.Scenarios == -1].copy(deep=True)

        for emission_type in ["CH4", "N2O"]:
            abated_values = filter0_abated[emission_type]
            unabated_values = filter0_unabated[emission_type]

            # Check that values are almost equal
            for actual, expected in zip(abated_values, unabated_values):
                self.assertAlmostEqual(actual, expected, places=2)  # Adjust 'places' for desired precision


        filter1_abated = abated_emissions[abated_emissions.Scenarios != -1].copy(deep=True)
        filter1_unabated = unabated_emissions[unabated_emissions.Scenarios != -1].copy(deep=True)

        # Assert CH4 and N2O are 30% less (excluding row with index -1)
        for emission_type in ["CH4", "N2O"]:
            abated_values = filter1_abated[emission_type]
            unabated_values = filter1_unabated[emission_type]
            reduction_rate = 1 - self.rate

            # Creating a new series with the adjusted values
            expected_abated_values = unabated_values.copy()
            # Apply a 30% reduction to all except the first row
            expected_abated_values = unabated_values* reduction_rate

            # Check that values are almost equal
            for actual, expected in zip(abated_values, expected_abated_values):
                self.assertAlmostEqual(actual, expected, places=2)  # Adjust 'places' for desired precision

    def test_climate_change_total_abated(self):
        baseline_year = 2020
        target_year = 2050

        abated_emissions = self.fetcher.get_abated_climate_change_emissions_totals(baseline_year, target_year, self.rate)
        unabated_emissions = self.fetcher.get_climate_change_emission_totals()

        filter0_abated = abated_emissions[abated_emissions.Scenarios != -1].copy(deep=True)
        filter0_unabated = unabated_emissions[unabated_emissions.Scenarios != -1].copy(deep=True)

        for emission_type in ["CH4", "N2O", "CO2", "CO2e"]:
            abated_values = filter0_abated[emission_type]
            unabated_values = filter0_unabated[emission_type]

            # Check that values are almost equal
            for actual, expected in zip(abated_values, unabated_values):
                if emission_type == "CO2":
                    self.assertAlmostEqual(actual, expected, places=2)
                else:
                    #assert that abated emissions are less than unabated emissions
                    self.assertLess(actual, expected)


        
if __name__ == "__main__":
    unittest.main()
