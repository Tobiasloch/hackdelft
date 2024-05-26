# Magazine Delivery Route Optimization

This project is designed to calculate the optimal routes for vehicles delivering magazines. The program uses various algorithms to determine the most efficient paths, considering factors such as vehicle capacity, delivery locations, and time constraints. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Input File Format](#input-file-format)
- [Arguments](#arguments)
- [Output](#output)
- [Project Structure](#project-structure)

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the program, execute the `main.py` script with the necessary arguments:

```bash
python main.py input_file.json [--output_folder OUTPUT_FOLDER] [--k K] [--greedy] [--exact] [--dive] [--pricing_strategy PRICING_STRATEGY] [--time_limit TIME_LIMIT] [--use_pickled_graph] [--pickledump_new_graph] [--pickle_file_name PICKLE_FILE_NAME]
```

## Input File Format

The input file should be in JSON format and contain the following keys:

- `addressFile`: Path to the file containing the addresses (one per line).
- `vehicles`: A list of vehicles with their properties.
- `hubIndex`: (Optional) Index of the hub address in the address file.

Example `input_file.json`:
```json
{
    "addressFile": "addresses.txt",
    "vehicles": [
        {"name": "Bike1", "type": "bike", "capacity": 5},
        {"name": "Van1", "type": "car", "capacity": 50}
    ],
    "hubIndex": 0
}
```

## Arguments

- `input_file`: Path to the input file (JSON format).
- `--output_folder`: Folder to save the route HTML files. Default is "out".
- `--k`: Number of nearest neighbors to consider when building the k-NN graph. Default is 4.
- `--greedy`: Use the greedy algorithm to solve the problem.
- `--exact`: Use the exact algorithm to solve the problem.
- `--dive`: Use the diving strategy in the solver.
- `--pricing_strategy`: Pricing strategy to use when solving the problem. Default is "Hyper".
- `--time_limit`: Time limit (in seconds) for the solver. Default is 10.
- `--use_pickled_graph`: Use the pickled graph if available.
- `--pickledump_new_graph`: Dump the new graph to a pickle file.
- `--pickle_file_name`: Name of the pickle file to use. Default is "graph.pkl".

## Output

The program generates HTML files for each route, saved in the specified output folder. The HTML files visualize the routes using OpenStreetMap.

## Project Structure

- `main.py`: The main script to run the program.
- `src/vehicle.py`: Contains the `Vehicle` class definition.
- `src/graph.py`: Contains the `generateGraph` function to create the graph from addresses.
- `src/solver.py`: Contains the `solve` function to determine the optimal routes.
- `src/render_map.py`: Contains the `render_map` function to generate HTML files for the routes.

## Example

To run the program with an example input file:
```bash
python main.py example_input.json --output_folder results --k 5 --greedy --pricing_strategy Simple --time_limit 20
```

This command will process the `example_input.json` file, calculate the routes, and save the HTML files in the `results` folder.

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

