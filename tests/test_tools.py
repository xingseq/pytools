import pytest
from tools.text_transform.tool import TextTransformTool
from tools.image_resize.tool import ImageResizeTool


def test_text_transform_uppercase():
    """测试文本转大写"""
    tool = TextTransformTool()
    result = tool.run({
        "text": "hello world",
        "operation": "转大写"
    })
    
    assert result.success is True
    assert result.output == "HELLO WORLD"


def test_text_transform_reverse():
    """测试文本反转"""
    tool = TextTransformTool()
    result = tool.run({
        "text": "hello",
        "operation": "反转"
    })
    
    assert result.success is True
    assert result.output == "olleh"


def test_text_transform_count():
    """测试统计字数"""
    tool = TextTransformTool()
    result = tool.run({
        "text": "hello world\ntest",
        "operation": "统计字数"
    })
    
    assert result.success is True
    assert "字符数: 17" in result.output


def test_tool_metadata():
    """测试工具元数据"""
    tool = TextTransformTool()
    metadata = tool.get_metadata()
    
    assert metadata.id == "text_transform"
    assert metadata.name == "文本转换"
    assert len(metadata.input_fields) == 2
