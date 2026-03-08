"""
测试工具模块发现
"""
import importlib
import pkgutil
from pathlib import Path
import sys
import pytest


class TestToolDiscovery:
    """测试工具发现功能"""
    
    def test_tools_module_exists(self):
        """测试tools模块可以导入"""
        try:
            tools_module = importlib.import_module("tools")
            assert tools_module.__path__ is not None
            print(f"tools模块路径: {tools_module.__path__}")
        except ImportError as e:
            pytest.fail(f"无法导入tools模块: {e}")
    
    def test_tools_submodules(self):
        """测试工具子模块"""
        tools_module = importlib.import_module("tools")
        tools_path = Path(tools_module.__path__[0])
        
        # 列出所有子模块
        submodules = list(pkgutil.iter_modules([str(tools_path)]))
        assert len(submodules) >= 3, f"应该至少有3个子模块，实际有{len(submodules)}个"
        
        # 验证预期的子模块存在
        expected_submodules = {"image_resize", "image_split", "text_transform"}
        actual_submodules = {name for _, name, _ in submodules}
        assert expected_submodules.issubset(actual_submodules), \
            f"缺少子模块: {expected_submodules - actual_submodules}"
        
        print(f"找到的子模块: {actual_submodules}")
    
    def test_tool_module_import(self):
        """测试可以导入工具模块"""
        tool_modules = [
            "tools.image_resize.tool",
            "tools.image_split.tool", 
            "tools.text_transform.tool"
        ]
        
        for module_name in tool_modules:
            try:
                module = importlib.import_module(module_name)
                print(f"成功导入模块: {module_name}")
                
                # 检查模块中是否有BaseTool的子类
                has_tool_class = False
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        attr.__name__ not in ['BaseTool', 'object', 'ABC'] and 
                        hasattr(attr, '__bases__')):
                        for base in attr.__bases__:
                            if base.__name__ == 'BaseTool':
                                has_tool_class = True
                                print(f"  找到工具类: {attr_name}")
                                break
                
                assert has_tool_class, f"模块{module_name}中没有找到BaseTool的子类"
                
            except ImportError as e:
                pytest.fail(f"无法导入模块{module_name}: {e}")
    
    def test_tool_class_instantiation(self):
        """测试工具类可以实例化"""
        tool_classes = [
            ("tools.image_resize.tool", "ImageResizeTool"),
            ("tools.image_split.tool", "ImageSplitTool"),
            ("tools.text_transform.tool", "TextTransformTool")
        ]
        
        for module_name, class_name in tool_classes:
            try:
                module = importlib.import_module(module_name)
                tool_class = getattr(module, class_name)
                instance = tool_class()
                
                # 检查元数据
                metadata = instance.get_metadata()
                assert metadata.id is not None
                assert metadata.name is not None
                
                print(f"成功实例化: {class_name} (ID: {metadata.id}, 名称: {metadata.name})")
                
            except Exception as e:
                pytest.fail(f"无法实例化{class_name}: {e}")


if __name__ == "__main__":
    pytest.main([__file__])