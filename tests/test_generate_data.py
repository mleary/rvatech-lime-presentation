import unittest
import pandas as pd
from data.generate_data import calculate_accident_reported


class TestCalculateAccidentReported(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Body_Style': ['truck', 'sedan', 'truck', 'suv'],
            'Miles_Driven': [18000, 5000, 20000, 15000],
            'Years_Customer': [5, 15, 10, 8],
            'Model_Color': ['Red', 'Blue', 'White', 'Blue']
        })

    def test_calculate_accident_reported(self):
        self.df['Accident_Reported'] = self.df.apply(calculate_accident_reported, axis=1)
        
        # Check that the function returns only 0s and 1s
        self.assertTrue((self.df['Accident_Reported'].isin([0, 1])).all())
        
        # Check that the function returns 1 for trucks with Miles_Driven > 17500
        self.assertEqual(self.df.loc[0, 'Accident_Reported'], 1)
        
        # Check that the function returns 0 for customers with Years_Customer > 10
        self.assertEqual(self.df.loc[1, 'Accident_Reported'], 0)
        
        # Check that the function returns a value based on the sigmoid function for non-trucks with Model_Color == 'Blue'
        self.assertIn(self.df.loc[3, 'Accident_Reported'], [0, 1])

if __name__ == '__main__':
    unittest.main()