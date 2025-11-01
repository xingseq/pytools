from typing import Any, Dict
from pathlib import Path
from PIL import Image
import math
import time
import zipfile

from core.base_tool import BaseTool
from core.schemas import ToolMetadata, ToolInputField, ToolExecutionResult


class ImageSplitTool(BaseTool):
    """图片切分工具"""
    
    def get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            id="image_split",
            name="图片切分",
            description="将大图片按指定方式切分成多个小图片",
            category="图像处理",
            icon="✂️",
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
                    name="split_method",
                    label="切分方式",
                    type="select",
                    required=True,
                    options=["按行列数切分", "按固定尺寸切分"],
                    default="按行列数切分",
                    help_text="选择切分方式"
                ),
                ToolInputField(
                    name="rows",
                    label="行数",
                    type="number",
                    required=False,
                    default=2,
                    help_text="在'按行列数切分'模式下有效"
                ),
                ToolInputField(
                    name="cols",
                    label="列数",
                    type="number",
                    required=False,
                    default=2,
                    help_text="在'按行列数切分'模式下有效"
                ),
                ToolInputField(
                    name="slice_width",
                    label="切片宽度(像素)",
                    type="number",
                    required=False,
                    help_text="在'按固定尺寸切分'模式下有效"
                ),
                ToolInputField(
                    name="slice_height",
                    label="切片高度(像素)",
                    type="number",
                    required=False,
                    help_text="在'按固定尺寸切分'模式下有效"
                ),
                ToolInputField(
                    name="output_format",
                    label="输出格式",
                    type="select",
                    required=True,
                    options=["PNG", "JPG", "与原图相同"],
                    default="PNG",
                    help_text="选择切分后的图片格式"
                )
            ]
        )
    
    def run(self, inputs: Dict[str, Any]) -> ToolExecutionResult:
        logs = []
        
        try:
            image_path = inputs.get("image")
            split_method = inputs.get("split_method", "按行列数切分")
            output_format = inputs.get("output_format", "PNG")
            
            # 处理文件路径 - 确保使用绝对路径
            if not image_path:
                return ToolExecutionResult(
                    success=False,
                    error="请选择要切分的图片文件",
                    logs=logs
                )
            
            image_path = Path(image_path)
            if not image_path.is_absolute():
                # 如果是相对路径，转换为绝对路径
                image_path = Path.cwd() / image_path
            
            if not image_path.exists():
                logs.append(f"文件路径: {image_path}")
                logs.append(f"文件是否存在: {image_path.exists()}")
                return ToolExecutionResult(
                    success=False,
                    error=f"图片文件不存在: {image_path}",
                    logs=logs
                )
            
            # 打开图片
            img = Image.open(image_path)
            original_size = img.size
            logs.append(f"原始图片尺寸: {original_size[0]} × {original_size[1]} 像素")
            
            # 确定输出格式
            if output_format == "与原图相同":
                output_format = img.format if img.format else "PNG"
            
            # 计算切分参数
            if split_method == "按行列数切分":
                rows = int(inputs.get("rows", 2))
                cols = int(inputs.get("cols", 2))
                slice_width = original_size[0] // cols
                slice_height = original_size[1] // rows
                logs.append(f"切分方式: {rows}行 × {cols}列")
                
            else:  # 按固定尺寸切分
                slice_width = int(inputs.get("slice_width", 500))
                slice_height = int(inputs.get("slice_height", 500))
                rows = math.ceil(original_size[1] / slice_height)
                cols = math.ceil(original_size[0] / slice_width)
                logs.append(f"切分方式: 固定尺寸 {slice_width} × {slice_height} 像素")
            
            logs.append(f"将切分为: {rows}行 × {cols}列 = {rows * cols}个切片")
            logs.append(f"每个切片尺寸: {slice_width} × {slice_height} 像素")
            
            # 执行切分
            split_images = []
            for row in range(rows):
                for col in range(cols):
                    # 计算每个切片的坐标
                    left = col * slice_width
                    upper = row * slice_height
                    right = min((col + 1) * slice_width, original_size[0])
                    lower = min((row + 1) * slice_height, original_size[1])
                    
                    # 切分图片
                    slice_img = img.crop((left, upper, right, lower))
                    split_images.append((slice_img, row, col))
            
            logs.append(f"✓ 成功切分 {len(split_images)} 个图片切片")
            
            # 保存结果
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            
            timestamp = int(time.time())
            zip_filename = f"split_images_{timestamp}.zip"
            zip_path = output_dir / zip_filename
            
            # 创建ZIP文件
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for img_slice, row, col in split_images:
                    # 保存单个切片
                    slice_filename = f"slice_{row+1}_{col+1}.{output_format.lower()}"
                    slice_path = output_dir / slice_filename
                    img_slice.save(slice_path, output_format)
                    
                    # 添加到ZIP
                    zip_file.write(slice_path, slice_filename)
            
            logs.append(f"✓ 所有切片已打包到 {zip_filename}")
            
            return ToolExecutionResult(
                success=True,
                output=f"图片切分完成！\\n共生成 {len(split_images)} 个切片\\n打包文件: {zip_filename}",
                files=[
                    {
                        "name": zip_filename,
                        "path": f"/outputs/{zip_filename}"
                    }
                ],
                logs=logs
            )
            
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                error=f"图片切分失败: {str(e)}",
                logs=logs
            )