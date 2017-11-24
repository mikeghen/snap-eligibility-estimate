from census import Census
from us import states
import pandas as pd
import numpy as np

C = Census("79d4f20c2a84412e07d717af5d13929cf7aa3ce5")

HOUSEHOLD_SIZES = [1, 2, 3, 4, 5, 6, 7]

INCOMES = [ '< $10k', '$10k - $14.9k', '$15k - $19.9k', '$20k - $24.9k',
  '$25k - $29.9k', '$30k - $34.9k', '$35k - $39.9k', '$40k - $44.9k',
  '$45k - $49.9k', '$50k - $59.9k', '$60k - $74.9k', '$75k - $99.9k',
  '$100k - $124.9k', '$125k - $149.9k', '$150k - $199.9k', '$200k +' ]

def get_household_sizes_pdf(state_code, county_code):
    """
    Returns a probability density function for households sizes.
    Returns PDF as a list of decimals parallel to HOUSEHOLD_SIZES
    """
    acs5_household_names_labels = {
        'B11016_001E': 'Total',
        'B11016_003E': '2-person',
        'B11016_004E': '3-person',
        'B11016_005E': '4-person',
        'B11016_006E': '5-person',
        'B11016_007E': '6-person',
        'B11016_008E': '7+ person'
    }

    households_fields = [name for name, label in acs5_household_names_labels.items()]
    household_results = C.acs5.state_county(households_fields, state_code, county_code)
    del household_results[0]['state']
    del household_results[0]['county']
    household_size_dict = {}

    total_households = household_results[0]['B11016_001E']
    total_non_single_households = 0
    for name, value in household_results[0].items():
        label = acs5_household_names_labels[name]
        if label != 'Total':
            total_non_single_households += value
            household_size_dict[label] = value

    # NOTE: Calculate 1-peron households by subtracting Census data points
    household_size_dict['1-person'] = total_households - total_non_single_households

    household_size_df = pd.DataFrame.from_dict(household_size_dict,orient='index')\
                                    .sort_index()
    household_size_df.columns = pd.Index(['Households'])

    # Calculate PDF
    household_size_df['Dist'] = household_size_df['Households'] / household_size_df['Households'].sum()
    return list(household_size_df['Dist'])


def get_incomes_pdf(state_code, county_code, household_size=None):
    """
    Returns a probability density function for incomes. Parallel to INCOMES

    TODO: Adjust PDF based on household size.
    """
    acs5_incomes_names_labels = {
        'B19101_001E': 'Total',
        'B19101_002E': '< $10k',
        'B19101_003E': '$10k - $14.9k',
        'B19101_004E': '$15k - $19.9k',
        'B19101_005E': '$20k - $24.9k',
        'B19101_006E': '$25k - $29.9k',
        'B19101_007E': '$30k - $34.9k',
        'B19101_008E': '$35k - $39.9k',
        'B19101_009E': '$40k - $44.9k',
        'B19101_010E': '$45k - $49.9k',
        'B19101_011E': '$50k - $59.9k',
        'B19101_012E': '$60k - $74.9k',
        'B19101_013E': '$75k - $99.9k',
        'B19101_014E': '$100k - $124.9k',
        'B19101_015E': '$125k - $149.9k',
        'B19101_016E': '$150k - $199.9k',
        'B19101_017E': '$200k +'
    }

    income_fields = [name for name, label in acs5_incomes_names_labels.items()]
    income_results = C.acs5.state_county(income_fields, state_code, county_code)

    del income_results[0]['state'] # we know what State we're working with
    del income_results[0]['county'] # we know what State we're working with

    # Map to a dictionary with labels for dataframe plotting
    incomes_dict = {}
    for name, value in income_results[0].items():
        label = acs5_incomes_names_labels[name]
        if label != 'Total':
            incomes_dict[label] = value

    incomes_df = pd.DataFrame.from_dict(incomes_dict,orient='index')\
                             .reindex(INCOMES)
    incomes_df.columns = pd.Index(['Households'])

    incomes_df['Dist'] = incomes_df['Households'] / incomes_df['Households'].sum()

    return list(incomes_df['Dist'])
