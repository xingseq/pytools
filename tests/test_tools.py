"""
测试工具功能
"""
import pytest
import tempfile
import os
from pathlib import Path
from PIL import Image

from tools.text_transform.tool import TextTransformTool
from tools.image_resize.tool import ImageResizeTool
from tools.image_split.tool import ImageSplitTool


@pytest.fixture
def temp_image_file():
    """创建临时图片文件供测试使用"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        # 创建一个简单的测试图片
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tmp.name, 'PNG')
        temp_path = tmp.name
    
    yield temp_path
    
    # 清理
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestTextTransformTool:
    """测试文本转换工具"""
    
    def test_tool_metadata(self):
        """测试工具元数据"""
        tool = TextTransformTool()
        metadata = tool.get_metadata()
        
        assert metadata.id == "text_transform"
        assert metadata.name == "文本转换"
        assert metadata.category == "文本处理"
        assert len(metadata.input_fields) == 2
    
    def test_uppercase_operation(self):
        """测试文本转大写"""
        tool = TextTransformTool()
        result = tool.run({
            "text": "hello world",
            "operation": "转大写"
        })
        
        assert result.success is True
        assert result.output == "HELLO WORLD"
        assert "HELLO WORLD" in result.logs[0] if result.logs else True
    
    def test_lowercase_operation(self):
        """测试文本转小写"""
        tool = TextTransformTool()
        result = tool.run({
            "text": "HELLO WORLD",
            "operation": "转小写"
        })
        
        assert result.success is True
        assert result.output == "hello world"
    
    def test_reverse_operation(self):
        """测试文本反转"""
        tool = TextTransformTool()
        result = tool.run({
            "text": "hello",
            "operation": "反转"
        })
        
        assert result.success is True
        assert result.output == "olleh"
    
    def test_remove_spaces_operation(self):
        """测试去除空格"""
        tool = TextTransformTool()
        result = tool.run({
            "text": "hello world  test",
            "operation": "去除空格"
        })
        
        assert result.success is True
        assert result.output == "helloworldtest"
    
    def test_count_chars_operation(self):
        """测试统计字数"""
        tool = TextTransformTool()
        result = tool.run({
            "text": "hello world\ntest",
            "operation": "统计字数"
        })
        
        assert result.success is True
        assert "字符数: 17" in result.output
        assert "单词数: 3" in result.output
        assert "行数: 2" in result.output
    
    def test_invalid_operation(self):
        """测试无效操作"""
        tool = TextTransformTool()
        result = tool.run({
            "text": "hello",
            "operation": "invalid"
        })
        
        assert result.success is False
        assert "不支持的操作" in result.error


class TestImageResizeTool:
    """测试图像缩放工具"""
    
    def test_tool_metadata(self):
        """测试工具元数据"""
        tool = ImageResizeTool()
        metadata = tool.get_metadata()
        
        assert metadata.id == "image_resize"
        assert metadata.name == "图像缩放"
        assert metadata.category == "图像处理"
        assert len(metadata.input_fields) == 5
    
    def test_resize_by_scale(self, temp_image_file):
        """测试按比例缩放"""
        tool = ImageResizeTool()
        result = tool.run({
            "image": temp_image_file,
            "mode": "按比例",
            "scale": 50  # 缩放50%
        })
        
        assert result.success is True
        assert "图片已成功缩放" in result.output
        assert len(result.files) == 1
        assert result.files[0]["name"].startswith("resized_")
        assert result.files[0]["name"].endswith(".png")
    
    def test_resize_by_width(self, temp_image_file):
        """测试按指定宽度缩放"""
        tool = ImageResizeTool()
        result = tool.run({
            "image": temp_image_file,
            "mode": "指定宽度",
            "width": 50
        })
        
        assert result.success is True
        assert "指定宽度" in result.logs[1] if len(result.logs) > 1 else True
    
    def test_resize_by_height(self, temp_image_file):
        """测试按指定高度缩放"""
        tool = ImageResizeTool()
        result = tool.run({
            "image": temp_image_file,
            "mode": "指定高度",
            "height": 50
        })
        
        assert result.success is True
        assert "指定高度" in result.logs[1] if len(result.logs) > 1 else True
    
    def test_resize_by_dimensions(self, temp_image_file):
        """测试按指定宽高缩放"""
        tool = ImageResizeTool()
        result = tool.run({
            "image": temp_image_file,
            "mode": "指定宽高",
            "width": 80,
            "height": 80
        })
        
        assert result.success is True
        assert "指定尺寸" in result.logs[1] if len(result.logs) > 1 else True
    
    def test_invalid_image_path(self):
        """测试无效图片路径"""
        tool = ImageResizeTool()
        result = tool.run({
            "image": "/nonexistent/image.png",
            "mode": "按比例"
        })
        
        assert result.success is False
        assert "图片文件不存在" in result.error
    
    def test_invalid_mode(self, temp_image_file):
        """测试无效缩放模式"""
        tool = ImageResizeTool()
        result = tool.run({
            "image": temp_image_file,
            "mode": "invalid_mode"
        })
        
        assert result.success is False
        assert "不支持的模式" in result.error


class TestImageSplitTool:
    """测试图片切分工具"""
    
    def test_tool_metadata(self):
        """测试工具元数据"""
        tool = ImageSplitTool()
        metadata = tool.get_metadata()
        
        assert metadata.id == "image_split"
        assert metadata.name == "图片切分"
        assert metadata.category == "图像处理"
        assert len(metadata.input_fields) == 7
    
    def test_split_by_rows_cols(self, temp_image_file):
        """测试按行列数切分"""
        tool = ImageSplitTool()
        result = tool.run({
            "image": temp_image_file,
            "split_method": "按行列数切分",
            "rows": 2,
            "cols": 2,
            "output_format": "PNG"
        })
        
        assert result.success is True
        assert "图片切分完成" in result.output
        assert len(result.files) == 1
        assert result.files[0]["name"].startswith("split_images_")
        assert result.files[0]["name"].endswith(".zip")
        assert "共生成 4 个切片" in result.output
    
    def test_split_by_fixed_size(self, temp_image_file):
        """测试按固定尺寸切分"""
        tool = ImageSplitTool()
        result = tool.run({
            "image": temp_image_file,
            "split_method": "按固定尺寸切分",
            "slice_width": 50,
            "slice_height": 50,
            "output_format": "PNG"
        })
        
        assert result.success is True
        assert "固定尺寸" in result.logs[2] if len(result.logs) > 2 else True
    
    def test_invalid_image_path(self):
        """测试无效图片路径"""
        tool = ImageSplitTool()
        result = tool.run({
            "image": "/nonexistent/image.png",
            "split_method": "按行列数切分",
            "output_format": "PNG"
        })
        
        assert result.success is False
        assert "图片文件不存在" in result.error


if __name__ == "__main__":
    pytest.main([__file__])