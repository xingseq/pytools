# PyTools - Python 开发工具集

PyTools 是一个集成化的 Python 开发工具集，提供代码格式化、检查、依赖管理、虚拟环境管理等核心功能，支持 CLI 命令行工具和 Web UI 界面两种使用方式。

## ✨ 功能特性

### 🔧 核心功能
- **代码格式化**: 支持 black 和 autopep8 格式化工具
- **代码检查**: 支持 pylint 和 flake8 代码质量检查
- **依赖管理**: 安装、更新、卸载 Python 包，查看已安装包列表
- **虚拟环境管理**: 创建、激活、删除、列出虚拟环境
- **脚本执行**: 执行 Python 脚本并传递参数

### 🎯 设计优势
- **双模式支持**: CLI 命令行工具 + Web UI 界面
- **开箱即用**: 无需复杂配置，安装即可使用
- **跨平台**: 支持 macOS、Linux、Windows 系统
- **易于扩展**: 模块化设计，方便添加新功能

## 🚀 快速开始

### 安装

1. **确保已安装 Python 3.7+ 和相关工具**
   ```bash
   # 安装 Python 工具
   pip install black autopep8 pylint flake8
   ```

2. **PyTools 会自动被星序引擎扫描注册**
   - 放置到 `~/Library/Application Support/xingseq/projects/pytools/`
   - 重启星序引擎或刷新子应用列表

### CLI 使用

```bash
# 查看帮助
pytools --help

# 格式化代码
pytools format ./src/main.py
pytools format ./src/ --formatter autopep8

# 代码检查
pytools lint ./src/main.py
pytools lint ./src/ --linter flake8

# 依赖管理
pytools deps list
pytools deps install numpy
pytools deps update pip

# 虚拟环境管理
pytools venv create myenv
pytools venv list

# 执行脚本
pytools run ./scripts/main.py
pytools run ./scripts/main.py "arg1 arg2"
```

### Web UI 使用

1. **启动 UI 界面**
   ```bash
   cd ~/Library/Application\ Support/xingseq/projects/pytools/ui
   npm install
   npm run subapp
   ```

2. **访问界面**
   - 打开浏览器访问: `http://localhost:5176`
   - 或通过星序引擎主界面访问

## 📁 项目结构

```
pytools/
├── bin/                          # CLI 命令行入口
│   └── pytools.js               # 主 CLI 脚本
├── lib/                          # API 模块
│   └── index.js                 # 库模块入口
├── ui/                           # Web 界面模块
│   ├── index.html              # HTML 入口
│   ├── package.json            # UI 依赖配置
│   ├── vite.config.js          # Vite 配置
│   ├── tailwind.config.js      # Tailwind 配置
│   ├── postcss.config.js       # PostCSS 配置
│   ├── src/
│   │   ├── App.jsx             # 主 React 组件
│   │   ├── main.jsx            # React 入口
│   │   └── index.css           # 全局样式
│   └── public/                 # 静态资源
├── doc/                         # 文档
│   └── 开发文档/               # 开发文档
├── templates/                   # 模板文件
├── sub-app-manifest.json       # 子应用清单
├── package.json                # 主项目配置
└── README.md                   # 项目说明
```

## 🔌 子应用配置

### sub-app-manifest.json 关键配置

```json
{
  "name": "pytools",
  "displayName": "Python 工具集",
  "version": "1.0.0",
  "description": "Python 开发工具集",
  
  "cli": {
    "enabled": true,
    "bin": "./bin/pytools.js",
    "commands": {
      "format": "格式化 Python 代码",
      "lint": "检查 Python 代码质量",
      "deps": "管理 Python 项目依赖",
      "venv": "管理 Python 虚拟环境",
      "run": "执行 Python 脚本"
    }
  },
  
  "ui": {
    "enabled": true,
    "entry": "./ui/dist/index.html",
    "port": 5176
  }
}
```

## 🛠️ 开发指南

### 环境要求
- Node.js 18+
- Python 3.7+
- npm 或 yarn

### 开发流程

1. **安装依赖**
   ```bash
   cd ~/Library/Application\ Support/xingseq/projects/pytools
   npm install
   
   cd ui
   npm install
   ```

2. **开发模式**
   ```bash
   # CLI 开发测试
   node bin/pytools.js format ./example.py
   
   # UI 开发模式
   cd ui
   npm run dev
   ```

3. **构建部署**
   ```bash
   # 构建 UI
   cd ui
   npm run build
   
   # 安装 CLI 全局命令（可选）
   npm link
   ```

### 添加新功能

1. **添加 CLI 命令**
   - 在 `bin/pytools.js` 中添加新的命令处理器
   - 更新 `sub-app-manifest.json` 中的 commands 配置

2. **添加 UI 功能**
   - 在 `ui/src/App.jsx` 中添加新的标签页和组件
   - 更新状态管理和 API 调用

## 📦 依赖说明

### 主项目依赖
- `commander`: CLI 参数解析
- `chalk`: 终端颜色输出
- `execa`: 子进程执行

### UI 依赖
- `react`: UI 框架
- `vite`: 构建工具
- `tailwindcss`: CSS 框架
- `lucide-react`: 图标库

## 🌐 集成与扩展

### 集成其他工具
- **测试框架**: 集成 pytest/unittest
- **文档生成**: 集成 pydoc/Sphinx
- **性能分析**: 集成 cProfile/py-spy
- **安全扫描**: 集成 bandit/safety

### API 扩展
```javascript
// 使用 lib/index.js 中的 API
import pytools from './lib/index.js';

// 格式化代码
await pytools.format.black('./src/main.py');

// 检查代码质量
await pytools.lint.pylint('./src/main.py');
```

## 🐛 故障排除

### 常见问题

1. **Python 命令找不到**
   ```
   确保 Python 3.7+ 已安装并添加到 PATH
   ```

2. **格式化工具不可用**
   ```
   安装所需工具: pip install black autopep8
   ```

3. **UI 无法启动**
   ```
   检查端口 5176 是否被占用
   检查 ui/node_modules 是否安装完整
   ```

### 调试模式
```bash
# 启用调试日志
export DEBUG=pytools*
pytools format ./test.py

# 查看详细错误
pytools --verbose <command>
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 开发规范
- 使用 ESLint 进行代码检查
- 遵循 Conventional Commits 提交规范
- 添加相应的测试用例
- 更新文档和示例

## 📄 许可证

MIT License

## 📞 支持与反馈

- 问题报告: GitHub Issues
- 功能建议: GitHub Discussions
- 文档更新: Pull Request

---

**PyTools** - 让 Python 开发更高效、更简单！