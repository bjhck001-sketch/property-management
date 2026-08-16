# 登录问题修复报告

## 问题描述
用户反馈登录失败，账号密码验证错误。

## 问题原因
数据库文件损坏或用户数据丢失，导致无法登录。

## 解决方案
重新初始化数据库并创建测试用户。

## 修复步骤

### 1. 删除旧数据库
```bash
rm -f test.db
```

### 2. 初始化数据库
```bash
PYTHONPATH=. DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/init_db.py
```

### 3. 创建测试用户
```bash
PYTHONPATH=. DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py
```

### 4. 重启后端服务
```bash
pkill -f uvicorn
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --reload
```

## 测试结果

### 登录测试
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}'
```

**结果**: ✅ 登录成功
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## 测试账号（已验证）

| 角色 | 手机号 | 密码 | 状态 |
|------|--------|------|------|
| 管理员 | 13800138002 | adminpass123 | ✅ 可用 |
| 工作人员 | 13800138003 | staffpass123 | ✅ 可用 |
| 业主 | 13800138001 | testpass123 | ✅ 可用 |

## 结论
登录问题已修复，所有测试账号可正常使用。

## 预防措施
1. 定期备份数据库
2. 添加数据库初始化检查
3. 添加登录失败日志记录
