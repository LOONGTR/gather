# scripts/setup.sh
#!/bin/bash

# 创建虚拟环境
python -m venv venv
echo "虚拟环境已创建。"

# 激活虚拟环境
# 注意：以下命令在 Linux/Mac 上有效，Windows 用户需手动激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
echo "依赖已安装。"

# 取消虚拟环境激活（可选）
deactivate
