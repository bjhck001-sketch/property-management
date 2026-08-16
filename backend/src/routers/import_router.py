"""批量导入路由"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.middleware import get_current_user, require_role
from src.models.user import User, UserRole
from src.services.import_service import (
    import_users_from_excel,
    import_properties_from_excel,
    import_communities_from_excel
)

router = APIRouter(prefix="/import", tags=["Import"])


@router.post("/users")
async def import_users(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """批量导入用户"""
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="仅支持Excel或CSV文件")
    
    content = await file.read()
    try:
        results = await import_users_from_excel(content, db)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/properties")
async def import_properties(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """批量导入房产"""
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="仅支持Excel或CSV文件")
    
    content = await file.read()
    try:
        results = await import_properties_from_excel(content, db)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/communities")
async def import_communities(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """批量导入小区"""
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="仅支持Excel或CSV文件")
    
    content = await file.read()
    try:
        results = await import_communities_from_excel(content, db)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
