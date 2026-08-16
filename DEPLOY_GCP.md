# 物业管理APP - Google Cloud部署指南

## 部署前准备

### 1. 安装Google Cloud CLI

**macOS:**
```bash
brew install --cask google-cloud-sdk
```

**Linux:**
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-linux-x86_64.tar.gz
tar -xzf google-cloud-sdk-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
```

### 2. 登录Google Cloud

```bash
gcloud auth login
gcloud config set project project-9f52d49f-6b89-4c78-93e
```

### 3. 安装Docker

https://docs.docker.com/get-docker/

---

## 一键部署

```bash
cd /Users/venda/Documents/ChatGPT/文生图片/property-management
./deploy-gcp.sh
```

---

## 手动部署步骤

### 1. 启用API

```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 2. 部署后端

```bash
cd backend

# 构建镜像
docker build -t gcr.io/project-9f52d49f-6b89-4c78-93e/property-api:latest .

# 推送镜像
gcloud docker -- push gcr.io/project-9f52d49f-6b89-4c78-93e/property-api:latest

# 部署
gcloud run deploy property-api \
  --image gcr.io/project-9f52d49f-6b89-4c78-93e/property-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=sqlite+aiosqlite:///./test.db \
  --set-env-vars JWT_SECRET=your-secret-key
```

### 3. 部署前端

```bash
cd frontend-web

# 构建镜像
docker build -t gcr.io/project-9f52d49f-6b89-4c78-93e/property-web:latest .

# 推送镜像
gcloud docker -- push gcr.io/project-9f52d49f-6b89-4c78-93e/property-web:latest

# 部署
gcloud run deploy property-web \
  --image gcr.io/project-9f52d49f-6b89-4c78-93e/property-web:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 免费额度

| 服务 | 免费额度 |
|------|----------|
| Cloud Run | 2百万请求/月 |
| Container Registry | 1GB存储 |
| Cloud SQL (可选) | 不免费 |

**建议**: 使用SQLite进行测试，需要时用Supabase免费PostgreSQL

---

## 费用估算

| 项目 | 月费 |
|------|------|
| Cloud Run (后端) | ¥0 (免费额度内) |
| Cloud Run (前端) | ¥0 (免费额度内) |
| 数据库 | ¥0 (使用SQLite) |
| **总计** | **¥0** |

---

## 访问地址

部署完成后，访问：
- API文档: https://property-api-xxx.a.run.app/docs
- Web管理后台: https://property-web-xxx.a.run.app

---

## 常见问题

### 1. 构建失败
检查Docker是否运行：
```bash
docker info
```

### 2. 权限错误
重新登录：
```bash
gcloud auth login
```

### 3. 服务不可访问
检查Cloud Run服务状态：
```bash
gcloud run services describe property-api --platform managed --region us-central1
```
