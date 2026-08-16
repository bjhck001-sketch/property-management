# Google Cloud部署前检查

## ✅ 已完成
- [x] Google Cloud CLI安装成功
- [x] 登录成功 (bjhck001@gmail.com)
- [x] 项目设置完成 (project-9f52d49f-6b89-4c78-93e)
- [x] API启用完成 (Cloud Run, Artifact Registry)

## ❌ 需要安装
- [ ] Docker Desktop

## 安装Docker步骤

### 方法1：使用Homebrew（推荐）
```bash
brew install --cask docker
```

安装后：
1. 打开Docker Desktop应用
2. 等待Docker引擎启动（状态栏显示Docker图标）
3. 确认Docker运行：
   ```bash
   docker info
   ```

### 方法2：手动下载
1. 访问: https://www.docker.com/products/docker-desktop/
2. 下载Mac版本（Intel或Apple Silicon）
3. 双击安装包并拖到Applications
4. 打开Docker Desktop并等待启动

## 验证安装
```bash
docker --version
docker info
```

## 部署命令
安装Docker后，运行：
```bash
cd /Users/venda/Documents/ChatGPT/文生图片/property-management
./deploy-gcp.sh
```
