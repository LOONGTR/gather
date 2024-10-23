# src/train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from src.utils import load_config, setup_logger

config = load_config('config/config.yaml')
logger = setup_logger('train', config['logging']['training_log'])

def train_model(data_path, labels_path, model_path):
    logger.info("加载预处理数据...")
    df = pd.read_csv(data_path)
    labels_df = pd.read_csv(labels_path)
    
    # 假设 labels.csv 中有 'pid' 和 'label' 列
    logger.info("合并数据和标签...")
    df = df.merge(labels_df, on='pid', how='left')
    
    # 填充缺失标签为正常（0）
    df['label'] = df['label'].fillna(0)
    
    X = df[['cpu_percent', 'memory_rss', 'name_length', 'cmdline_length']]
    y = df['label']
    
    logger.info("分割数据集...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    logger.info("训练模型...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    logger.info("评估模型...")
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred)
    logger.info(f"分类报告:\n{report}")
    
    logger.info("保存模型...")
    joblib.dump(clf, model_path)
    logger.info(f"模型已保存到 {model_path}。")

if __name__ == "__main__":
    data_path = config['data']['processed']
    labels_path = config['data']['labels']
    model_path = config['model']['path']
    train_model(data_path, labels_path, model_path)
