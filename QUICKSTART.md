# 物业管理APP - 快速开始

## 本地开发

### 后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=sqlite+aiosqlite:///./test.db python3 -m uvicorn src.main:app --reload
```

### 前端
```bash
cd frontend-web
npm install
npm run dev
```

## 部署到Google Cloud

### 前置条件
1. 安装Google Cloud CLI: `brew install --cask google-cloud-sdk`
2. 登录: `gcloud auth login`
3. 设置项目: `gcloud config set project project-9f52d49f-6b89-4c78-93e`
4. 安装Docker: https://docs.docker.com/get-docker/

### 一键部署
```bash
./deploy-gcp.sh
```

### 手动部署
详见 [DEPLOY_GCP.md](./DEPLOY_GCP.md)

## 测试账号

| 角色 | 手机号 | 密码 |
|------|--------|------|
| 管理员 | 13800138002 | adminpass123 |
| 工作人员 | 13800138003 | staffpass123 |
| 业主 | 13800138001 | testpass123 |
