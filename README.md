# Iowa Food-Energy-Water (IFEW) System

## Overview

The Iowa Food-Energy-Water (IFEW) system is a model designed to calculate the **nitrogen surplus (NS)** at the county level in Iowa. The NS is composed of several key variables:

- **Manure Nitrogen (MN)**
- **Commercial Nitrogen (CN)**
- **Grain Nitrogen (GN)**
- **Fixation Nitrogen (FN)**

The variables FN, GN, and MN are derived from lower-level variables sourced from the [USDA National Agricultural Statistics Service](https://www.nass.usda.gov/). These lower-level variables may contribute to multiple upper-level input variables. The CN data is obtained from a county-level dataset.

## Getting Started

### Prerequisites

- Python installed on your system.
- Necessary libraries installed.

### Installation

1. **Download the Main Model Script**

   - Obtain the `IFEWs.py` file, which is the core model script responsible for aggregating inputs from lower-level data to compute the NS at the county level.

2. **Prepare the Data**

   - **Data Folder Contents**:
     - `Agriculture_Data_county_usda.csv`
     - `Animal_Agriculture_data_county_data.csv`
     - `CN_from_GIS_and_Cao.csv`
   - These files are merged into a single dataset named `IFEWs_merged_data.csv` for convenience.
   - Ensure that `IFEWs_merged_data.csv` is placed in the same directory as `IFEWs.py`.

### Running the Model

1. **Execute the Script**

   - Run the Python script using the command:
     ```bash
     python IFEWs.py
     ```

2. **Output**

   - After running the script, an output file named `IFEWs_output.csv` will be generated.
   - This file contains the aggregated inputs and the calculated NS for each county along with data on lower-level variables.

## Visualization

### SimDec Visualization

- **Step 1**: Visit the [SimDec App](https://simdec.io/simdec_app).
- **Step 2**: Upload the `IFEWs_output.csv` file.
- **Step 3**: Select "Output" and "Input" from the labels in the data file.
- **Result**: Generate plots identical to those used in the analysis.

### Sankey Diagram

- **Step 1**: Go to [SankeyMATIC](https://sankeymatic.com/build/).
- **Step 2**: Manually input the flow thickness values based on data.
- **Result**: Create a Sankey diagram to visualize the flow of nitrogen components.


## Citation

Jeong, T., Kozlova, M., Leifsson, L., & Yeomans, J. (Submitted). *Simulation Decomposition Analysis of the Iowa Food-Water-Energy System*. Environmental Modelling & Software.

