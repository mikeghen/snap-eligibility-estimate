from census import Census
from us import states
from pprint import pprint
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import simulator

"""
Household Size Adjusted Income PDFs
"""



household_size_df = pd.DataFrame()
income_df = pd.DataFrame()
households = [] # Parallel to incomes
incomes = []    # Parallel to households
total_households = 0
for county, county_fips in simulator.PA_COUNTIES.items():
    # Calculate Household Size Incomes pdfs
    household_size_income_pdfs = {}

    for household_size in range(0,7):
        pdf = simulator.get_household_size_incomes_pdf(household_size+1, 42, county_fips)
        household_size_income_pdfs[household_size] = pdf

    # Run Monte Carlo Simulation for Households' Sizes for Philadelphia
    p, num_households = simulator.get_household_sizes_pdf(42, county_fips)
    total_households += num_households
    pprint("Simulating {0} households for {1} County".format(num_households,county))

    household_size_sim_data = [0,0,0,0,0,0,0]
    pbar = tqdm(total=num_households*2)
    for i in range(0,num_households):
        household_size = np.random.choice(np.arange(0, 7), p=p)
        households.append(household_size)
        household_size_sim_data[household_size] += 1
        pbar.update(1)

    household_size_df = pd.concat([household_size_df, pd.DataFrame({county:household_size_sim_data})], axis=1)

    # Run Monte Carlo Simulation for Incomes for Philadelphia
    income_sim_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0,num_households):
        # Calc p based on household size
        p = household_size_income_pdfs[households[i]]
        income = np.random.choice(np.arange(0, 16), p=p)
        incomes.append(income)
        income_sim_data[income] += 1
        pbar.update(1)

    pbar.close()
    income_df = pd.concat([income_df, pd.DataFrame({county:income_sim_data})], axis=1)
print("Simulated {0} households".format(total_households))
# household_size_df.plot(kind='bar',subplots=True, title=county)
# income_df.plot(kind='bar',subplots=True, title=county)

"""
Zip incomes and household sizes together in a DataFrame
"""
households_df = pd.DataFrame({'size':households, 'income':incomes})
households_df['income'] = households_df['income'].apply(simulator.get_income_from_bucket)
households_df['snap_eligible'] = households_df.apply(simulator.is_snap_eligible, axis=1)
households_df.head(100).to_csv('data.csv')
print("SNAP ELIGIBLE:", households_df['snap_eligible'].sum())
