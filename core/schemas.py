from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ToolInputField(BaseModel):
    """工具输入字段定义"""
    name: str
    label: str
    type: str = Field(description="text, textarea, number, file, select")
    required: bool = True
    default: Optional[Any] = None
    placeholder: Optional[str] = None
    options: Optional[List[str]] = None
    help_text: Optional[str] = None


class ToolMetadata(BaseModel):
    """工具元数据"""
    id: str
    name: str
    description: str
    category: str = "通用"
    icon: str = "🔧"
    version: str = "1.0.0"
    input_fields: List[ToolInputField]


class ToolExecutionRequest(BaseModel):
    """工具执行请求"""
    tool_id: str
    inputs: Dict[str, Any]


class ToolExecutionResult(BaseModel):
    """工具执行结果"""
    success: bool
    output: Optional[Any] = None
    error: Optional[str] = None
    logs: List[str] = []
    files: List[Dict[str, str]] = []  # [{"name": "file.png", "path": "/outputs/xxx.png"}]
    execution_time: float = 0.0


class ExecutionHistory(BaseModel):
    """执行历史记录"""
    id: int
    tool_id: str
    tool_name: str
    inputs: Dict[str, Any]
    result: ToolExecutionResult
    created_at: datetime
    
    class Config:
        from_attributes = True
