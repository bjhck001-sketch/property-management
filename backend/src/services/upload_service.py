"""上传服务 - 支持本地存储和MinIO"""
import os
import uuid
from pathlib import Path
from typing import Optional, List
from fastapi import UploadFile
from src.config import settings

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 支持的文件类型
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".mp4"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


async def upload_file(file: UploadFile, subdir: str = "general") -> str:
    """上传文件到本地存储"""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {ext}")
    
    # 生成唯一文件名
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / subdir / filename
    
    # 创建子目录
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存文件
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("文件大小超过限制")
    
    file_path.write_bytes(content)
    return f"/uploads/{subdir}/{filename}"


async def upload_files(files: List[UploadFile], subdir: str = "general") -> List[str]:
    """批量上传文件"""
    results = []
    for file in files:
        url = await upload_file(file, subdir)
        results.append(url)
    return results


def get_file_url(filepath: str) -> str:
    """获取文件访问URL"""
    return f"{settings.API_URL}/uploads{filepath}"


def delete_file(filepath: str) -> bool:
    """删除文件"""
    file_path = UPLOAD_DIR / filepath.lstrip("/")
    if file_path.exists():
        file_path.unlink()
        return True
    return False
