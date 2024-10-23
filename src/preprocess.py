# src/preprocess.py
import json
import pandas as pd
from src.utils import load_config, setup_logger

config = load_config('config/config.yaml')
logger = setup_logger('preprocess', config['logging']['training_log'])

def load_process_logs(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            timestamp = entry['timestamp']
            for proc in entry['processes']:
                data.append({
                    'timestamp': timestamp,
                    'pid': proc['pid'],
                    'name': proc['name'],
                    'exe': proc['exe'],
                    'cmdline': proc['cmdline'],
                    'cpu_percent': proc['cpu_percent'],
                    'memory_rss': proc['memory_info']
                })
    return pd.DataFrame(data)

def preprocess_data(df):
    # 示例预处理：将字符串特征转换为数值特征
    df = df.copy()
    df['name_length'] = df['name'].apply(lambda x: len(x) if x else 0)
    df['cmdline_length'] = df['cmdline'].apply(lambda x: len(x) if x else 0)
    # 你可以添加更多特征，如进程路径的哈希值、行为模式等
    df = df[['cpu_percent', 'memory_rss', 'name_length', 'cmdline_length']]
    return df

def main():
    raw_data_path = config['data']['raw']
    processed_data_path = config['data']['processed']
    logger.info("加载原始数据...")
    df = load_process_logs(raw_data_path)
    logger.info(f"原始数据加载完成，共 {len(df)} 条记录。")
    logger.info("开始数据预处理...")
    df_processed = preprocess_data(df)
    df_processed.to_csv(processed_data_path, index=False)
    logger.info(f"预处理后的数据已保存到 {processed_data_path}。")

if __name__ == "__main__":
    main()
