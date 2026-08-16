"""批量导入服务 - 支持Excel/CSV"""
import io
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User
from src.models.community import Community
from src.models.community import Community, Property
from src.middleware import get_password_hash


async def import_users_from_excel(file_data: bytes, db: AsyncSession) -> Dict[str, Any]:
    """从Excel导入用户"""
    df = pd.read_excel(io.BytesIO(file_data))
    
    required_columns = ['phone', 'name', 'role']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"缺少必要列: {missing}")
    
    results = {"success": 0, "failed": 0, "errors": []}
    
    for idx, row in df.iterrows():
        try:
            phone = str(row['phone']).strip()
            name = str(row.get('name', '')).strip()
            role = str(row.get('role', 'owner')).strip().lower()
            password = str(row.get('password', '123456')).strip()
            
            # 检查是否已存在
            existing = await db.execute(select(User).where(User.phone == phone))
            if existing.scalar_one_or_none():
                results["errors"].append(f"第{idx+2}行: 手机号{phone}已存在")
                results["failed"] += 1
                continue
            
            # 创建用户
            user = User(
                phone=phone,
                name=name,
                role=role,
                password_hash=get_password_hash(password),
                status=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(user)
            results["success"] += 1
            
        except Exception as e:
            results["errors"].append(f"第{idx+2}行: {str(e)}")
            results["failed"] += 1
    
    await db.commit()
    return results


async def import_properties_from_excel(file_data: bytes, db: AsyncSession) -> Dict[str, Any]:
    """从Excel导入房产"""
    df = pd.read_excel(io.BytesIO(file_data))
    
    required_columns = ['community_id', 'building_no', 'room_no']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"缺少必要列: {missing}")
    
    results = {"success": 0, "failed": 0, "errors": []}
    
    for idx, row in df.iterrows():
        try:
            property_data = {
                'community_id': int(row.get('community_id', 1)),
                'building_no': str(row['building_no']).strip(),
                'unit_no': str(row.get('unit_no', '')),
                'floor_no': str(row.get('floor_no', '')),
                'room_no': str(row['room_no']).strip(),
                'area': float(row.get('area', 100)),
                'owner_id': int(row.get('owner_id', 0)) if pd.notna(row.get('owner_id')) else None
            }
            
            prop = Property(**property_data)
            db.add(prop)
            results["success"] += 1
            
        except Exception as e:
            results["errors"].append(f"第{idx+2}行: {str(e)}")
            results["failed"] += 1
    
    await db.commit()
    return results


async def import_communities_from_excel(file_data: bytes, db: AsyncSession) -> Dict[str, Any]:
    """从Excel导入小区"""
    df = pd.read_excel(io.BytesIO(file_data))
    
    required_columns = ['name', 'address']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"缺少必要列: {missing}")
    
    results = {"success": 0, "failed": 0, "errors": []}
    
    for idx, row in df.iterrows():
        try:
            community = Community(
                name=str(row['name']).strip(),
                address=str(row.get('address', '')).strip(),
                contact_phone=str(row.get('contact_phone', '')),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(community)
            results["success"] += 1
            
        except Exception as e:
            results["errors"].append(f"第{idx+2}行: {str(e)}")
            results["failed"] += 1
    
    await db.commit()
    return results
