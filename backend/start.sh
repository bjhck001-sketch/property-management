#!/bin/bash
# 物业管理APP - 快速启动脚本

echo "==================================="
echo "物业管理APP - 启动中..."
echo "==================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

cd "$(dirname "$0")/backend"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f "requirements_installed" ]; then
    echo "安装 Python 依赖..."
    pip install -q -r requirements.txt
    pip install -q -r requirements-test.txt
    pip install -q pandas openpyxl xlrd
    touch requirements_installed
fi

# 设置数据库
export DATABASE_URL="sqlite+aiosqlite:///./test.db"

# 删除旧数据库
rm -f test.db

# 初始化数据库
echo "初始化数据库..."
PYTHONPATH=. python3 scripts/init_db.py 2>&1 | grep -v "bcrypt"

# 创建测试用户
echo "创建测试用户..."
PYTHONPATH=. python3 scripts/setup_test_data.py 2>&1 | grep -v "bcrypt"

# 运行测试
echo ""
echo "运行测试..."
python3 -m pytest tests/ -q 2>&1 | tail -3

echo ""
echo "启动后端服务..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 等待服务启动
sleep 2

echo ""
echo "==================================="
echo "服务已启动!"
echo "==================================="
echo ""
echo "访问地址:"
echo "  📱 API文档: http://localhost:8000/docs"
echo "  💻 Web演示: 打开 demo.html"
echo "  📱 业主端: 打开 owner-demo.html"
echo ""
echo "测试账号:"
echo "  👑 管理员: 13800138002 / adminpass123"
echo "  👨‍💼 工作人员: 13800138003 / staffpass123"
echo "  🏠 业主: 13800138001 / testpass123"
echo ""
echo "按 Ctrl+C 停止服务"
echo "==================================="

# 捕获退出信号
trap "kill $BACKEND_PID 2>/dev/null; exit 0" INT TERM

# 等待用户中断
wait
