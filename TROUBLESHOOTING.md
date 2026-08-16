# 物业管理APP - 故障排查指南

## 登录失败问题排查

### 1. 检查后端服务状态

```bash
# 测试 API 连接
curl http://localhost:8000/docs

# 测试登录接口
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}'
```

### 2. 检查数据库连接

```bash
# 确认数据库文件存在
ls -la backend/test.db

# 运行数据库初始化脚本
cd backend
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py
```

### 3. 检查环境变量

```bash
# 确认环境变量设置
echo $DATABASE_URL
# 应该输出: sqlite+aiosqlite:///./test.db
```

### 4. 常见问题

#### 问题1: 数据库连接失败
**原因**: PostgreSQL 未运行
**解决**: 使用 SQLite 测试数据库
```bash
export DATABASE_URL=sqlite+aiosqlite:///./test.db
```

#### 问题2: 用户不存在
**原因**: 测试用户未创建
**解决**: 运行 setup_test_data.py
```bash
cd backend
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py
```

#### 问题3: 密码验证失败
**原因**: 密码哈希不匹配
**解决**: 重新创建用户
```bash
rm -f backend/test.db
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py
```

#### 问题4: 账户被禁用
**原因**: user.status = False
**解决**: 更新用户状态
```python
# 在数据库中设置 status=True
```

### 5. 测试账号

| 角色 | 手机号 | 密码 |
|------|--------|------|
| 管理员 | 13800138002 | adminpass123 |
| 工作人员 | 13800138003 | staffpass123 |
| 业主 | 13800138001 | testpass123 |

### 6. 日志查看

```bash
# 后端日志
tail -f backend/logs/app.log

# 前端日志
cd frontend-web
npm run dev 2>&1 | tail -50
```

### 7. 快速重置

```bash
# 停止所有服务
pkill -f uvicorn
pkill -f "next dev"

# 清理数据库
cd backend
rm -f test.db

# 重新创建测试数据
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py

# 重启服务
./start.sh
```

## 测试命令

```bash
# 运行所有测试
cd backend
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m pytest tests/ -v

# 只运行认证测试
python3 -m pytest tests/test_auth.py -v

# 运行登录测试
python3 -m pytest tests/test_auth.py::TestAuth::test_login_success -v
```

## API 端点验证

```bash
# 注册新用户
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139000","password":"test123","role":"owner","name":"Test"}'

# 登录获取 token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}'

# 获取用户信息
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```
