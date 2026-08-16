# 物业管理APP v1.0.0

> 物业管理系统 - 后端API + Web管理后台 + 移动端APP

## 版本信息

- **版本号**: v1.0.0
- **发布日期**: 2026-08-16
- **状态**: 测试完成，可发布

## 系统要求

### 后端
- Python 3.9+
- PostgreSQL 15+ (推荐) 或 SQLite (测试)
- pip 包管理

### Web管理后台
- Node.js 18+
- npm 9+

### 移动端 (可选)
- Flutter 3.10+
- Dart 3.0+

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your-username/property-management.git
cd property-management
```

### 2. 启动后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt

# 初始化数据库
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/init_db.py
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 scripts/setup_test_data.py

# 启动服务
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --reload --port 8000
```

### 3. 启动Web管理后台
```bash
cd frontend-web
npm install
npm run dev
```

### 4. 访问应用
- API文档: http://localhost:8000/docs
- Web管理后台: http://localhost:3000
- 演示页面: 打开 demo.html 或 owner-demo.html

## 测试账号

| 角色 | 手机号 | 密码 |
|------|--------|------|
| 管理员 | 13800138002 | adminpass123 |
| 工作人员 | 13800138003 | staffpass123 |
| 业主 | 13800138001 | testpass123 |

## 功能特性

### 后端API
- ✅ 用户认证 (JWT)
- ✅ 用户管理
- ✅ 房产管理
- ✅ 账单管理
- ✅ 支付模块
- ✅ 报修管理
- ✅ 访客管理
- ✅ 投诉建议
- ✅ 通知系统
- ✅ 工单管理
- ✅ 巡检任务
- ✅ 管理员统计
- ✅ 图片上传
- ✅ 批量导入 (Excel/CSV)

### Web管理后台
- ✅ 登录认证
- ✅ 仪表板
- ✅ 用户管理
- ✅ 房产管理
- ✅ 账单管理
- ✅ 报修管理
- ✅ 访客管理
- ✅ 投诉建议
- ✅ 系统设置

### 移动端 (架构设计)
- ✅ 业主端APP架构
- ✅ 工作人员端APP架构
- ✅ HTML5演示版本

## 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.111.0 |
| ORM | SQLAlchemy | 2.0.31 |
| 数据库 | PostgreSQL/SQLite | 15+/3.44+ |
| 认证 | JWT + bcrypt | - |
| Web框架 | Next.js | 14.2.0 |
| 语言 | TypeScript | 5.x |
| 样式 | Tailwind CSS | 4.x |
| UI库 | shadcn/ui | latest |
| 移动端框架 | Flutter | 3.x |
| 状态管理 | Riverpod | 2.4.0 |
| HTTP客户端 | Dio | 5.3.0 |
| 数据处理 | pandas | 2.x |

## 测试

```bash
cd backend
python3 -m pytest tests/ -v
```

**测试结果**: 74 passed, 1 skipped

## 项目结构

```
property-management/
├── backend/                    # FastAPI 后端
│   ├── src/
│   │   ├── models/            # 数据库模型 (9个)
│   │   ├── schemas/           # Pydantic Schema (9个)
│   │   ├── routers/           # API路由 (14个)
│   │   ├── services/          # 业务逻辑
│   │   ├── middleware.py      # 认证中间件
│   │   └── main.py            # 应用入口
│   ├── tests/                 # 单元测试 (11个文件)
│   ├── scripts/               # 工具脚本
│   ├── requirements.txt       # Python依赖
│   └── Dockerfile             # Docker配置
├── frontend-web/               # Next.js Web管理后台
│   ├── app/                   # 页面路由
│   ├── components/            # React组件
│   ├── lib/                   # API客户端
│   └── package.json
├── frontend-mobile/            # Flutter 移动端
│   ├── lib/                   # Dart源代码
│   └── pubspec.yaml           # Flutter依赖
├── demo.html                   # Web管理后台演示
├── owner-demo.html             # 业主移动端演示
├── docker-compose.yml          # Docker部署
├── README.md                   # 项目说明
├── API_DOCS.md                 # API文档
├── DEPLOYMENT.md               # 部署指南
└── DEVELOPMENT_PLAN.md         # 开发计划
```

## API文档

启动后端服务后访问: http://localhost:8000/docs

## 部署

### Docker部署
```bash
docker-compose up -d
```

### 手动部署
见 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 许可证

MIT License

## 联系方式

- 项目作者: AgnesCode
- 项目地址: https://github.com/your-username/property-management

---

**版本 v1.0.0 完成！**
