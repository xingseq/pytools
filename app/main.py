from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pathlib import Path

from core.registry import registry
from core.database import db
from core.executor import ToolExecutor
from app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 启动 PyTools...")
    
    # 初始化数据库
    await db.init_db()
    print("✓ 数据库初始化完成")
    
    # 自动发现并注册工具
    registry.auto_discover()
    print(f"✓ 已注册 {len(registry.get_all_tools())} 个工具")
    
    # 创建必要目录
    Path("uploads").mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)
    
    yield
    
    # 关闭时
    print("👋 关闭 PyTools...")


app = FastAPI(
    title="PyTools",
    description="Python工具集Web应用",
    version="0.1.0",
    lifespan=lifespan
)

# 静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# 路由
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
