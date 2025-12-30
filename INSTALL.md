# GitHub MCP Server 安装指南

## 🚀 快速开始

### Windows 用户
双击运行 `deploy.bat` 即可一键部署！

### Linux/macOS 用户
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📋 系统要求

- Python 3.10 或更高版本
- Git (可选，用于Git操作功能)
- 网络连接 (访问GitHub API)

## 📦 文件说明

- `github_mcp_server.py` - 主服务器文件
- `requirements.txt` - Python依赖包列表
- `.env.example` - 环境变量配置模板
- `deploy.bat` - Windows一键部署脚本
- `deploy.sh` - Linux/macOS一键部署脚本
- `README.md` - 详细说明文档
- `cursor_mcp_config.json` - Cursor配置示例

## 🔧 手动安装

如果自动部署脚本无法工作，可以手动安装：

### 1. 创建虚拟环境
```bash
# Windows
py -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量 (可选)
```bash
cp .env.example .env
# 编辑 .env 文件，添加 GitHub Token
```

### 4. 测试运行
```bash
python github_mcp_server.py
```

## 🔗 在AI助手中使用

### Cursor
1. 打开设置 → MCP
2. 添加服务器配置：
```json
{
  "mcpServers": {
    "github-mcp": {
      "command": "python",
      "args": ["path/to/github_mcp_server.py"]
    }
  }
}
```

### Claude Desktop
编辑 `claude_desktop_config.json` 文件，添加相同配置。

## ⚡ 功能特性

- 🔍 GitHub仓库和代码搜索
- 🔄 Git操作 (克隆、拉取)
- 📁 文件和仓库下载
- 🔌 GitHub API访问
- 🛡️ 错误处理和重试机制

## 🆘 常见问题

### Q: Python版本不兼容
A: 请确保使用Python 3.10或更高版本

### Q: API限制超出
A: 在GitHub设置中生成Personal Access Token并配置到.env文件

### Q: Git命令失败
A: 确保系统已安装Git并在PATH中

## 📞 支持

如有问题，请查看README.md或提交Issue。