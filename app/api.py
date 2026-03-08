from fastapi import APIRouter, Request, HTTPException, Form, File
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.datastructures import UploadFile
from typing import Optional
import json
from pathlib import Path

from core.registry import registry
from core.executor import ToolExecutor
from core.database import db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
executor = ToolExecutor(max_workers=4)


@router.get("/", response_class=HTMLResponse)
@router.head("/")
async def index(request: Request):
    """首页 - 工具列表"""
    tools = registry.get_all_tools()
    tools_data = [
        {
            "metadata": tool.get_metadata().model_dump(),
        }
        for tool in tools.values()
    ]
    
    # 按类别分组
    categories = {}
    for item in tools_data:
        category = item["metadata"]["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "categories": categories,
            "total_tools": len(tools_data)
        }
    )


@router.get("/tool/{tool_id}", response_class=HTMLResponse)
@router.head("/tool/{tool_id}")
async def tool_detail(request: Request, tool_id: str):
    """工具详情页"""
    try:
        tool = registry.get_tool(tool_id)
        metadata = tool.get_metadata()
        
        return templates.TemplateResponse(
            "tool_detail.html",
            {
                "request": request,
                "metadata": metadata.model_dump()
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/api/tool/{tool_id}/execute")
async def execute_tool_stream(request: Request, tool_id: str):
    """执行工具（SSE流式输出）"""
    try:
        tool = registry.get_tool(tool_id)
        metadata = tool.get_metadata()
        
        # 解析表单数据
        form_data = await request.form()
        inputs = {}
        
        print(f"[DEBUG] 收到的表单字段: {list(form_data.keys())}")  # 调试日志
        
        for field in metadata.input_fields:
            value = form_data.get(field.name)
            
            print(f"[DEBUG] 字段 {field.name}: type={type(value)}, value={value if not isinstance(value, UploadFile) else f'UploadFile({value.filename})'}")
            
            if field.type == "file":
                print(f"[DEBUG] 检查文件字段: isinstance={isinstance(value, UploadFile)}, filename={getattr(value, 'filename', None)}, bool(filename)={bool(getattr(value, 'filename', None))}")
                if isinstance(value, UploadFile) and value.filename and len(value.filename) > 0:
                    # 保存上传文件
                    upload_dir = Path("uploads")
                    upload_dir.mkdir(exist_ok=True)
                    upload_path = upload_dir / value.filename
                    
                    # 读取并保存文件内容
                    file_content = await value.read()
                    print(f"[DEBUG] 文件内容大小: {len(file_content)} bytes")
                    
                    with open(upload_path, "wb") as f:
                        f.write(file_content)
                    
                    inputs[field.name] = str(upload_path)
                    print(f"[DEBUG] 文件已保存: {upload_path}, 文件大小: {upload_path.stat().st_size} bytes")
                else:
                    # 如果是必填字段但没有文件，设为 None
                    inputs[field.name] = None
                    print(f"[DEBUG] 未接收到文件，value类型: {type(value)}, value: {value}")
            elif field.type == "number":
                if value:
                    inputs[field.name] = float(value) if '.' in value else int(value)
            else:
                inputs[field.name] = value
        
        print(f"[DEBUG] 最终inputs: {inputs}")  # 调试日志
        
        # 流式执行
        async def event_generator():
            final_result = None
            async for event in executor.execute_with_stream(tool, inputs):
                yield event
                # 捕获最终结果
                if '\"type\": \"complete\"' in event:
                    try:
                        result_data = json.loads(event.split("'result': ")[1].rstrip("}'\n\n"))
                        final_result = result_data
                    except:
                        pass
            
            # 保存历史记录
            if final_result:
                await db.save_history(
                    tool_id=tool_id,
                    tool_name=metadata.name,
                    inputs=inputs,
                    result=final_result
                )
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/history")
@router.head("/api/history")
async def get_history(tool_id: Optional[str] = None, limit: int = 50):
    """获取执行历史"""
    history = await db.get_history(limit=limit, tool_id=tool_id)
    return JSONResponse(content=history)


@router.get("/api/history/{history_id}")
@router.head("/api/history/{history_id}")
async def get_history_detail(history_id: int):
    """获取历史详情"""
    history = await db.get_history_by_id(history_id)
    if not history:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return JSONResponse(content=history)


@router.get("/history", response_class=HTMLResponse)
@router.head("/history")
async def history_page(request: Request):
    """历史记录页面"""
    return templates.TemplateResponse(
        "history.html",
        {"request": request}
    )


@router.get("/api/tools")
@router.head("/api/tools")
async def list_tools():
    """列出所有已注册的工具"""
    tools = registry.get_all_tools()
    tools_list = []
    for tool_id, tool in tools.items():
        metadata = tool.get_metadata()
        tools_list.append({
            "id": tool_id,
            "name": metadata.name,
            "description": metadata.description,
            "category": metadata.category,
            "version": metadata.version,
            "input_fields": [field.model_dump() for field in metadata.input_fields]
        })
    return JSONResponse(content=tools_list)