# tests/test_model.py
import unittest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.train import train_model

class TestModel(unittest.TestCase):
    def test_train_model(self):
        # 创建模拟数据
        data = {
            'cpu_percent': [10.5, 20.3, 30.1, 40.2],
            'memory_rss': [104857600, 209715200, 314572800, 419430400],
            'name_length': [11, 15, 12, 14],
            'cmdline_length': [19, 22, 18, 21]
        }
        labels = {
            'pid': [1234, 5678, 91011, 121314],
            'label': [0, 1, 0, 1]
        }
        df = pd.DataFrame(data)
        labels_df = pd.DataFrame(labels)
        
        # 保存到临时文件
        df.to_csv('data/processed/processed_data.csv', index=False)
        labels_df.to_csv('data/labels/labels.csv', index=False)
        
        # 训练模型
        train_model('data/processed/processed_data.csv', 'data/labels/labels.csv', 'models/anti_cheat_model.joblib')
        
        # 检查模型文件是否存在
        import os
        self.assertTrue(os.path.exists('models/anti_cheat_model.joblib'))

if __name__ == '__main__':
    unittest.main()
