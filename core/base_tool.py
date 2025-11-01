from abc import ABC, abstractmethod
from typing import Any, Dict
from core.schemas import ToolMetadata, ToolExecutionResult


class BaseTool(ABC):
    """工具基类"""
    
    @abstractmethod
    def get_metadata(self) -> ToolMetadata:
        """返回工具元数据"""
        pass
    
    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> ToolExecutionResult:
        """
        执行工具逻辑
        
        Args:
            inputs: 输入参数字典
            
        Returns:
            ToolExecutionResult: 执行结果
        """
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """验证输入参数"""
        metadata = self.get_metadata()
        for field in metadata.input_fields:
            if field.required and field.name not in inputs:
                raise ValueError(f"缺少必需参数: {field.label}")
        return True
