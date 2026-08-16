"""上传路由"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import os

from src.services.upload_service import upload_file, upload_files, ALLOWED_EXTENSIONS
from src.middleware import get_current_user
from src.models.user import User

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("/")
async def upload(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """上传单个文件"""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")
    
    filepath = await upload_file(file)
    return {"url": filepath, "filename": file.filename}


@router.post("/batch")
async def upload_batch(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    """批量上传文件"""
    paths = await upload_files(files)
    return {"urls": paths, "count": len(paths)}


@router.get("/{filepath:path}")
async def get_file(filepath: str):
    """获取文件"""
    file_path = Path("uploads") / filepath
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(file_path)
