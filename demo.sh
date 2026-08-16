#!/bin/bash
# 物业管理APP - 演示脚本

echo "=========================================="
echo "物业管理APP - 本地演示环境"
echo "=========================================="
echo ""

# 检查后端服务
echo "[1/4] 检查后端服务..."
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "  ✅ 后端服务运行中: http://localhost:8000"
else
    echo "  ❌ 后端服务未启动，正在启动..."
    cd "$(dirname "$0")/backend"
    DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 &
    sleep 3
fi

# 检查前端服务
echo ""
echo "[2/4] 检查前端服务..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "  ✅ 前端服务运行中: http://localhost:3000"
else
    echo "  ❌ 前端服务未启动，正在启动..."
    cd "$(dirname "$0")/frontend-web"
    export PATH="$HOME/.agnes/config/mcp-hermit/bin:$PATH"
    npm run dev &
    sleep 3
fi

# 确保测试数据存在
echo ""
echo "[3/4] 检查测试数据..."
if [ ! -f "backend/test.db" ]; then
    echo "  创建测试数据..."
    cd "$(dirname "$0")/backend"
    PYTHONPATH=. DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py 2>&1 | grep -v "bcrypt"
fi

echo ""
echo "[4/4] 运行测试..."
cd "$(dirname "$0")/backend"
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m pytest tests/ -q 2>&1 | tail -3

echo ""
echo "=========================================="
echo "演示环境已就绪!"
echo "=========================================="
echo ""
echo "访问地址:"
echo "  📱 API文档: http://localhost:8000/docs"
echo "  💻 Web管理后台: http://localhost:3000"
echo ""
echo "测试账号:"
echo "  👑 管理员: 13800138002 / adminpass123"
echo "  👨‍💼 工作人员: 13800138003 / staffpass123"
echo "  🏠 业主: 13800138001 / testpass123"
echo ""
echo "功能演示:"
echo "  1. 打开 http://localhost:3000 登录 Web 管理后台"
echo "  2. 使用管理员账号登录"
echo "  3. 查看仪表板、用户管理、房产管理等页面"
echo "  4. 打开 http://localhost:8000/docs 查看 API 文档"
echo ""
echo "按 Ctrl+C 停止服务"
echo "=========================================="

# 等待用户中断
trap "kill $(jobs -p) 2>/dev/null; exit 0" INT TERM
wait
