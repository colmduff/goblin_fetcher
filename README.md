# goblin_fetcher

Data fetcher for externally specified GOBLIN database

## Installation

```bash
pip install "goblin_fetcher@git+https://github.com/colmduff/goblin_fetcher.git@main" 

```

## Usage

Allows for the retrieval of goblin data tables from externally specified data base. The tool allows users who have generated databaseses 
from multiple instances of the GOBLIN class to specify those databases as external inputs rather than using the GOBLIN class itself, which has the database
stored internally. 

The input is a list of paths to the databases. The returned data will be a concatenation of all the table outputs from the databases.

```python
from goblin_fetcher.goblin_fetcher import DataFetcher
import os 

def main():

    data_path ="./data/"
    path = [os.path.join("./data", "instance_0.db"), os.path.join("./data", "instance_1.db")]

    fetch = DataFetcher(path)

    print(fetch.get_air_quality_animal_emissions_by_category())



if __name__ == "__main__":  
    main()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`goblin_fetcher` was created by Colm Duffy. It is licensed under the terms of the MIT license.

## Credits

`goblin_fetcher` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
