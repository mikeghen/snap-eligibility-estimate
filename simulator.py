from census import Census
from us import states
import pandas as pd
import numpy as np
import random

# Maps income buckets to range of incomes
# TODO: Consolidate this with INCOMES
INCOMES_BUCKETS = {
    0: [0,9999],      #'< $10k',
    1: [10000,14999], #'$10k - $14.9k',
    2: [15000,19999], #'$15k - $19.9k',
    3: [20000,24999], #'$20k - $24.9k',
    4: [25000,29999], #'$25k - $29.9k',
    5: [30000,34999], #'$30k - $34.9k',
    6: [35000,39999], #'$35k - $39.9k',
    7: [40000,44999], #'$40k - $44.9k',
    8: [45000,49999], #'$45k - $49.9k',
    9: [50000,59999], #'$50k - $59.9k',
    10: [60000,74999], #'$60k - $74.9k',
    11: [75000,99999], #'$75k - $99.9k',
    12: [100000,124999], #'$100k - $124.9k',
    13: [125000,149999], #'$125k - $149.9k',
    14: [150000,199999], #'$150k - $199.9k',
    15: [200000,1000000] #'$200k +'
}

# Eligibilty stats from:
# http://www.dhs.pa.gov/citizens/supplementalnutritionassistanceprogram/snapincomelimits/
# household_size: (max_gross_monthly_income, max_gross_monthly_income_elderly_disabled)
SNAP_ELIGIBILITY = {
    0: (1608, 2010),
    1: (2166, 2708),
    2: (2723, 3404),
    3: (3280, 4100),
    4: (3838, 4798),
    5: (4395, 5494),
    6: (4952, 6190),
    7: (5510, 6888),
    8: (6068, 7586),
    9: (6626, 8284)
}

PA_COUNTIES = {
    #'Adams':	1,
    'Allegheny':3,
    # 'Armstrong':5,
    # 'Beaver':	7,
    # 'Bedford':	9,
    # 'Berks':	11,
    # 'Blair':	13,
    # 'Bradford':	15,
    'Bucks':	17,
    # 'Butler':	19,
    # 'Cambria':	21,
    # 'Cameron':	23,
    # 'Carbon':	25,
    # 'Centre':	27,
    # 'Chester':	29,
    # 'Clarion':	31,
    # 'Clearfield':33,
    # 'Clinton':	35,
    # 'Columbia':	37,
    # 'Crawford':	39,
    # 'Cumberland':41,
    # 'Dauphin':	43,
    # 'Delaware':	45,
    'Elk':	    47,
    # 'Erie':	    49,
    # 'Fayette':	51,
    # 'Forest':	53,
    # 'Franklin':	55,
    # 'Fulton':	57,
    # 'Greene':	59,
    # 'Huntingdon':61,
    # 'Indiana':	63,
    # 'Jefferson':65,
    # 'Juniata':	67,
    # 'Lackawanna':69,
    # 'Lancaster': 71,
    # 'Lawrence':	 73,
    # 'Lebanon':	 75,
    # 'Lehigh':	 77,
    # 'Luzerne':	 79,
    # 'Lycoming':	 81,
    # 'McKean':	 83,
    # 'Mercer':	 85,
    # 'Mifflin':	 87,
    # 'Monroe':	 89,
    'Montgomery':91,
    # 'Montour':	 93,
    # 'Northampton':	95,
    # 'Northumberland':	97,
    # 'Perry':	        99,
    'Philadelphia':	    101
    # 'Pike':	            103,
    # 'Potter':	        105,
    # 'Schuylkill':	    107,
    # 'Snyder':	        109,
    # 'Somerset':	        111,
    # 'Sullivan':	        113,
    # 'Susquehanna':	    115,
    # 'Tioga':	        117,
    # 'Union':	        119,
    # 'Venango':	        121,
    # 'Warren':	        123,
    # 'Washington':	    125,
    # 'Wayne':	        127,
    # 'Westmoreland':	129,
    # 'Wyoming':	    131,
    # 'York':	        133
}

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
    return list(household_size_df['Dist']), int(total_households)


def get_incomes_pdf(state_code, county_code, household_size=None):
    """
    Returns a probability density function for incomes. Parallel to INCOMES
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
    total_incomes = income_results[0]['B19101_001E']
    incomes_dict = {}
    for name, value in income_results[0].items():
        label = acs5_incomes_names_labels[name]
        if label != 'Total':
            incomes_dict[label] = value

    incomes_df = pd.DataFrame.from_dict(incomes_dict,orient='index')\
                             .reindex(INCOMES)
    incomes_df.columns = pd.Index(['Households'])

    incomes_df['Dist'] = incomes_df['Households'] / incomes_df['Households'].sum()

    return list(incomes_df['Dist']), int(total_incomes)


def get_income_from_bucket(bucket):
    """
    Returns an exact income in dollars based on the income bucket (integer)
    """
    low, high  = INCOMES_BUCKETS[bucket]
    return random.uniform(low, high)


def get_elderly_households_probabilities(state_code, county_code):
    """
    Returns the probabilty that a household will have one or more people 65 years and over
    """
    acs5_elderly_labels = {
        'B11007_003E': 'Estimate!!Total!!Households with one or more people 65 years and over!!1-person household',
        'B11007_004E': 'Estimate!!Total!!Households with one or more people 65 years and over!!2-or-more-person household',
        'B11007_008E': 'Estimate!!Total!!Households with no people 65 years and over!!1-person households',
        'B11007_009E': 'Estimate!!Total!!Households with no people 65 years and over!!2-or-more-person household'
    }

    elderly_fields = [name for name, label in acs5_elderly_labels.items()]
    elderly_results = C.acs5.state_county(elderly_fields, state_code, county_code)

    del elderly_results[0]['state']  # we know what state we're working with
    del elderly_results[0]['county'] # we know what county we're working with

    elderly_numerator = float(elderly_results[0]['B11007_003E'])
    elderly_denominator = float(elderly_results[0]['B11007_008E']) + elderly_numerator
    one_person_elderly_prob = elderly_numerator / elderly_denominator

    elderly_numerator = float(elderly_results[0]['B11007_004E'])
    elderly_denominator = float(elderly_results[0]['B11007_009E']) + elderly_numerator
    two_or_more_person_elderly_prob = elderly_numerator / elderly_denominator

    return one_person_elderly_prob, two_or_more_person_elderly_prob


def build_elderly_probabilities():
    """
    Returns a dictionary where keys are county codes and tuples probabilities

    NOTE: This needs some work, coupled to PA, did this quick for a demo
    """
    elderly_rates_by_county = {}
    for county, fips_code in PA_COUNTIES.items():
        one_person_elderly_prob, two_or_more_person_elderly_prob = \
           get_elderly_households_probabilities(42,fips_code)
        elderly_rates_by_county[fips_code] = (one_person_elderly_prob, two_or_more_person_elderly_prob)

    return elderly_rates_by_county


def is_snap_eligible(household):
    """
    Returns 1 if household size and income make it eligible for SNAP in PA
    0 otherwise
    """

    max_monthly_income = SNAP_ELIGIBILITY[int(household['size'])]

    if max_monthly_income >= household['income'] / 12:
        return int(household['size'])
    else:
        return 0


def get_household_size_incomes_pdf(household_size, state_code, county_code):
    """
    Generates a income PDF for household_size households
    """
    acs5_household_sizes_median_incomes = {
        1: 'B19019_002E',
        2: 'B19019_003E',
        3: 'B19019_004E',
        4: 'B19019_005E',
        5: 'B19019_006E',
        6: 'B19019_007E',
        7: 'B19019_008E'
    }

    field = acs5_household_sizes_median_incomes[household_size]
    results = C.acs5.state_county(field, state_code, county_code)
    median_income = results[0][field]

    # NOTE: Assume sigma = median / 4, use median as mean
    samples = np.random.normal(median_income, 200000/6, 10000)
    pdf_dict = {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
        8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0
    }
    for sample in samples:
        for bucket, rng in INCOMES_BUCKETS.items():
            if sample < rng[1] and sample >= rng[0]:
                pdf_dict[bucket] += 1

    incomes_df = pd.DataFrame.from_dict(pdf_dict,orient='index')
    incomes_df.columns = pd.Index(['Households'])
    incomes_df['Dist'] = incomes_df['Households'] / incomes_df['Households'].sum()

    return list(incomes_df['Dist'])


class MonteCarlo:

    def __init__(self):
        print("Initializing MonteCarlo")
        self.STATE_CODE = 42
        self.elderly_rates_by_county = build_elderly_probabilities()
        print("Done Initializing MonteCarlo")


    def is_snap_eligible(self, household):
        """
        Returns 1 if household size and income make it eligible for SNAP in PA
        0 otherwise

        TODO: elderly_rates_by_county was added for a quick demo, probably better to
              move this an other functions into the class...
        """
        # 1 in 5 households has an elderly or disabled person
        is_elderly = np.random.choice([0,1,2,3,4])

        max_monthly_income, max_gross_monthly_income_elderly_disabled = SNAP_ELIGIBILITY[int(household['size'])]

        if is_elderly == 0:
            income_threshold = max_gross_monthly_income_elderly_disabled
        else:
            income_threshold = max_monthly_income

        if income_threshold >= household['income'] / 12:
            return int(household['size'])
        else:
            return 0


    def run(self, county_fips):
        """
        Simulates SNAP eligibilty for a single state county
        """
        print("Running for", county_fips )
        results = {}

        # Run Monte Carlo Simulation for Households' Sizes for PA
        p, num_households = get_household_sizes_pdf(self.STATE_CODE, county_fips)
        total_households = num_households
        household_size_df = pd.DataFrame()
        income_df = pd.DataFrame()
        households = [] # Parallel to incomes
        incomes = []    # Parallel to households

        household_size_sim_data = [0,0,0,0,0,0,0]
        for i in range(0,num_households):
            household_size = np.random.choice(np.arange(0, 7), p=p)
            households.append(household_size)
            household_size_sim_data[household_size] += 1

        household_size_df = pd.concat([household_size_df, pd.DataFrame({county_fips:household_size_sim_data})], axis=1)

        # Run Monte Carlo Simulation for Incomes for Philadelphia
        p, n = get_incomes_pdf(self.STATE_CODE, county_fips)

        income_sim_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0,num_households):
            income = np.random.choice(np.arange(0, 16), p=p)
            incomes.append(income)
            income_sim_data[income] += 1

        income_df = pd.concat([income_df, pd.DataFrame({county_fips:income_sim_data})], axis=1)

        """
        Zip incomes and household sizes together in a DataFrame, compute eligibilty
        output the results.
        """
        households_df = pd.DataFrame({'size':households, 'income':incomes})
        households_df['income'] = households_df['income'].apply(get_income_from_bucket)
        households_df['snap_eligible'] = households_df.apply(self.is_snap_eligible, axis=1)
        households_df.head(100).to_csv('data.csv')
        individuals = households_df['size'].sum()
        snap_eligible = households_df['snap_eligible'].sum()

        return (county_fips, snap_eligible)
