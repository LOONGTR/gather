# tests/test_preprocess.py
import unittest
import pandas as pd
from src.preprocess import preprocess_data

class TestPreprocess(unittest.TestCase):
    def test_preprocess_data(self):
        data = {
            'cpu_percent': [10.5, 20.3],
            'memory_rss': [104857600, 209715200],
            'name': ['example.exe', 'cheatengine.exe'],
            'cmdline': ['example.exe -arg1', 'cheatengine.exe -speed 100']
        }
        df = pd.DataFrame(data)
        processed_df = preprocess_data(df)
        self.assertEqual(len(processed_df), 2)
        self.assertIn('cpu_percent', processed_df.columns)
        self.assertIn('memory_rss', processed_df.columns)
        self.assertIn('name_length', processed_df.columns)
        self.assertIn('cmdline_length', processed_df.columns)

if __name__ == '__main__':
    unittest.main()
