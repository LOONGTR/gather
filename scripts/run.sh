# scripts/run.sh
#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 启动监控模块
python src/monitor.py &

# 启动实时检测模块
python src/detect.py &

echo "反外挂系统已启动。"

# 等待所有后台进程
wait
