# src/monitor.py
import psutil
import time
import json
import os
from src.utils import load_config, setup_logger

config = load_config('config/config.yaml')
logger = setup_logger('monitor', config['logging']['monitor_log'])

def get_process_info():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            process_list.append({
                'pid': info['pid'],
                'name': info['name'],
                'exe': info['exe'],
                'cmdline': ' '.join(info['cmdline']) if info['cmdline'] else '',
                'cpu_percent': info['cpu_percent'],
                'memory_info': info['memory_info'].rss  # 使用物理内存（字节）
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return process_list

def monitor_system(interval=5):
    raw_data_path = config['data']['raw']
    while True:
        processes = get_process_info()
        log_entry = {
            'timestamp': int(time.time()),
            'processes': processes
        }
        with open(raw_data_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        logger.info(f"Logged {len(processes)} processes at {log_entry['timestamp']}")
        time.sleep(interval)

if __name__ == "__main__":
    logger.info("启动系统监控...")
    monitor_system(interval=config['monitoring']['interval'])
