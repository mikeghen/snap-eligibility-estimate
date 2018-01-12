from census import Census
from us import states
from pprint import pprint
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import simulator

for county, county_fips in simulator.PA_COUNTIES.items():
    # Run Monte Carlo Simulation for Households' Sizes for Philadelphia
    p, num_households = simulator.get_household_sizes_pdf(42, county_fips)
    total_households = num_households
    household_size_df = pd.DataFrame()
    income_df = pd.DataFrame()
    households = [] # Parallel to incomes
    incomes = []    # Parallel to households
    print("Simulating {0} households for {1} County".format(num_households,county))

    household_size_sim_data = [0,0,0,0,0,0,0]
    pbar = tqdm(total=num_households*2)
    for i in range(0,num_households):
        household_size = np.random.choice(np.arange(0, 7), p=p)
        households.append(household_size)
        household_size_sim_data[household_size] += 1
        pbar.update(1)

    household_size_df = pd.concat([household_size_df, pd.DataFrame({county:household_size_sim_data})], axis=1)

    # Run Monte Carlo Simulation for Incomes for Philadelphia
    p, n = simulator.get_incomes_pdf(42, county_fips)

    income_sim_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0,num_households):
        income = np.random.choice(np.arange(0, 16), p=p)
        incomes.append(income)
        income_sim_data[income] += 1
        pbar.update(1)

    pbar.close()
    income_df = pd.concat([income_df, pd.DataFrame({county:income_sim_data})], axis=1)

    """
    Zip incomes and household sizes together in a DataFrame, compute eligibilty
    output the results.
    """
    households_df = pd.DataFrame({'size':households, 'income':incomes})
    households_df['income'] = households_df['income'].apply(simulator.get_income_from_bucket)
    households_df['snap_eligible'] = households_df.apply(simulator.is_snap_eligible, axis=1)
    households_df.head(100).to_csv('data.csv')
    individuals = households_df['size'].sum()
    snap_eligible = households_df['snap_eligible'].sum()
    print("Simulated {0} households, found {1} of {2} individuals eligible in {3}".format(total_households,snap_eligible,individuals,county))
