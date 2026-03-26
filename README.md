# Korean Study Agent

## 项目介绍
Korean Study Agent 是一个面向韩语学习场景的 AI 学习助手项目。

这个项目的目标，是根据用户的学习记录、错题情况和复习需求，提供更有针对性的学习帮助。当前第一版主要聚焦于三个核心能力：分析错题、推荐复习内容、生成练习题。

项目整体采用前后端分离的轻量结构。前端负责输入学习需求并展示结果，后端负责处理请求、读取学习数据，并生成对应的学习建议与练习内容。后续还可以继续扩展为真正的 Agent 系统，例如接入 tool calling、RAG 知识库、教材问答、学习日志记录、错题追踪等功能。

这个项目既是一个韩语学习工具，也是一个用于练习 AI 应用开发的作品集项目。

---

## 技术栈

### 后端
- Python
- Flask
- SQLite
- python-dotenv

### 前端
- HTML
- CSS
- JavaScript

### AI 相关
- OpenAI API（后续接入）
- Agent / Tool Calling（规划中）

### 开发环境
- macOS
- Python 虚拟环境 `venv`

---

## 如何运行

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd Korean-Agent
