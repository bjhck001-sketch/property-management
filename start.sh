#!/bin/bash

echo "==================================="
echo "物业管理APP - 快速启动脚本"
echo "==================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js"
    exit 1
fi

# 后端服务
echo "[1/3] 启动后端服务..."
cd "$(dirname "$0")/backend"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "  创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f "requirements_installed" ]; then
    echo "  安装 Python 依赖..."
    pip install -q -r requirements.txt
    pip install -q -r requirements-test.txt
    touch requirements_installed
fi

# 设置测试数据库
export DATABASE_URL="sqlite+aiosqlite:///./test.db"

# 创建测试用户
echo "  创建测试数据..."
PYTHONPATH=. python3 scripts/setup_test_data.py

# 启动后端
echo "  启动后端服务器 (http://localhost:8000)..."
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Web 前端
echo ""
echo "[2/3] 启动 Web 管理后台..."
cd "$(dirname "$0")/frontend-web"

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "  安装 Node.js 依赖..."
    npm install
fi

# 启动前端
echo "  启动前端服务器 (http://localhost:3000)..."
npm run dev &
FRONTEND_PID=$!

# 等待服务启动
echo ""
echo "等待服务启动..."
sleep 3

echo ""
echo "==================================="
echo "服务已启动:"
echo "  - API 文档: http://localhost:8000/docs"
echo "  - Web 管理后台: http://localhost:3000"
echo ""
echo "测试账号:"
echo "  - 管理员: 13800138002 / adminpass123"
echo "  - 工作人员: 13800138003 / staffpass123"
echo "  - 业主: 13800138001 / testpass123"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "==================================="

# 捕获退出信号
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

# 等待用户中断
wait
