# 物业管理APP - 演示指南

## 环境状态

✅ 后端服务: http://localhost:8000 (运行中)
✅ 前端服务: http://localhost:3000 (运行中)
✅ 测试数据库: backend/test.db
✅ 单元测试: 74 passed, 1 skipped

## 快速访问

| 服务 | 地址 | 说明 |
|------|------|------|
| API文档 | http://localhost:8000/docs | Swagger UI - 可在线测试API |
| API文档(备用) | http://localhost:8000/redoc | ReDoc |
| Web管理后台 | http://localhost:3000 | Next.js应用 |

## 测试账号

| 角色 | 手机号 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | 13800138002 | adminpass123 | 全部权限 |
| 工作人员 | 13800138003 | staffpass123 | 工单/巡检 |
| 业主 | 13800138001 | testpass123 | 业主功能 |

## 演示流程

### 1. API文档演示 (5分钟)

打开 http://localhost:8000/docs

**演示步骤:**
1. 点击 "POST /api/v1/auth/login"
2. 点击 "Try it out"
3. 输入测试账号:
   ```json
   {
     "phone": "13800138002",
     "password": "adminpass123"
   }
   ```
4. 点击 "Execute" 获取 Token
5. 点击 "Authorize" 输入 Token
6. 测试其他接口:
   - GET /api/v1/admins/stats/ (统计数据)
   - GET /api/v1/users/ (用户列表)
   - GET /api/v1/properties/ (房产列表)

### 2. Web管理后台演示 (10分钟)

打开 http://localhost:3000

**演示步骤:**
1. 使用管理员账号登录
2. 查看仪表板 - 数据统计
3. 用户管理 - 列表/搜索/权限
4. 房产管理 - 添加/编辑/删除
5. 账单管理 - 批量生成
6. 报修管理 - 状态跟踪
7. 访客管理 - 审核/签到
8. 系统设置

### 3. 移动端演示 (5分钟)

展示 Flutter 项目结构:
```bash
cd frontend-mobile
ls -la lib/
```

展示已完成的页面:
- 登录/注册页面
- 业主端首页
- 工作人员端首页
- 费用缴纳页面
- 报修管理页面
- 访客管理页面

## API 测试脚本

```bash
# 登录获取 Token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 获取用户信息
curl -s http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# 获取统计数据
curl -s http://localhost:8000/api/v1/admins/stats/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# 获取用户列表
curl -s http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## 运行测试

```bash
# 运行所有测试
cd backend
python3 -m pytest tests/ -v

# 运行特定模块测试
python3 -m pytest tests/test_auth.py -v
python3 -m pytest tests/test_properties.py -v
python3 -m pytest tests/test_bills.py -v
```

## 启动/停止服务

```bash
# 启动所有服务
./start.sh

# 或单独启动
# 后端
cd backend && DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --reload --port 8000

# 前端
cd frontend-web && npm run dev

# 停止服务
pkill -f uvicorn
pkill -f "next dev"
```

## Docker 部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

## 故障排查

### 问题1: 登录失败
```bash
# 检查用户是否存在
cd backend
python3 -c "
import asyncio
from src.database import async_session_maker
from src.models.user import User
from sqlalchemy import select

async def check():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        for u in result.scalars().all():
            print(f'{u.phone}: {u.name} [{u.role}]')

asyncio.run(check())
"
```

### 问题2: 服务未启动
```bash
# 检查进程
ps aux | grep -E "uvicorn|next"

# 重启服务
./start.sh
```

### 问题3: 端口被占用
```bash
# 查看端口占用
lsof -i :8000
lsof -i :3000

# 杀死进程
pkill -f uvicorn
pkill -f "next dev"
```

## 演示准备清单

- [ ] 后端服务运行中
- [ ] 前端服务运行中
- [ ] 测试账号可用
- [ ] API文档可访问
- [ ] 测试通过 (74/75)
- [ ] 演示脚本准备

## 演示时间分配

| 环节 | 时间 | 内容 |
|------|------|------|
| API演示 | 5分钟 | Swagger UI 在线测试 |
| Web管理后台 | 10分钟 | 核心功能演示 |
| 移动端 | 5分钟 | 页面结构展示 |
| 测试 | 3分钟 | 测试报告 |
| 问答 | 7分钟 | 问题解答 |
| **总计** | **30分钟** | |

## 注意事项

1. 确保后端和前端服务已启动
2. 使用正确的测试账号登录
3. 演示时打开浏览器开发者工具查看网络请求
4. 准备回答技术问题（技术栈、架构、安全等）
5. 备份演示数据

---

**演示就绪! 祝演示成功! 🎉**
