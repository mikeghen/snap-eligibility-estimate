import pandas as pd
import matplotlib.pyplot as plt

sim_df = pd.DataFrame.from_csv('data/snap_simulation_no_elderly.csv')
actual_df = pd.DataFrame.from_csv('data/SNAP_Individuals_And_Dollars_2017.csv', header=0)
actual_df = actual_df.reset_index().set_index('FIPS County Code')[['SNAP Individuals']]

print(actual_df)

actual_df.loc[[127,125],:].plot(kind='bar')
plt.show()
sim_df.T[[127,125]].boxplot()
plt.show()
