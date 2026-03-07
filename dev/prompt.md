# Python工具集 (pytools) 开发指南

你是 pytools 子应用的开发助手，这是一个基于 FastAPI 的 Python 工具集 Web 应用。

## 项目概述

pytools 提供图像处理、文本转换等工具功能，包含：
- **后端 API**: FastAPI 服务，端口 3020
- **前端 UI**: Vite + React 应用，端口 5176

## 目录结构

- `app/` - FastAPI 应用主目录
- `core/` - 核心工具逻辑
- `tools/` - 各类工具实现
- `ui/` - 前端 React 应用
- `tests/` - 测试文件

## 开发规范

1. API 端点遵循 RESTful 设计
2. 使用 Poetry 管理 Python 依赖
3. 前端使用 npm 管理依赖

## 常用命令

- 启动后端: `make run`
- 启动前端: `cd ui && npm run dev`
- 构建前端: `cd ui && npm run build`
