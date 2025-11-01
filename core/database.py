from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from typing import Optional
import json

Base = declarative_base()


class ExecutionHistoryModel(Base):
    """执行历史记录表"""
    __tablename__ = "execution_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_id = Column(String(100), nullable=False, index=True)
    tool_name = Column(String(200), nullable=False)
    inputs = Column(Text, nullable=False)  # JSON
    result = Column(Text, nullable=False)  # JSON
    created_at = Column(DateTime, default=datetime.now, index=True)


class Database:
    """数据库管理"""
    
    def __init__(self, db_url: str = "sqlite+aiosqlite:///./pytools.db"):
        self.engine = create_async_engine(db_url, echo=False)
        self.session_maker = async_sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
    
    async def init_db(self):
        """初始化数据库"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def save_history(self, tool_id: str, tool_name: str, inputs: dict, result: dict):
        """保存执行历史"""
        async with self.session_maker() as session:
            history = ExecutionHistoryModel(
                tool_id=tool_id,
                tool_name=tool_name,
                inputs=json.dumps(inputs, ensure_ascii=False),
                result=json.dumps(result, ensure_ascii=False, default=str)
            )
            session.add(history)
            await session.commit()
            return history.id
    
    async def get_history(self, limit: int = 50, tool_id: Optional[str] = None):
        """获取执行历史"""
        from sqlalchemy import select, desc
        
        async with self.session_maker() as session:
            query = select(ExecutionHistoryModel).order_by(desc(ExecutionHistoryModel.created_at))
            
            if tool_id:
                query = query.where(ExecutionHistoryModel.tool_id == tool_id)
            
            query = query.limit(limit)
            result = await session.execute(query)
            records = result.scalars().all()
            
            return [
                {
                    "id": r.id,
                    "tool_id": r.tool_id,
                    "tool_name": r.tool_name,
                    "inputs": json.loads(r.inputs),
                    "result": json.loads(r.result),
                    "created_at": r.created_at.isoformat()
                }
                for r in records
            ]
    
    async def get_history_by_id(self, history_id: int):
        """根据ID获取历史记录"""
        from sqlalchemy import select
        
        async with self.session_maker() as session:
            query = select(ExecutionHistoryModel).where(ExecutionHistoryModel.id == history_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            
            if record:
                return {
                    "id": record.id,
                    "tool_id": record.tool_id,
                    "tool_name": record.tool_name,
                    "inputs": json.loads(record.inputs),
                    "result": json.loads(record.result),
                    "created_at": record.created_at.isoformat()
                }
            return None


# 全局数据库实例
db = Database()
