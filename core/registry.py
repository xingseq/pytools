import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type
from core.base_tool import BaseTool


class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        """注册工具"""
        metadata = tool.get_metadata()
        self._tools[metadata.id] = tool
    
    def get_tool(self, tool_id: str) -> BaseTool:
        """获取工具实例"""
        if tool_id not in self._tools:
            raise ValueError(f"工具不存在: {tool_id}")
        return self._tools[tool_id]
    
    def get_all_tools(self) -> Dict[str, BaseTool]:
        """获取所有工具"""
        return self._tools
    
    def auto_discover(self, tools_package: str = "tools"):
        """自动发现并注册tools目录下的所有工具"""
        try:
            tools_module = importlib.import_module(tools_package)
            tools_path = Path(tools_module.__path__[0])
            
            for finder, name, ispkg in pkgutil.iter_modules([str(tools_path)]):
                if ispkg:
                    try:
                        module = importlib.import_module(f"{tools_package}.{name}.tool")
                        # 查找BaseTool的子类
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (isinstance(attr, type) and 
                                issubclass(attr, BaseTool) and 
                                attr is not BaseTool):
                                tool_instance = attr()
                                self.register(tool_instance)
                                print(f"✓ 已注册工具: {tool_instance.get_metadata().name}")
                    except Exception as e:
                        print(f"✗ 加载工具 {name} 失败: {e}")
        except Exception as e:
            print(f"工具自动发现失败: {e}")
    
    def clear(self):
        """清空注册表"""
        self._tools.clear()


# 全局注册中心
registry = ToolRegistry()