from typing import Any, Dict
from pathlib import Path
from PIL import Image
import time

from core.base_tool import BaseTool
from core.schemas import ToolMetadata, ToolInputField, ToolExecutionResult


class ImageResizeTool(BaseTool):
    """图像缩放工具"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            id="image_resize",
            name="图像缩放",
            description="调整图片尺寸，支持按比例或指定宽高",
            category="图像处理",
            icon="🖼️",
            version="1.0.0",
            input_fields=[
                ToolInputField(
                    name="image",
                    label="上传图片",
                    type="file",
                    required=True,
                    help_text="支持 JPG, PNG, GIF 等格式"
                ),
                ToolInputField(
                    name="mode",
                    label="缩放模式",
                    type="select",
                    required=True,
                    options=["按比例", "指定宽度", "指定高度", "指定宽高"],
                    default="按比例"
                ),
                ToolInputField(
                    name="scale",
                    label="缩放比例 (%)",
                    type="number",
                    required=False,
                    default=50,
                    help_text="仅在'按比例'模式下有效"
                ),
                ToolInputField(
                    name="width",
                    label="宽度 (像素)",
                    type="number",
                    required=False,
                    help_text="在'指定宽度'或'指定宽高'模式下有效"
                ),
                ToolInputField(
                    name="height",
                    label="高度 (像素)",
                    type="number",
                    required=False,
                    help_text="在'指定高度'或'指定宽高'模式下有效"
                )
            ]
        )
    
    def run(self, inputs: Dict[str, Any]) -> ToolExecutionResult:
        logs = []
        
        try:
            image_path = inputs.get("image")
            mode = inputs.get("mode", "按比例")
            
            if not image_path or not Path(image_path).exists():
                return ToolExecutionResult(
                    success=False,
                    error="图片文件不存在",
                    logs=logs
                )
            
            # 打开图片
            img = Image.open(image_path)
            original_size = img.size
            logs.append(f"原始尺寸: {original_size[0]} × {original_size[1]} 像素")
            
            # 计算新尺寸
            if mode == "按比例":
                scale = float(inputs.get("scale", 50)) / 100
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                logs.append(f"缩放比例: {scale * 100}%")
                
            elif mode == "指定宽度":
                width = int(inputs.get("width", original_size[0]))
                ratio = width / original_size[0]
                new_size = (width, int(original_size[1] * ratio))
                logs.append(f"指定宽度: {width} 像素，按比例计算高度")
                
            elif mode == "指定高度":
                height = int(inputs.get("height", original_size[1]))
                ratio = height / original_size[1]
                new_size = (int(original_size[0] * ratio), height)
                logs.append(f"指定高度: {height} 像素，按比例计算宽度")
                
            elif mode == "指定宽高":
                width = int(inputs.get("width", original_size[0]))
                height = int(inputs.get("height", original_size[1]))
                new_size = (width, height)
                logs.append(f"指定尺寸: {width} × {height} 像素（可能变形）")
            
            else:
                return ToolExecutionResult(
                    success=False,
                    error=f"不支持的模式: {mode}",
                    logs=logs
                )
            
            # 缩放图片
            logs.append(f"开始缩放到: {new_size[0]} × {new_size[1]} 像素")
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 保存结果
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            
            timestamp = int(time.time())
            output_filename = f"resized_{timestamp}.png"
            output_path = output_dir / output_filename
            
            resized_img.save(output_path, "PNG")
            logs.append(f"✓ 图片已保存")
            
            return ToolExecutionResult(
                success=True,
                output=f"图片已成功缩放\n原始尺寸: {original_size[0]} × {original_size[1]}\n新尺寸: {new_size[0]} × {new_size[1]}",
                files=[
                    {
                        "name": output_filename,
                        "path": f"/outputs/{output_filename}"
                    }
                ],
                logs=logs
            )
            
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                error=f"处理失败: {str(e)}",
                logs=logs
            )
