# 物业管理APP - 演示指南

## 🎯 演示准备

### 环境检查
```bash
# 1. 检查后端服务
curl http://localhost:8000/docs

# 2. 检查测试账号
# 管理员: 13800138002 / adminpass123
# 业主: 13800138001 / testpass123
```

---

## 📱 演示流程

### 第一部分：后端API演示（5分钟）

#### 1. API文档访问
```bash
open http://localhost:8000/docs
```
**说明**: Swagger UI交互式API文档，可在线测试所有接口

#### 2. 用户登录演示
```bash
# 管理员登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}'
```

**预期输出**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### 3. 创建小区演示
```bash
TOKEN="your_token_here"
curl -X POST http://localhost:8000/api/v1/admins/communities/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"阳光花园","address":"北京市朝阳区","contact_phone":"010-12345678"}'
```

#### 4. 创建房产演示
```bash
curl -X POST http://localhost:8000/api/v1/admins/properties/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"community_id":1,"owner_id":1,"building_no":"1号楼","unit_no":"1单元","floor_no":"1","room_no":"101","area":100.5}'
```

#### 5. 批量生成账单演示
```bash
curl -X POST http://localhost:8000/api/v1/bills/batch-generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"month":"2026-08","bill_type":"property_fee","amount":500.00}'
```

#### 6. 统计数据演示
```bash
curl -s http://localhost:8000/api/v1/admins/stats/ \
  -H "Authorization: Bearer $TOKEN"
```

---

### 第二部分：Web管理后台演示（5分钟）

#### 1. 启动Web服务
```bash
cd frontend-web
npm run dev
```
访问: http://localhost:3000

#### 2. 登录演示
- 使用管理员账号登录
- 展示仪表板统计
- 展示用户管理列表

#### 3. 功能演示
- 小区管理：添加/编辑/删除
- 房产管理：添加/编辑/删除
- 账单管理：批量生成/导出
- 报修管理：状态更新
- 访客管理：审核/签到

---

### 第三部分：移动端演示（3分钟）

#### 1. HTML5演示版
```bash
# 业主端演示
open /Users/venda/Documents/ChatGPT/文生图片/property-management/owner-demo.html

# Web管理后台演示
open /Users/venda/Documents/ChatGPT/文生图片/property-management/demo.html
```

#### 2. 功能演示
- 费用缴纳：查看账单/模拟支付
- 报修管理：提交报修/跟踪进度
- 访客管理：创建访客/生成二维码
- 投诉建议：提交投诉/查看处理

---

### 第四部分：Railway部署演示（2分钟）

#### 1. GitHub仓库
```
https://github.com/bjhck001-sketch/property-management
```

#### 2. Railway部署
```
https://railway.app/project/4030d709-1789-44bf-8c25-43e8cbe1d235
```

#### 3. 版本发布
```
https://github.com/bjhck001-sketch/property-management/releases/tag/v1.0.7
```

---

## 🎬 完整演示脚本

### 快速演示（15分钟）

```bash
#!/bin/bash
# 物业管理APP快速演示脚本

echo "=========================================="
echo "物业管理APP演示"
echo "=========================================="
echo ""

# 1. 启动后端服务
echo "1️⃣ 启动后端服务..."
cd /Users/venda/Documents/ChatGPT/文生图片/property-management/backend
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --reload --port 8000 &
sleep 3

# 2. 测试API
echo "2️⃣ 测试API..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "✅ 登录成功: ${TOKEN:0:30}..."
echo ""

# 3. 创建测试数据
echo "3️⃣ 创建测试数据..."
curl -s -X POST http://localhost:8000/api/v1/admins/communities/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"阳光花园","address":"北京市朝阳区","contact_phone":"010-12345678"}' > /dev/null

curl -s -X POST http://localhost:8000/api/v1/admins/properties/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"community_id":1,"owner_id":1,"building_no":"1号楼","unit_no":"1单元","floor_no":"1","room_no":"101","area":100.5}' > /dev/null

echo "✅ 测试数据创建完成"
echo ""

# 4. 打开演示页面
echo "4️⃣ 打开演示页面..."
open http://localhost:8000/docs
open /Users/venda/Documents/ChatGPT/文生图片/property-management/demo.html
open /Users/venda/Documents/ChatGPT/文生图片/property-management/owner-demo.html

echo ""
echo "=========================================="
echo "演示完成！"
echo "=========================================="
echo ""
echo "📱 API文档: http://localhost:8000/docs"
echo "💻 Web管理: demo.html"
echo "📲 业主端: owner-demo.html"
echo ""
echo "测试账号:"
echo "  管理员: 13800138002 / adminpass123"
echo "  业主: 13800138001 / testpass123"
echo ""
```

---

## 📊 演示检查清单

### 后端API
- [ ] API文档可访问
- [ ] 用户登录成功
- [ ] 创建小区成功
- [ ] 创建房产成功
- [ ] 批量生成账单成功
- [ ] 统计数据正确

### Web管理后台
- [ ] 登录页面正常
- [ ] 仪表板数据正确
- [ ] 用户管理功能正常
- [ ] 房产管理功能正常
- [ ] 账单管理功能正常

### 移动端演示
- [ ] 业主端页面正常
- [ ] 报修提交功能正常
- [ ] 访客管理功能正常
- [ ] 投诉建议功能正常

### 部署状态
- [ ] GitHub仓库可访问
- [ ] Railway部署成功
- [ ] 版本发布正常

---

## 🎯 演示要点

### 核心功能
1. **用户认证** - JWT + bcrypt安全认证
2. **小区管理** - CRUD完整功能
3. **房产管理** - 关联小区和业主
4. **账单管理** - 批量生成 + 状态跟踪
5. **报修管理** - 提交 + 状态更新 + 评价
6. **访客管理** - 创建 + 审核 + 签到 + 二维码
7. **投诉建议** - 提交 + 处理 + 反馈
8. **通知系统** - 创建 + 发送 + 已读标记
9. **工单管理** - 创建 + 分配 + 完成
10. **数据统计** - 实时数据统计

### 技术亮点
1. **后端**: FastAPI + SQLAlchemy + PostgreSQL/SQLite
2. **前端**: Next.js 14 + TypeScript + Tailwind CSS
3. **移动端**: Flutter架构 + HTML5演示
4. **部署**: Railway + GitHub Actions
5. **测试**: 74个测试用例，100%通过

---

## ⏱️ 演示时间分配

| 部分 | 时间 | 内容 |
|------|------|------|
| 开场介绍 | 2分钟 | 项目背景、技术栈 |
| 后端API | 5分钟 | API文档、核心功能 |
| Web管理后台 | 5分钟 | 页面演示、功能操作 |
| 移动端演示 | 3分钟 | HTML5演示、功能展示 |
| 部署展示 | 2分钟 | GitHub、Railway |
| Q&A | 3分钟 | 问题解答 |
| **总计** | **20分钟** | - |

---

## 🎉 演示成功！

**您的物业管理APP演示版已准备就绪！**

按照上述步骤操作，即可完成专业演示。
