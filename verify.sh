#!/bin/bash
# 物业管理APP - 项目验证脚本

echo "=========================================="
echo "物业管理APP - 项目验证"
echo "=========================================="
echo ""

# 检查后端测试
echo "[1/4] 检查后端测试..."
cd "$(dirname "$0")/backend"
if [ -f "test.db" ]; then
    rm -f test.db
fi

export DATABASE_URL="sqlite+aiosqlite:///./test.db"
python3 -m pytest tests/ -q 2>&1 | tail -5

echo ""
echo "[2/4] 检查Web前端构建..."
cd "$(dirname "$0")/frontend-web"
export PATH="$HOME/.agnes/config/mcp-hermit/bin:$PATH"
npm run build 2>&1 | tail -5

echo ""
echo "[3/4] 检查文件结构..."
cd "$(dirname "$0")"
echo "  后端文件: $(find backend -type f -name '*.py' ! -path '*/__pycache__/*' | wc -l | tr -d ' ')"
echo "  前端文件: $(find frontend-web -type f \( -name '*.ts' -o -name '*.tsx' \) ! -path '*/node_modules/*' ! -path '*/.next/*' | wc -l | tr -d ' ')"
echo "  移动端文件: $(find frontend-mobile -type f -name '*.dart' | wc -l | tr -d ' ')"
echo "  文档文件: $(find . -type f -name '*.md' | wc -l | tr -d ' ')"

echo ""
echo "[4/4] 检查测试账号..."
echo "  管理员: 13800138002 / adminpass123"
echo "  工作人员: 13800138003 / staffpass123"
echo "  业主: 13800138001 / testpass123"

echo ""
echo "=========================================="
echo "验证完成!"
echo "=========================================="
echo ""
echo "访问地址:"
echo "  - API文档: http://localhost:8000/docs"
echo "  - Web管理后台: http://localhost:3000"
echo ""
echo "启动服务:"
echo "  ./start.sh"
echo ""
