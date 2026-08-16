FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pandas openpyxl xlrd 'passlib[bcrypt]==1.7.4'

# 复制应用代码
COPY . .

# 创建上传目录
RUN mkdir -p uploads

# 设置端口
ENV PORT=8080

# 暴露端口
EXPOSE 8080

# 启动应用
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8080"]
