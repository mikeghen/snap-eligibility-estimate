from census import Census
from us import states
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import simulator
household_size_df = pd.DataFrame()
income_df = pd.DataFrame()
households = [] # Parallel to incomes
incomes = []    # Parallel to households
total_households = 0
for county, county_fips in simulator.PA_COUNTIES.items():
    # Run Monte Carlo Simulation for Households' Sizes for Philadelphia
    p, num_households = simulator.get_household_sizes_pdf(42, county_fips)
    total_households += num_households
    pprint("Simulating {0} households for {1} County".format(num_households,county))

    household_size_sim_data = [0,0,0,0,0,0,0]
    for i in range(0,num_households):
        household_size = np.random.choice(np.arange(0, 7), p=p)
        households.append(household_size)
        household_size_sim_data[household_size] += 1

    household_size_df = pd.concat([household_size_df, pd.DataFrame({county:household_size_sim_data})], axis=1)

    # Run Monte Carlo Simulation for Incomes for Philadelphia
    p, n = simulator.get_incomes_pdf(42, county_fips)
    pprint("Simulating {0} household incomes for {1} County".format(num_households,county))

    income_sim_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0,num_households):
        income = np.random.choice(np.arange(0, 16), p=p)
        incomes.append(incomes)
        income_sim_data[income] += 1

    income_df = pd.concat([income_df, pd.DataFrame({county:income_sim_data})], axis=1)
print("Simulated {0} households".format(total_households))
# household_size_df.plot(kind='bar',subplots=True, title=county)
# income_df.plot(kind='bar',subplots=True, title=county)
# plt.show()
