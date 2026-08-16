# Railway部署配置

## 配置Railway

### 1. 创建Railway项目
1. 访问: https://railway.app/
2. 登录GitHub账号
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择仓库: property-management

### 2. 配置环境变量

在Railway Dashboard中设置以下环境变量：

```
DATABASE_URL=sqlite+aiosqlite:///./test.db
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=*
```

### 3. 配置构建

Railway会自动检测Dockerfile并构建。

### 4. 部署

点击 "Deploy" 按钮。

## 故障排除

如果构建失败：

1. 检查Railway日志
2. 确保Dockerfile正确
3. 检查依赖文件

## 访问地址

部署成功后：
- API: https://property-management-xxx.railway.app
- 文档: https://property-management-xxx.railway.app/docs
