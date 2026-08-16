# Railway部署指南

## 快速部署

### 方法一：使用Railway CLI（推荐）

```bash
# 1. 安装Railway CLI
npm install -g @railway/cli

# 2. 登录
railway login

# 3. 初始化项目
cd /Users/venda/Documents/ChatGPT/文生图片/property-management/backend
railway init

# 4. 设置环境变量
railway variables set DATABASE_URL=sqlite+aiosqlite:///./test.db
railway variables set JWT_SECRET=your-secret-key-here
railway variables set CORS_ORIGINS=*

# 5. 部署
railway up
```

### 方法二：使用Railway Dashboard

1. 访问: https://railway.app/
2. 使用GitHub账号登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择仓库: bjhck001-sketch/property-management
5. 配置环境变量:
   - DATABASE_URL: sqlite+aiosqlite:///./test.db
   - JWT_SECRET: your-secret-key-here
   - CORS_ORIGINS: *
6. 点击 "Deploy"

## 环境变量

| 变量名 | 值 | 说明 |
|--------|-----|------|
| DATABASE_URL | sqlite+aiosqlite:///./test.db | 数据库连接 |
| JWT_SECRET | your-secret-key-here | JWT密钥 |
| CORS_ORIGINS | * | 允许的域名 |

## 免费额度

- 每月$5免费额度
- 包含：
  - 1个服务
  - 512MB内存
  - 0.1 vCPU
  - 1GB网络出口流量

## 访问地址

部署后，Railway会提供访问地址：
- API: https://property-api-xxx.railway.app
- 文档: https://property-api-xxx.railway.app/docs

## 测试账号

| 角色 | 手机号 | 密码 |
|------|--------|------|
| 管理员 | 13800138002 | adminpass123 |
| 工作人员 | 13800138003 | staffpass123 |
| 业主 | 13800138001 | testpass123 |
