"""
============================================
Author: Julia Brittes Tuthill

IFEWs Data Fetch
This code fetches IFEWs necessary data from USDA and other sources.

Variables*:
x1: corng_y = Corn Grain Yield (bu/ac)
x2: soy_y = Soybeans Yield (bu/ac)

x3: beef = Beef Cattle Inventory (heads)  
x4: steers = Cattle on Feed (heads)
x6: bulls = adult male cattle (heads)
x5: fin_cattle = Finishing Cattle (heads)
x7: milk = Milk Cattle Inventory (heads)  
x8: dairy_150 = Young Female Dairy Cattle less than 1 year old (heads)
x9: dairy_440 = Young Female Dairy Cattle between 1 and 2 years old (heads)
x10: hogs_boars = adult male Hogs (heads)
x11: hogs_sow = adult female Hogs (heads)
x12: hogs_fin = Hogs fattening (finish) (heads)

*All yearly data.

Time Scale = 1968** till Current Year-1
Spatial Scale = Iowa Counties

**Why 1968: animal data constrained 
============================================
"""
import numpy as np
import pandas as pd



# function to calculate ManureN_kg_ha for each row
def calculate_manure_n(row):
    hogs_sow = row['hogs_sow']
    hogs_boars = row['hogs_boars']
    hogs_fin = row['hogs_fin']
    milk_cows = row['milk']
    beef_cows = row['beef']
    milk_cows_150 = row['dairy_150']
    milk_cows_440 = row['dairy_440']
    beef_bulls = row['bulls']
    calf = row['steers']
    cattle_fin = row['fin_cattle']
    
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    # from Gronberg et al. (2017) and looking into nloss from Andersen, D. S., & Pepple, L. M. (2017) 
    manure_n = (hogs_sow * 0.036 * 365 +
                hogs_boars * 0.022 * 365 +
                hogs_fin * 0.028 * 365 +
                milk_cows * 0.2 * 365 +
                beef_cows * 0.029 * 365 +
                milk_cows_150 * 0.031 * 365 +
                milk_cows_440 * 0.060 * 365 +
                beef_bulls * 0.029 * 365 +
                calf * 0.019 * 365 +
                cattle_fin * 0.089 * 365) / (0.404686 * (soybeans_acres + corn_acres))
        
    return round(manure_n, 1)

# function for calculating fixation n
# soybeans bushels consider 1 metric ton/hectare = 14.87 (15) bushels/acre from https://www.extension.iastate.edu/agdm/wholefarm/pdf/c6-80.pdf
def calculate_fix_n(row):
    soybeans_yield = row['soy_y']
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    fix_n = ((soybeans_yield/15)*81.1-98.5)*(soybeans_acres/(soybeans_acres+corn_acres))
    
    return round(fix_n, 1)

# function for calculation grain nitrogen
def calculate_grain_n(row):
    soybeans_yield = row['soy_y']
    corn_yield = row['corng_y']
    soybeans_acres_h = row['soy_ha']
    corn_acres_h = row['corng_ha']
    
    grain_n = ((soybeans_yield*67.25)*(6.4/100)*(soybeans_acres_h*0.404686)+(corn_yield*62.77)*(1.18/100)*corn_acres_h*0.404686)/(0.404686*(soybeans_acres_h+corn_acres_h))
    
    return round(grain_n, 1)

# function for calculating nitrogen surplus 
def calculate_ns(row):
    commercial = row['CN']
    manure = row['MN']
    grain = row['GN']
    fix = row['FN']
    
    ns = commercial + manure + fix - grain
    
    return round(ns, 1)

# ---------------------- Merge USDA and Nrate data ----------------------------------------
"""
This section calculates the surplus based on Vishal's work:
The below modeling addresses the agricutlure and water (nitrogen surplus as a water
quality indicador) of the IFEWs.

Ns = CN + MN + FN - GN

Output: 
Ns = N surplus [kg/ha]
CN = commercial nitrogen applied in planted corn crop (No fertilizer to soybean in Iowa)[kg/ha]
MN = nitrogen generated from manure[kg/ha]
FN = nitrogen fixed by soybean crop[kg/ha]
GN = nitrogen present in harvested grain [kg/ha]
"""

# Load a data file
IFEWs = pd.read_csv('IFEWs_merged_data.csv')

# Convert the specified columns to numeric values, setting any non-numeric entries to NaN
IFEWs["beef"] = pd.to_numeric(IFEWs["beef"], errors='coerce')
IFEWs["milk"] = pd.to_numeric(IFEWs["milk"], errors='coerce')
IFEWs["steers"] = pd.to_numeric(IFEWs["steers"], errors='coerce')
IFEWs["bulls"] = pd.to_numeric(IFEWs["bulls"], errors='coerce')
IFEWs["dairy_150"] = pd.to_numeric(IFEWs["dairy_150"], errors='coerce')
IFEWs["dairy_440"] = pd.to_numeric(IFEWs["dairy_440"], errors='coerce')
IFEWs["fin_cattle"] = pd.to_numeric(IFEWs["fin_cattle"], errors='coerce')
IFEWs["hogs_fin"] = pd.to_numeric(IFEWs["hogs_fin"], errors='coerce')
IFEWs["hogs_sow"] = pd.to_numeric(IFEWs["hogs_sow"], errors='coerce')
IFEWs["hogs_boars"] = pd.to_numeric(IFEWs["hogs_boars"], errors='coerce')
IFEWs["corng_y"] = pd.to_numeric(IFEWs["corng_y"], errors='coerce')
IFEWs["corng_pa"] = pd.to_numeric(IFEWs["corng_pa"], errors='coerce')
IFEWs["corng_ha"] = pd.to_numeric(IFEWs["corng_ha"], errors='coerce')
IFEWs["soy_y"] = pd.to_numeric(IFEWs["soy_y"], errors='coerce')
IFEWs["soy_pa"] = pd.to_numeric(IFEWs["soy_pa"], errors='coerce')
IFEWs["soy_ha"] = pd.to_numeric(IFEWs["soy_ha"], errors='coerce')
IFEWs["CN_lb/ac"] = pd.to_numeric(IFEWs["CN_lb/ac"], errors='coerce')

# Apply the functionS to create the upper level inputs (CN, MN, FN, GN) and final output (NS)

IFEWs['CN'] = round(IFEWs["CN_lb/ac"] * 1.121, 1)
IFEWs['MN'] = IFEWs.apply(calculate_manure_n, axis=1)
IFEWs['FN'] = IFEWs.apply(calculate_fix_n, axis=1)
IFEWs['GN'] = IFEWs.apply(calculate_grain_n, axis=1)
IFEWs['NS'] = IFEWs.apply(calculate_ns, axis=1)

IFEWs = IFEWs.loc[:, ~IFEWs.columns.str.contains('^Unnamed')]

IFEWs.to_csv('IFEW_with_upper_input.csv', index=False)