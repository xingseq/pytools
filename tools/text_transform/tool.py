from typing import Any, Dict
from core.base_tool import BaseTool
from core.schemas import ToolMetadata, ToolInputField, ToolExecutionResult


class TextTransformTool(BaseTool):
    """文本转换工具"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            id="text_transform",
            name="文本转换",
            description="对文本进行大小写转换、反转、去重等操作",
            category="文本处理",
            icon="📝",
            version="1.0.0",
            input_fields=[
                ToolInputField(
                    name="text",
                    label="输入文本",
                    type="textarea",
                    required=True,
                    placeholder="请输入要处理的文本..."
                ),
                ToolInputField(
                    name="operation",
                    label="操作类型",
                    type="select",
                    required=True,
                    options=["转大写", "转小写", "反转", "去除空格", "统计字数"],
                    default="转大写"
                )
            ]
        )
    
    def run(self, inputs: Dict[str, Any]) -> ToolExecutionResult:
        logs = []
        
        try:
            text = inputs.get("text", "")
            operation = inputs.get("operation", "转大写")
            
            logs.append(f"输入文本长度: {len(text)} 字符")
            logs.append(f"执行操作: {operation}")
            
            if operation == "转大写":
                result = text.upper()
            elif operation == "转小写":
                result = text.lower()
            elif operation == "反转":
                result = text[::-1]
            elif operation == "去除空格":
                result = text.replace(" ", "").replace("\n", "").replace("\t", "")
            elif operation == "统计字数":
                result = f"字符数: {len(text)}\n单词数: {len(text.split())}\n行数: {len(text.splitlines())}"
            else:
                return ToolExecutionResult(
                    success=False,
                    error=f"不支持的操作: {operation}",
                    logs=logs
                )
            
            logs.append(f"✓ 处理完成")
            
            return ToolExecutionResult(
                success=True,
                output=result,
                logs=logs
            )
            
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                error=str(e),
                logs=logs
            )
