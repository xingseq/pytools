"""
测试工具注册表
"""
import pytest
from core.registry import registry
from tools.image_resize.tool import ImageResizeTool
from tools.image_split.tool import ImageSplitTool
from tools.text_transform.tool import TextTransformTool


class TestRegistry:
    """测试注册表功能"""
    
    def setup_method(self):
        """每个测试方法前执行"""
        registry.clear()  # 清空注册表，确保测试隔离
    
    def test_auto_discover(self):
        """测试自动发现工具"""
        # 执行自动发现
        registry.auto_discover()
        
        # 验证发现的工具数量
        tools = registry.get_all_tools()
        assert len(tools) >= 3, f"应该至少发现3个工具，实际发现{len(tools)}个"
        
        # 验证工具ID存在
        expected_tool_ids = {"image_resize", "image_split", "text_transform"}
        actual_tool_ids = set(tools.keys())
        assert expected_tool_ids.issubset(actual_tool_ids), \
            f"缺少工具: {expected_tool_ids - actual_tool_ids}"
    
    def test_get_tool(self):
        """测试获取单个工具"""
        registry.auto_discover()
        
        # 测试存在的工具
        tool = registry.get_tool("text_transform")
        assert tool is not None
        assert tool.get_metadata().id == "text_transform"
        
        # 测试不存在的工具
        tool = registry.get_tool("nonexistent")
        assert tool is None
    
    def test_register_manual(self):
        """测试手动注册工具"""
        # 清空注册表
        registry.clear()
        
        # 手动注册工具
        tool = TextTransformTool()
        registry.register(tool)
        
        # 验证注册成功
        tools = registry.get_all_tools()
        assert len(tools) == 1
        assert "text_transform" in tools
    
    def test_tool_metadata(self):
        """测试工具元数据"""
        registry.auto_discover()
        
        for tool_id, tool in registry.get_all_tools().items():
            metadata = tool.get_metadata()
            assert metadata.id == tool_id
            assert metadata.name is not None and len(metadata.name) > 0
            assert metadata.description is not None
            assert metadata.version is not None
            assert metadata.category is not None
            assert isinstance(metadata.input_fields, list)
    
    def test_clear_registry(self):
        """测试清空注册表"""
        registry.auto_discover()
        assert len(registry.get_all_tools()) > 0
        
        registry.clear()
        assert len(registry.get_all_tools()) == 0


if __name__ == "__main__":
    pytest.main([__file__])