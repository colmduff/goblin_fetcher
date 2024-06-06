"""
Time Series Module
==================
This module contains the TimeSeries class which is used to generate time series data for the different emission categories.

"""
import pandas as pd
import numpy as np
import itertools

class TimeSeries:
    """
    TimeSeries class is used to generate time series data for the different emission categories.
    """
    @staticmethod
    def get_land_use_emissions_time_series(baseline_year, target_year, scenario_df, landuse_df):
        """
        Get land use emissions time series.

        Parameters:
            baseline_year (int): The year for which calibration data is available.
            target_year (int): The year for which scenario ends.
            scenario_df (DataFrame): Data containing scenario information.
            landuse_df (DataFrame): Data containing land use information.

        Returns:
            DataFrame: A dataframe of total emissions for each scenario.
        """
        # year range
        years = list(range(baseline_year, target_year + 1))

        default_scenario_list = list(scenario_df["Scenarios"].unique())

        baseline_index = -1

        scenario_list_extended = [baseline_index]
        scenario_list_extended.extend(list(scenario_df["Scenarios"].unique()))

        gases = ["CH4", "N2O", "CO2", "CO2e"]
        instances = landuse_df.db_instance.unique()

        CH4_conversion = 28
        N2O_conversion = 265

        #empty land use dataframe
        # Create the MultiIndex
        land_multiindex = pd.MultiIndex.from_product([default_scenario_list, instances, gases], names=['scenario', 'instance','gas'])

        land_use_time_series = pd.DataFrame(index=land_multiindex, columns=years)

        # land use data 
        for (instance, sc, gas, year) in itertools.product(instances, default_scenario_list, gases, years):

            CO2_land_mask_2050 = (
                (landuse_df.Scenarios == sc)
                & (landuse_df.db_instance == instance)
                & ((landuse_df["land_use"] == "cropland")
                | (landuse_df["land_use"] == "grassland")
                | (landuse_df["land_use"] == "wetland"))
                & (landuse_df["year"] == target_year)
            )
                                    
            CO2_land_mask = (
                (landuse_df.Scenarios == baseline_index)
                & (landuse_df.db_instance == instance)
                & ((landuse_df["land_use"] == "cropland")
                | (landuse_df["land_use"] == "grassland")
                | (landuse_df["land_use"] == "wetland"))
                & (landuse_df["year"] == baseline_year)
            )

            default_mask = (
                (landuse_df.Scenarios == baseline_index)
                & (landuse_df.db_instance == instance)
                & (landuse_df["land_use"] == "total")
                & (landuse_df["year"] == baseline_year)
            )

            default_mask_2050 = (
                (landuse_df.Scenarios == baseline_index)
                & (landuse_df.db_instance == instance)
                & (landuse_df["land_use"] == "total")
                & (landuse_df["year"] == baseline_year)
            )
     
            if year == baseline_year:
                if gas == "CO2":
                    emission_value = landuse_df.loc[CO2_land_mask, gas].sum()
                else:
                    emission_value = landuse_df.loc[default_mask, gas].item()

            elif year == target_year:
                if gas == "CO2":
                    emission_value = landuse_df.loc[CO2_land_mask_2050, gas].sum()
                else:
                    emission_value = landuse_df.loc[default_mask_2050, gas].item()
               
            else:
                emission_value = np.nan


            land_use_time_series.loc[(sc, instance, gas), year] = emission_value

    
        # Apply linear interpolation to fill in NaN values along each row
        land_use_time_series = land_use_time_series.astype(float).interpolate(axis=1, method='linear', limit_direction='forward')
        
        # Calculate CO2e and add it to the DataFrame
        for year in years:
            for sc in default_scenario_list:
                for instance in instances:
                    CO2 = land_use_time_series.loc[(sc, instance, "CO2"), year]
                    CH4 = land_use_time_series.loc[(sc, instance, "CH4"), year] * CH4_conversion
                    N2O = land_use_time_series.loc[(sc, instance, "N2O"), year] * N2O_conversion
                    CO2e = CO2 + CH4 + N2O
                    land_use_time_series.loc[(sc, instance, "CO2e"), year] = CO2e

        return land_use_time_series
    

    @staticmethod
    def get_livestock_emissions_time_series(baseline_year, target_year, scenario_df, livestock_df):
        """
        Get livestock emissions time series.

        Parameters:
            baseline_year (int): The year for which calibration data is available.
            target_year (int): The year for which scenario ends.
            scenario_df (DataFrame): Data containing scenario information.
            livestock_df (DataFrame): Data containing livestock information.

        Returns:
            DataFrame: A dataframe of total emissions for each scenario.
        """
        # year range
        years = list(range(baseline_year, target_year + 1))

        default_scenario_list = list(scenario_df["Scenarios"].unique())

        baseline_index = -1

        scenario_list_extended = [baseline_index]
        scenario_list_extended.extend(list(scenario_df["Scenarios"].unique()))

        gases = ["CH4", "N2O", "CO2", "CO2e"]
        instances = livestock_df.db_instance.unique()

        CH4_conversion = 28
        N2O_conversion = 265


        #empty land use dataframe
        # Create the MultiIndex
        livestock_multiindex = pd.MultiIndex.from_product([default_scenario_list, instances, gases], names=['scenario', 'instance','gas'])

        livesetock_time_series = pd.DataFrame(index=livestock_multiindex, columns=years)

        for (instance, sc, gas, year) in itertools.product(instances, default_scenario_list, gases, years):
            if year == baseline_year:
                mask = ((livestock_df.Scenarios == baseline_index) & (livestock_df.db_instance == instance))
                emission_value = livestock_df.loc[mask, gas].item()
            elif year == target_year:
                mask = ((livestock_df.Scenarios == sc) & (livestock_df.db_instance == instance))
                emission_value = livestock_df.loc[mask, gas].item()
            else:
                emission_value = np.nan

            livesetock_time_series.loc[(sc, instance, gas), year] = emission_value

        # Apply linear interpolation to fill in NaN values along each row
        livesetock_time_series = livesetock_time_series.astype(float).interpolate(axis=1, method='linear', limit_direction='forward')

        # Calculate CO2e and add it to the DataFrame
        for (year, sc, instance) in itertools.product(years, default_scenario_list, instances):
            CO2 = livesetock_time_series.loc[(sc, instance, "CO2"), year]
            CH4 = livesetock_time_series.loc[(sc, instance, "CH4"), year] * CH4_conversion
            N2O = livesetock_time_series.loc[(sc, instance, "N2O"), year] * N2O_conversion
            CO2e = CO2 + CH4 + N2O
            livesetock_time_series.loc[(sc, instance, "CO2e"), year] = CO2e

        return livesetock_time_series
    

    @staticmethod
    def get_forest_carbon_time_series(baseline_year, target_year, scenario_df, forest_carbon_df):
        """
        Get forest carbon emissions time series.

        Parameters:
            baseline_year (int): The year for which calibration data is available.
            target_year (int): The year for which scenario ends.
            scenario_df (DataFrame): Data containing scenario information.
            forest_carbon_df (DataFrame): Data containing forest carbon information.

        Returns:
            DataFrame: A dataframe of total emissions for each scenario.
        """
        CO2e_conversion = 3.67
        t_to_kt = 1e-3

        # year range
        years = list(range(baseline_year, target_year + 1))

        default_scenario_list = list(scenario_df["Scenarios"].unique())

        gas = ["CO2e"]
        instances = forest_carbon_df.db_instance.unique()

        #empty land use dataframe
        # Create the MultiIndex
        forest_multiindex = pd.MultiIndex.from_product([default_scenario_list, instances, gas], names=['scenario', 'instance','gas'])

        forest_time_series = pd.DataFrame(index=forest_multiindex, columns=years)

        for (instance, sc, year) in itertools.product(instances, default_scenario_list, years):
            mask = ((forest_carbon_df.Scenario == sc) & (forest_carbon_df.db_instance == instance) & (forest_carbon_df["Year"] == year))

            if mask.any():
                emission_value = forest_carbon_df.loc[mask, "Total Ecosystem"].item() * CO2e_conversion * t_to_kt
            else:
                emission_value = np.nan

            forest_time_series.loc[(sc, instance, gas), year] = emission_value

        return forest_time_series
    

    @staticmethod
    def total_climate_change_emissions_time_series(baseline_year, target_year, scenario_df, livestock_df, landuse_df, forest_carbon_df):
        """
        Get total climate change emissions time series.

        Parameters:
            baseline_year (int): The year for which calibration data is available.
            target_year (int): The year for which scenario ends.
            scenario_df (DataFrame): Data containing scenario information.
            livestock_df (DataFrame): Data containing livestock information.
            landuse_df (DataFrame): Data containing land use information.
            forest_carbon_df (DataFrame): Data containing forest carbon information.

        Returns:
            DataFrame: A dataframe of total emissions for each scenario.
        """
        land_use_time_series = TimeSeries.get_land_use_emissions_time_series(baseline_year, target_year, scenario_df, landuse_df)
        livestock_time_series = TimeSeries.get_livestock_emissions_time_series(baseline_year, target_year, scenario_df, livestock_df)
        forest_time_series = TimeSeries.get_forest_carbon_time_series(baseline_year, target_year, scenario_df, forest_carbon_df)

        land_uses = ["Agriculture", "Other Land Use", "Forestry", "Total"]
        gases = ["CH4", "N2O", "CO2", "CO2e"]
        default_scenario_list = list(scenario_df["Scenarios"].unique())
        instances = landuse_df.db_instance.unique()

        years = list(range(baseline_year, target_year + 1))

        # Create the MultiIndex
        total_multiindex = pd.MultiIndex.from_product([default_scenario_list, instances, land_uses, gases], names=['scenario', 'instance', 'land_use', 'gas'])

        total_time_series = pd.DataFrame(index=total_multiindex, columns=years)

        for (landuse, instance, sc, gas, year) in itertools.product(land_uses, instances, default_scenario_list, gases, years):
            if landuse == "Agriculture":
                land_use_mask = (livestock_time_series.index.get_level_values("scenario") == sc) & (livestock_time_series.index.get_level_values("instance") == instance) & (livestock_time_series.index.get_level_values("gas") == gas)
                emission_value = livestock_time_series.loc[land_use_mask, year].item()
            elif landuse == "Other Land Use":
                land_use_mask = (land_use_time_series.index.get_level_values("scenario") == sc) & (land_use_time_series.index.get_level_values("instance") == instance) & (land_use_time_series.index.get_level_values("gas") == gas)
                emission_value = land_use_time_series.loc[land_use_mask, year].item()
            elif landuse == "Forestry":
                if gas == "CO2e" or gas == "CO2":
                    land_use_mask = (forest_time_series.index.get_level_values("scenario") == sc) & (forest_time_series.index.get_level_values("instance") == instance) & (forest_time_series.index.get_level_values("gas") == "CO2e")
                    emission_value = forest_time_series.loc[land_use_mask, year].item()
                else:
                    emission_value = 0
            else:
                emission_value = np.nan

            total_time_series.loc[(sc, instance, landuse, gas), year] = emission_value


        # Calculate totals after filling the other categories
        for (instance, sc, gas, year) in itertools.product(instances, default_scenario_list, gases, years):
            total = 0
            for landuse in ['Agriculture', 'Other Land Use', 'Forestry']:
                total += total_time_series.loc[(sc, instance, landuse, gas), year]
            total_time_series.loc[(sc, instance, 'Total', gas), year] = total

        return total_time_series
        

