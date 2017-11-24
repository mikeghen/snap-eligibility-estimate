from census import Census
from us import states
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import simulator

# Run Monte Carlo Simulation for Households' Sizes for Philadelphia
p = simulator.get_household_sizes_pdf(42, 101)

household_size_sim_data = [0,0,0,0,0,0,0]
for i in range(0,24358):
    household_size = np.random.choice(np.arange(0, 7), p=p)
    household_size_sim_data[household_size] += 1
pprint(household_size_sim_data)

# household_size_df = pd.DataFrame.from_records(household_size_sim_data, columns=['Households'])
# print(household_size_df)
# household_size_df.plot(kind='bar',subplots=True)

# Run Monte Carlo Simulation for Incomes for Philadelphia
p = simulator.get_incomes_pdf(42, 101)
pprint(p)
income_sim_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,24358):
    income = np.random.choice(np.arange(0, 16), p=p)
    income_sim_data[income] += 1
pprint(income_sim_data)

# income_df = pd.DataFrame.from_records(income_sim_data, columns=['Households'])
# print(income_df)
# income_df.plot(kind='bar',subplots=True)
# plt.show()
