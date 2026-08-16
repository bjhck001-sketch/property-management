#!/bin/bash
# 物业管理APP - Google Cloud部署脚本
# 使用前请先安装Google Cloud CLI并登录

set -e

echo "=========================================="
echo "物业管理APP - Google Cloud部署脚本"
echo "=========================================="
echo ""

# 配置变量
PROJECT_ID="project-9f52d49f-6b89-4c78-93e"
REGION="us-central1"
BACKEND_NAME="property-api"
FRONTEND_NAME="property-web"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "项目ID: $PROJECT_ID"
echo "区域: $REGION"
echo ""

# 检查gcloud是否安装
if ! command -v gcloud &> /dev/null; then
    echo "❌ 错误: 未找到gcloud命令"
    echo ""
    echo "请先安装Google Cloud CLI:"
    echo "  方法1: brew install --cask google-cloud-sdk"
    echo "  方法2: 访问 https://cloud.google.com/sdk/docs/install"
    echo ""
    exit 1
fi

# 检查是否已登录
echo "检查登录状态..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ 错误: 未登录Google Cloud"
    echo ""
    echo "请先登录:"
    echo "  gcloud auth login"
    echo ""
    exit 1
fi
echo "✅ 已登录"
echo ""

# 设置项目
echo "设置项目..."
gcloud config set project $PROJECT_ID
echo "✅ 项目已设置: $PROJECT_ID"
echo ""

# 启用API
echo "启用API服务..."
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
echo "✅ API已启用"
echo ""

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到Docker命令"
    echo ""
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    echo ""
    exit 1
fi

# 检查Docker是否运行
if ! docker info &> /dev/null; then
    echo "❌ 错误: Docker未运行"
    echo ""
    echo "请先启动Docker Desktop"
    echo ""
    exit 1
fi
echo "✅ Docker已运行"
echo ""

# 构建并部署后端
echo "=========================================="
echo "部署后端API..."
echo "=========================================="

cd "$BASE_DIR/backend"

# 构建Docker镜像
echo "构建Docker镜像..."
docker build -t gcr.io/$PROJECT_ID/$BACKEND_NAME:latest .

# 推送镜像
echo "推送镜像到Container Registry..."
gcloud docker -- push gcr.io/$PROJECT_ID/$BACKEND_NAME:latest

# 部署到Cloud Run
echo "部署到Cloud Run..."
gcloud run deploy $BACKEND_NAME \
  --image gcr.io/$PROJECT_ID/$BACKEND_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=sqlite+aiosqlite:///./test.db \
  --set-env-vars JWT_SECRET=your-secret-key-here \
  --set-env-vars CORS_ORIGINS=https://$(gcloud run services describe $BACKEND_NAME --platform managed --region $REGION --format="value(status.url)")

BACKEND_URL=$(gcloud run services describe $BACKEND_NAME --platform managed --region $REGION --format="value(status.url)")
echo "✅ 后端API已部署: $BACKEND_URL"
echo ""

# 构建并部署前端
echo "=========================================="
echo "部署Web管理后台..."
echo "=========================================="

cd "$BASE_DIR/frontend-web"

# 构建Docker镜像
echo "构建Docker镜像..."
docker build -t gcr.io/$PROJECT_ID/$FRONTEND_NAME:latest .

# 推送镜像
echo "推送镜像到Container Registry..."
gcloud docker -- push gcr.io/$PROJECT_ID/$FRONTEND_NAME:latest

# 部署到Cloud Run
echo "部署到Cloud Run..."
gcloud run deploy $FRONTEND_NAME \
  --image gcr.io/$PROJECT_ID/$FRONTEND_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=$BACKEND_URL/api/v1

FRONTEND_URL=$(gcloud run services describe $FRONTEND_NAME --platform managed --region $REGION --format="value(status.url)")
echo "✅ Web管理后台已部署: $FRONTEND_URL"
echo ""

# 完成
echo "=========================================="
echo "部署完成!"
echo "=========================================="
echo ""
echo "访问地址:"
echo "  📱 API文档: $BACKEND_URL/docs"
echo "  💻 Web管理后台: $FRONTEND_URL"
echo ""
echo "测试账号:"
echo "  管理员: 13800138002 / adminpass123"
echo "  业主: 13800138001 / testpass123"
echo ""
echo "=========================================="
