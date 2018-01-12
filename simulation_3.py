from tqdm import tqdm
import pathos.pools as pp
import pandas as pd
import numpy as np
import simulator

county_fips = []
for county, fips in simulator.PA_COUNTIES.items():
    county_fips.append(fips)

p = pp.ProcessPool(4)
mcs = simulator.MonteCarlo()
mcs_df = pd.DataFrame()

pbar = tqdm(total=2)
for run in range(0,2):
    results = p.map(mcs.run, county_fips)
    results_df = pd.DataFrame(results, columns=['county_fips', str(run)])
    results_df = results_df.set_index('county_fips')
    mcs_df = pd.concat([mcs_df, results_df], axis=1)
    mcs_df.to_csv('snap_simulation.csv')
    pbar.update(1)
pbar.close()
