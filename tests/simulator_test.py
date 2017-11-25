import unittest
import simulator

PA_FIPS = '42'
PHILADELPHIA_FIPS = '110'

class TestSimulator(unittest.TestCase):

    def test_get_household_sizes_pdf(self):
        pdf = simulator.get_household_sizes_pdf(PA_FIPS, PHILADELPHIA_FIPS)
        for p in pdf:
            self.assertTrue(p < 1.0)
            self.assertTrue(p > 0)

    def test_get_incomes_pdf(self):
        pdf = simulator.get_incomes_pdf(PA_FIPS, PHILADELPHIA_FIPS)
        for p in pdf:
            self.assertTrue(p < 1.0)
            self.assertTrue(p > 0)

    def test_get_income_from_bucket(self):
        income = simulator.get_income_from_bucket(1)
        for p in pdf:
            self.assertTrue(income < 15000)
            self.assertTrue(income > 10000)

if __name__ == '__main__':
    unittest.main()
