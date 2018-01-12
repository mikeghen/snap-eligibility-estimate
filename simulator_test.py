import unittest
import simulator

PA_FIPS = 42
PHILADELPHIA_FIPS = 101

class TestSimulator(unittest.TestCase):


    # def test_get_household_sizes_pdf(self):
    #     pdf = simulator.get_household_sizes_pdf(PA_FIPS, PHILADELPHIA_FIPS)
    #     print(pdf)
    #     for p in pdf:
    #         self.assertTrue(p < 1.0)
    #         self.assertTrue(p > 0)
    #
    #
    # def test_get_incomes_pdf(self):
    #     pdf = simulator.get_incomes_pdf(PA_FIPS, PHILADELPHIA_FIPS)
    #     for p in pdf:
    #         self.assertTrue(p < 1.0)
    #         self.assertTrue(p > 0)
    #
    #
    # def test_get_income_from_bucket(self):
    #     income = simulator.get_income_from_bucket(1)
    #

    # def test_get_elderly_households_probabilities(self):
    #     one_person_elderly_prob, two_or_more_person_elderly_prob = \
    #        simulator.get_elderly_households_probabilities(PA_FIPS, PHILADELPHIA_FIPS)
    #
    #     print(one_person_elderly_prob, two_or_more_person_elderly_prob)

    def test_get_elderly_households_probabilities(self):

        print(simulator.build_elderly_probabilities())


if __name__ == '__main__':
    unittest.main()
