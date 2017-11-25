import pandas as pd
import numpy as np
import simulator

"""
Work in progress

STEP 1: Produce the Income PDF for a county from the US Census data
"""
income_pdf, n = simulator.get_incomes_pdf(42, 101) # Philadelphia

"""
STEP 2: Produce the normally distributed PDF for a household size
"""
household_size = 4
household_size_income_pdf = simulator.get_household_size_incomes_pdf(household_size)
"""
STEP 3: Sum the two PDFs together
"""
df = pd.DataFrame({'income_pdf':income_pdf,
                   'household_size_income_pdf':household_size_income_pdf})
df['adjusted_pdf'] = df.sum(axis=0)

"""
STEP 4: Normalize to get the household size adjusted income PDF
"""
df['adjusted_pdf'] =(df['adjusted_pdf']-df['adjusted_pdf'].min()) /
                    (df['adjusted_pdf'].max()-df['adjusted_pdf'].min())
