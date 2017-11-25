import matplotlib.pyplot as plt
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
household_size = 7
household_size_income_pdf = simulator.get_household_size_incomes_pdf(household_size, 42, 101)
print("PDF:", household_size_income_pdf)
"""
STEP 3: Sum the two PDFs together
"""
df = pd.DataFrame({'income_pdf':income_pdf,
                   'household_size_income_pdf':household_size_income_pdf})
df['adjusted_pdf'] = df['income_pdf'] + df['household_size_income_pdf']
print("DF:", df)


"""
STEP 4: Normalize to get the household size adjusted income PDF
"""
df['adjusted_pdf'] = df['adjusted_pdf'] / df['adjusted_pdf'].sum()
df.index = simulator.INCOMES
print("DF Normalized:", df)


axes = df.plot(kind='bar',subplots=True, title='Income PDF Adjustment for Philadelphia County')
axes[0].set_title('Income PDF (household_size = 7)')
axes[1].set_title('Income PDF (All Households)')
axes[2].set_title('Household Size Adjusted PDF (household_size = 7)')
plt.show()
