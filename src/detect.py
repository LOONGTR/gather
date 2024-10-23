# src/detect.py
import psutil
import time
import joblib
import numpy as np
from src.utils import load_config, setup_logger

config = load_config('config/config.yaml')
logger = setup_logger('detect', config['logging']['detect_log'])

# 加载训练好的模型
model = joblib.load(config['model']['path'])
logger.info(f"加载模型完成：{config['model']['path']}")

def extract_features(proc):
    features = {}
    features['cpu_percent'] = proc['cpu_percent']
    features['memory_rss'] = proc['memory_info']
    features['name_length'] = len(proc['name']) if proc['name'] else 0
    features['cmdline_length'] = len(proc['cmdline']) if proc['cmdline'] else 0
    # 添加更多特征
    return [features['cpu_percent'], features['memory_rss'], features['name_length'], features['cmdline_length']]

def terminate_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        logger.info(f"[终止] 进程 {pid} 已被终止。")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
        logger.error(f"[错误] 无法终止进程 {pid}: {e}")

def monitor_and_detect():
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                proc_info = proc.info
                features = extract_features(proc_info)
                features_np = np.array(features).reshape(1, -1)
                prediction = model.predict(features_np)
                if prediction[0] == 1:
                    logger.warning(f"[警告] 发现可疑进程: {proc_info['name']} (PID: {proc_info['pid']})")
                    terminate_process(proc_info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        time.sleep(config['monitoring']['interval'])  # 每指定秒数检测一次

if __name__ == "__main__":
    logger.info("启动实时检测...")
    monitor_and_detect()
