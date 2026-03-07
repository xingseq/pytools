# PyTools - 图像处理与文本转换工具集

PyTools 是一个基于 Web 的图像处理和文本转换工具集，提供图像缩放、图片切分、文本转换等实用功能，通过直观的 Web 界面轻松处理图像和文本任务。

## ✨ 功能特性

### 🖼️ 图像处理工具
- **图像缩放**: 调整图片尺寸，支持按比例缩放或指定宽高
- **图片切分**: 将大图片按行列数或固定尺寸切分成多个小图片
- **多格式支持**: 支持 JPG、PNG、GIF 等常见图像格式
- **批量输出**: 自动打包处理结果，方便下载

### 📝 文本转换工具
- **大小写转换**: 文本转大写或转小写
- **文本反转**: 反转文本字符顺序
- **空格处理**: 去除文本中所有空格
- **字数统计**: 统计字符数、单词数和行数

### 🎯 设计优势
- **现代化界面**: 直观的 React + Tailwind CSS 界面
- **流式处理**: 支持实时进度反馈和日志输出
- **文件管理**: 自动管理上传文件和处理结果
- **历史记录**: 保存执行历史，方便追溯

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 18+
- 星序引擎运行环境

### 安装与启动

1. **确保项目位于正确位置**
   ```
   ~/Library/Application Support/xingseq/projects/pytools/
   ```

2. **安装 Python 依赖**
   ```bash
   cd "/Users/ws/Library/Application Support/xingseq/projects/pytools"
   poetry install
   ```

3. **安装前端依赖**
   ```bash
   cd ui
   npm install
   ```

4. **启动应用**
   - 通过星序引擎主界面启动
   - 或手动启动：
     ```bash
     # 启动后端 API (端口 3020)
     make run
     
     # 在另一个终端启动前端 UI (端口 5176)
     cd ui
     npm run subapp
     ```

5. **访问界面**
   - 打开浏览器访问: `http://localhost:5176`
   - 或通过星序引擎主界面访问

## 📁 项目结构

```
pytools/
├── app/                          # 后端应用
│   ├── api.py                   # FastAPI 路由
│   ├── main.py                  # 应用入口
│   └── templates/               # HTML 模板
├── core/                        # 核心模块
│   ├── base_tool.py            # 工具基类
│   ├── executor.py             # 工具执行器
│   ├── registry.py             # 工具注册表
│   └── schemas.py              # 数据模型
├── tools/                       # 工具实现
│   ├── image_resize/           # 图像缩放工具
│   ├── image_split/            # 图片切分工具
│   └── text_transform/         # 文本转换工具
├── ui/                          # 前端界面
│   ├── src/App.jsx             # 主 React 组件
│   ├── src/main.jsx            # React 入口
│   ├── src/index.css           # 全局样式
│   └── vite.config.js          # Vite 配置
├── uploads/                     # 上传文件目录
├── outputs/                     # 输出文件目录
├── sub-app-manifest.json       # 子应用配置
├── pyproject.toml              # Python 项目配置
├── package.json                # Node.js 项目配置
└── README.md                   # 项目说明
```

## 🔧 工具使用指南

### 图像缩放工具

1. **上传图片**: 选择要缩放的图像文件
2. **选择缩放模式**:
   - 按比例: 输入缩放百分比
   - 指定宽度: 设置目标宽度，高度按比例计算
   - 指定高度: 设置目标高度，宽度按比例计算
   - 指定宽高: 同时设置宽度和高度（可能变形）
3. **执行处理**: 点击执行按钮，等待处理完成
4. **下载结果**: 处理后的图片会自动保存到输出目录

### 图片切分工具

1. **上传图片**: 选择要切分的图像文件
2. **选择切分方式**:
   - 按行列数切分: 指定行数和列数
   - 按固定尺寸切分: 指定每个切片的宽度和高度
3. **设置输出格式**: 选择 PNG、JPG 或与原图相同
4. **执行处理**: 点击执行按钮，等待处理完成
5. **下载结果**: 所有切片会打包成 ZIP 文件供下载

### 文本转换工具

1. **输入文本**: 在文本框中输入或粘贴要处理的文本
2. **选择操作类型**:
   - 转大写: 将所有字符转换为大写
   - 转小写: 将所有字符转换为小写
   - 反转: 反转文本字符顺序
   - 去除空格: 删除所有空格、换行和制表符
   - 统计字数: 统计字符数、单词数和行数
3. **执行处理**: 点击执行按钮，立即查看转换结果

## 🔌 API 接口

### 工具执行接口
```
POST /api/tool/{tool_id}/execute
```

**支持的工具 ID**:
- `image_resize` - 图像缩放
- `image_split` - 图片切分
- `text_transform` - 文本转换

**请求格式**: `multipart/form-data`

**响应格式**: Server-Sent Events (SSE) 流式响应

### 历史记录接口
```
GET /api/history
```
获取执行历史记录

## 🛠️ 开发指南

### 添加新工具

1. **创建工具目录**
   ```bash
   mkdir -p tools/new_tool
   ```

2. **实现工具类** (`tools/new_tool/tool.py`)
   ```python
   from core.base_tool import BaseTool
   from core.schemas import ToolMetadata, ToolInputField
   
   class NewTool(BaseTool):
       def get_metadata(self):
           return ToolMetadata(
               id="new_tool",
               name="新工具",
               description="工具描述",
               category="工具类别",
               input_fields=[
                   ToolInputField(
                       name="input_field",
                       label="输入字段",
                       type="text",
                       required=True
                   )
               ]
           )
       
       def run(self, inputs):
           # 工具逻辑实现
           pass
   ```

3. **自动注册**
   - 工具会自动被注册表发现和注册
   - 无需手动配置

### 前端开发

1. **开发模式**
   ```bash
   cd ui
   npm run dev
   ```

2. **构建生产版本**
   ```bash
   cd ui
   npm run build
   ```

3. **添加新工具到前端**
   - 在 `ui/src/App.jsx` 的 `tools` 数组中添加新工具配置
   - 定义输入字段和验证规则
   - 更新界面布局

## 🌐 技术架构

### 后端技术栈
- **FastAPI**: 高性能 Python Web 框架
- **PIL/Pillow**: 图像处理库
- **Poetry**: Python 依赖管理
- **SQLite**: 轻量级数据库（用于历史记录）

### 前端技术栈
- **React 18**: 现代前端框架
- **Vite**: 快速构建工具
- **Tailwind CSS**: 实用优先的 CSS 框架
- **Lucide React**: 精美的图标库

### 通信协议
- **RESTful API**: 标准 HTTP 接口
- **Server-Sent Events**: 实时流式输出
- **WebSocket**: 实时双向通信（预留）

## 🐛 故障排除

### 常见问题

1. **图像处理失败**
   ```
   确保已安装 Pillow 库: poetry install
   检查上传的文件格式是否支持
   验证文件大小是否在限制范围内
   ```

2. **API 连接错误**
   ```
   检查后端服务是否运行: 端口 3020
   查看前端代理配置是否正确
   检查跨域设置（如果需要）
   ```

3. **文件上传问题**
   ```
   检查 uploads/ 目录权限
   验证文件大小限制
   确保网络连接正常
   ```

### 日志查看

```bash
# 查看后端日志
tail -f logs/app.log

# 查看前端控制台
# 在浏览器中按 F12 打开开发者工具
```

## 📄 许可证

MIT License

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

### 贡献流程
1. Fork 项目仓库
2. 创建功能分支
3. 提交代码更改
4. 添加测试用例
5. 更新相关文档
6. 创建 Pull Request

### 开发规范
- 遵循 Python PEP 8 代码风格
- 使用 TypeScript 类型定义（前端）
- 添加必要的注释和文档
- 确保向后兼容性

## 📞 支持与反馈

- **问题报告**: 提交 GitHub Issue
- **功能建议**: 参与 GitHub Discussions
- **贡献代码**: 提交 Pull Request
- **文档改进**: 直接修改文档并提交

---

**PyTools** - 让图像处理和文本转换更简单、更高效！