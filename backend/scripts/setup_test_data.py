"""创建测试用户"""
import asyncio
from src.database import engine, Base, async_session_maker
from src.models.user import User
from src.middleware import get_password_hash
from sqlalchemy import select
from datetime import datetime

async def setup():
    # 初始化数据库
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_maker() as session:
        # 检查并创建测试用户
        test_users = [
            {'phone': '13800138001', 'password': 'testpass123', 'role': 'owner', 'name': 'Test User'},
            {'phone': '13800138002', 'password': 'adminpass123', 'role': 'admin', 'name': 'Test Admin'},
            {'phone': '13800138003', 'password': 'staffpass123', 'role': 'staff', 'name': 'Test Staff'},
        ]
        
        for u in test_users:
            result = await session.execute(select(User).where(User.phone == u['phone']))
            if not result.scalar_one_or_none():
                user = User(
                    phone=u['phone'],
                    password_hash=get_password_hash(u['password']),
                    role=u['role'],
                    name=u['name'],
                    status=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(user)
                print(f'Created: {u["phone"]} ({u["role"]})')
            else:
                print(f'Exists: {u["phone"]}')
        
        await session.commit()
        
        # 验证用户
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f'\nTotal users: {len(users)}')
        for u in users:
            print(f'  - {u.phone}: {u.name} [{u.role}] status={u.status}')

if __name__ == '__main__':
    asyncio.run(setup())
