# 物业管理APP - 部署指南

## 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+
- Python 3.12+
- Flutter 3.10+ (移动端开发)

## 快速启动

### 1. 后端服务

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 设置数据库连接

# 运行测试
python3 -m pytest tests/ -v

# 启动开发服务器
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Web管理后台

```bash
cd frontend-web
npm install
npm run dev
# 访问 http://localhost:3000
```

### 3. Docker Compose 部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

## API 文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试账号

| 角色 | 手机号 | 密码 |
|------|--------|------|
| 管理员 | 13800138002 | adminpass123 |
| 工作人员 | 13800138003 | staffpass123 |
| 业主 | 13800138001 | testpass123 |

## 项目结构

```
property-management/
├── backend/                  # FastAPI 后端
│   ├── src/
│   │   ├── models/          # 数据库模型
│   │   ├── schemas/         # Pydantic Schema
│   │   ├── routers/         # API 路由
│   │   ├── services/        # 业务逻辑
│   │   ├── middleware.py    # 认证中间件
│   │   └── main.py          # 应用入口
│   ├── tests/               # 单元测试
│   ├── requirements.txt     # Python依赖
│   └── .env.example         # 环境变量模板
├── frontend-web/             # Next.js Web管理后台
│   ├── app/                 # 页面路由
│   ├── components/          # React组件
│   ├── lib/                 # API客户端
│   └── package.json
├── frontend-mobile/          # Flutter 移动端
│   ├── lib/
│   │   ├── core/           # 核心配置
│   │   ├── data/           # 数据层
│   │   ├── presentation/   # 表现层
│   │   └── routes/         # 路由
│   └── pubspec.yaml
└── docker-compose.yml        # Docker部署配置
```

## 环境变量配置

### 后端 (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/property_mgmt
JWT_SECRET=your-secret-key
JWT_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
```

### Web前端 (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 数据库迁移

```bash
# 使用 Alembic 进行数据库迁移
cd backend
alembic init alembic
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

## 性能优化建议

1. **数据库**
   - 添加索引优化查询
   - 使用连接池
   - 定期清理过期数据

2. **API**
   - 启用 Gzip 压缩
   - 添加缓存层 (Redis)
   - 限流保护

3. **前端**
   - 启用代码分割
   - 图片懒加载
   - 使用 CDN

## 安全建议

1. 使用 HTTPS
2. 定期更新依赖
3. 启用 CORS 白名单
4. 敏感数据加密存储
5. 定期备份数据库
