#!/bin/bash
# 物业管理APP演示脚本
# 一键启动所有服务并打开演示页面

echo "=========================================="
echo "物业管理APP - 演示环境启动"
echo "=========================================="
echo ""

# 检查后端服务
echo "🔍 检查后端服务..."
if lsof -i :8000 | grep -q LISTEN; then
    echo "✅ 后端服务已在运行"
else
    echo "🚀 启动后端服务..."
    cd /Users/venda/Documents/ChatGPT/文生图片/property-management/backend
    DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 > /tmp/uvicorn.log 2>&1 &
    sleep 3
    echo "✅ 后端服务已启动"
fi
echo ""

# 测试API
echo "🧪 测试API..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"phone":"13800138002","password":"adminpass123"}' | \
    python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo "✅ API测试成功"
else
    echo "⚠️ API测试失败，请检查后端服务"
fi
echo ""

# 打开演示页面
echo "🌐 打开演示页面..."
open http://localhost:8000/docs
sleep 1
open /Users/venda/Documents/ChatGPT/文生图片/property-management/demo.html
sleep 1
open /Users/venda/Documents/ChatGPT/文生图片/property-management/owner-demo.html
echo ""

# 显示信息
echo "=========================================="
echo "✅ 演示环境已就绪！"
echo "=========================================="
echo ""
echo "📱 访问地址:"
echo "   • API文档: http://localhost:8000/docs"
echo "   • Web管理后台: demo.html (已打开)"
echo "   • 业主端: owner-demo.html (已打开)"
echo ""
echo "🔐 测试账号:"
echo "   • 管理员: 13800138002 / adminpass123"
echo "   • 工作人员: 13800138003 / staffpass123"
echo "   • 业主: 13800138001 / testpass123"
echo ""
echo "📊 项目信息:"
echo "   • GitHub: https://github.com/bjhck001-sketch/property-management"
echo "   • Railway: https://railway.app/project/4030d709-1789-44bf-8c25-43e8cbe1d235"
echo "   • 版本: v1.0.7"
echo ""
echo "=========================================="
echo "演示脚本: /Users/venda/Documents/ChatGPT/文生图片/property-management/demo.sh"
echo "=========================================="
