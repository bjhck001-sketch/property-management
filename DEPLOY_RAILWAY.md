# Railway部署指南

## 当前状态
- ✅ GitHub仓库已更新
- ✅ Dockerfile已优化
- ✅ 部署配置已添加

## 重新部署步骤

### 1. 在Railway Dashboard中重新部署
```
1. 进入项目 property-management
2. 点击 "Deployments" 标签
3. 找到最新的部署记录（显示Failed）
4. 点击 "Retry" 按钮重新部署
```

### 2. 如果仍然失败，请查看日志
```
1. 点击部署记录
2. 点击 "Build Logs" 标签
3. 查看完整的错误信息
4. 将日志截图或复制给我
```

### 3. 配置环境变量（重要）
```
在Railway Dashboard中：
1. 点击 "Settings" → "Variables"
2. 添加以下环境变量：
   - DATABASE_URL = sqlite+aiosqlite:///./test.db
   - JWT_SECRET = your-secret-key-here
   - CORS_ORIGINS = *
3. 保存并重新部署
```

## 故障排除

### 问题1：构建失败
**可能原因：**
- Python依赖安装失败
- 系统依赖缺失
- Dockerfile配置错误

**解决方案：**
- 查看Build Logs中的具体错误
- 告诉我错误信息，我会帮您修复

### 问题2：服务无法启动
**可能原因：**
- 端口配置错误
- 环境变量未设置
- 数据库连接失败

**解决方案：**
- 检查环境变量配置
- 查看Deploy Logs
- 确认端口设置为8080

## 测试账号

| 角色 | 手机号 | 密码 |
|------|--------|------|
| 管理员 | 13800138002 | adminpass123 |
| 工作人员 | 13800138003 | staffpass123 |
| 业主 | 13800138001 | testpass123 |

## 部署成功后访问

- API: https://property-management-xxx.railway.app
- 文档: https://property-management-xxx.railway.app/docs
