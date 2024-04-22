"""
Database Manager
================

This module contains the DataManager class, which is responsible for managing the database
for the GOBLIN LCA framework. The DataManager class is responsible for retrieving data from the database.
"""
import sqlalchemy as sqa
import pandas as pd
import os
import re


class DataManager:
    """
    Manages the GOBLIN LCA database.

    This class is responsible for managing the database for the GOBLIN LCA framework. It is responsible for creating,
    clearing, and saving data to the database. It also retrieves data from the database.

    Attributes
    ----------
    database_dir : str
        The directory where the database is stored.

    engine : sqlalchemy.engine.base.Engine

    Methods
    -------
    data_engine_creater()
        Creates the database engine.

    create_or_clear_database()
        Creates or clears the database.

    prepare_scenarios_column(df)
        Ensures there is a column named 'Scenarios'.

    get_goblin_results_output_datatable(table, index_col=None)
        Retrieves a DataFrame from the database.
 
    """

    def __init__(self, external_database_paths):
        """
        Initializes the DataManager.

        Parameters
        ----------
        external_database_path : list of str,
            list of paths to the external databases
        """

        self.database_paths = external_database_paths


    def data_engine_creator(self, path):
        """
        Checks if the database file exists and creates the engine if it does.
        Informs the user if the database file does not exist.

        Returns
        -------
        sqlalchemy.engine.base.Engine or None
            The database engine if the file exists, None otherwise.
        """
        database_dir = os.path.dirname(path)
        database_name = os.path.basename(path)
        try:
            # Construct the full path to the database file
            database_path = os.path.abspath(os.path.join(database_dir, database_name))
            
            # Check if the database file exists
            if not os.path.isfile(database_path):
                raise FileNotFoundError(f"Database file '{database_path}' not found.")

            # Create the engine URL and the engine itself
            engine_url = f"sqlite:///{database_path}"
            engine = sqa.create_engine(engine_url)
            return engine
        except Exception as e:
            # Inform the user of the problem
            print(f"An error occurred: {e}")
            return None


    def prepare_scenarios_column(self, df):
        """
        Ensures there is a column named 'Scenarios'. If 'scenario' or 'scenarios' exist,
        it renames them. If 'farm_id' exists, uses it for 'Scenarios'; otherwise, it uses the DataFrame index.
        """
        if 'Scenarios' not in df.columns:
            if 'scenario' in df.columns:
                df.rename(columns={'scenario': 'Scenarios'}, inplace=True)
            elif 'scenarios' in df.columns:
                df.rename(columns={'scenarios': 'Scenarios'}, inplace=True)
            else:
                # Check for 'farm_id' to use as 'Scenarios' or default to index
                if 'farm_id' in df.columns:
                    df['Scenarios'] = df['farm_id']
                else:
                    df['Scenarios'] = df.index
        
        return df


    def get_goblin_results_output_datatable(self, table, index_col=None):
        """
        Retrieves a DataFrame from the database.

        This method retrieves a DataFrame from the database.

        Parameters
        ----------
        table : str
            The name of the table to retrieve the DataFrame from.

        index_col : str, optional
            The column to use as the index. Defaults to None.

        Returns
        -------
        pandas.DataFrame
            The DataFrame retrieved from the database.
        """
        concatenated_data = pd.DataFrame()
        for path in self.database_paths:
            self.engine = self.data_engine_creator(path)
            if self.engine is not None:
                
                dataframe = pd.read_sql("SELECT * FROM '%s'" % table, self.engine, index_col)
                dataframe= self.prepare_scenarios_column(dataframe)
                dataframe["db_instance"] = re.sub(r'\..*$', '', os.path.basename(path)) 
                concatenated_data = pd.concat([concatenated_data, dataframe], ignore_index=True)
                self.engine.dispose()

        return concatenated_data
