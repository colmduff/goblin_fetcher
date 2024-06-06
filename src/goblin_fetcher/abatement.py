"""
Abatement Module 
================

This module contains the Abate class which is used to abate emissions from the livestock and land use sectors.
"""
import pandas as pd

class Abate:
    """
    This class contains methods for abating emissions from the livestock and land use sectors.
    """

    @staticmethod
    def climate_abate_livestock(df, rate, CH4=None, N2O=None):
        """
        Abates emissions from the livestock sector.

        Parameters:
            df (DataFrame): A DataFrame containing emissions data.
            rate (float): The rate at which emissions should be abated.
            CH4 (float): The GWP for CH4.
            N2O (float): The GWP for N2O.

        Returns:
            DataFrame: A DataFrame with abated emissions.
        """
        CH4 = 28 if CH4 is None else CH4
        N2O = 265 if N2O is None else N2O

        # Filter out rows with index -1 before modification
        df_filtered = df[df.Scenarios != -1].copy(deep=True)

        df_filtered["CH4"] -= df_filtered["CH4"] * rate
        df_filtered["N2O"] -= df_filtered["N2O"] * rate
        df_filtered["CO2e"] = df_filtered["CO2"] + (df_filtered["CH4"] * CH4) + (df_filtered["N2O"] * N2O)

        # Update the original dataframe with the modifications from the filtered one
        df.update(df_filtered)

        return df
    
    @staticmethod
    def eutrophication_air_quality_abate_livestock(df, rate):
        """
        Abates emissions from the livestock sector.

        Parameters:
            df (DataFrame): A DataFrame containing emissions data.
            rate (float): The rate at which emissions should be abated.
        """
        df_filtered = df[df.Scenarios != -1].copy(deep=True)

        df_filtered["manure_management"] = df_filtered["manure_management"] - (df_filtered["manure_management"] * rate)
        df_filtered["soils"] = df_filtered["soils"] - (df_filtered["soils"] * rate)
        df_filtered["Total"] = df_filtered["manure_management"] + df_filtered["soils"]

        df.update(df_filtered)

        return df

    @staticmethod
    def climate_total_abated(baseline_year, target_year, scenario_df, livestock_df, landcover_df, rate, CH4=None, N2O=None):
        """
        Abates emissions from the livestock and land use sectors.

        Parameters:
            baseline_year (int): The baseline year.
            target_year (int): The target year.
            scenario_df (DataFrame): A DataFrame containing scenario data.
            livestock_df (DataFrame): A DataFrame containing livestock data.
            landcover_df (DataFrame): A DataFrame containing land cover data.
            rate (float): The rate at which emissions should be abated.
            CH4 (float): The GWP for CH4.
            N2O (float): The GWP for N2O.
        """
        baseline_index = -1
        climate_change_livestock = Abate.climate_abate_livestock(livestock_df, rate, CH4, N2O)

        total_climate_change_emissions_dataframe = climate_change_livestock.copy(deep=True)
        land_use_dataframe = landcover_df.copy(deep=True)

        scenario_list = [baseline_index]
        scenario_list.extend(list(scenario_df["Scenarios"].unique()))

        gases = ["CH4", "N2O", "CO2", "CO2e"]

        # Initialize a list to collect DataFrame rows
        results = []

        for instance in total_climate_change_emissions_dataframe.db_instance.unique():
            for sc in scenario_list: 
                
                emissions_mask = (
                    (total_climate_change_emissions_dataframe.Scenarios == sc) 
                    & (total_climate_change_emissions_dataframe.db_instance == instance)
                )

                if sc >= 0:
                    land_mask = (
                        (land_use_dataframe.Scenarios == sc)
                        & (land_use_dataframe.db_instance == instance)
                        & (land_use_dataframe["land_use"] == "total")
                        & (land_use_dataframe["year"] == target_year)
                    )
                else:
                    land_mask = (
                        (land_use_dataframe.Scenarios == sc)
                        & (land_use_dataframe.db_instance == instance)
                        & (land_use_dataframe["land_use"] == "total")
                        & (land_use_dataframe["year"] == baseline_year)
                    )

                if not emissions_mask.any() or not land_mask.any():
                    print("Warning: No data matched for masks.")
                    continue

                    # Collect rows to append later
                result_row = total_climate_change_emissions_dataframe.loc[emissions_mask].copy()

                for gas in gases:

                    emission_value = total_climate_change_emissions_dataframe.loc[
                        emissions_mask, gas
                    ].item() + land_use_dataframe.loc[land_mask, gas].item()


                    result_row[gas] = emission_value

                results.append(result_row)

        # Concatenate all collected rows into a single DataFrame
        result_df = pd.concat(results, ignore_index=True)
        return result_df


