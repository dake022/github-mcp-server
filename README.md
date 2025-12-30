# GitHub MCP Server

一个功能强大的GitHub MCP服务器，为大语言模型提供完整的GitHub操作功能。

## 功能特性

### 🔍 GitHub搜索工具
- **仓库搜索**: 根据关键词搜索GitHub仓库
- **代码搜索**: 在GitHub上搜索特定代码片段

### 🔄 Git操作工具
- **仓库克隆**: 克隆远程仓库到本地
- **代码拉取**: 更新本地仓库到最新版本

### 📁 文件下载工具
- **单文件下载**: 下载指定文件
- **仓库压缩包下载**: 下载整个仓库的压缩包

### 🔌 GitHub API访问工具
- **仓库信息获取**: 获取仓库的详细信息
- **文件列表获取**: 获取仓库目录结构

## 安装和配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置GitHub Token（可选）
设置环境变量以提高API限制：
```bash
# Windows
set GITHUB_TOKEN=your_github_token_here

# Linux/Mac
export GITHUB_TOKEN=your_github_token_here
```

### 3. 运行服务器
```bash
python github_mcp_server.py
```

## 工具使用说明

### 搜索工具

#### `search_repositories`
搜索GitHub仓库：
```python
# 搜索与Python机器学习相关的仓库
search_repositories("python machine learning", limit=10)
```

#### `search_code`
搜索GitHub代码：
```python
# 在特定仓库中搜索代码
search_code("neural network", repo="tensorflow/tensorflow", language="python")
```

### Git操作工具

#### `clone_repository`
克隆仓库：
```python
# 克隆仓库到指定目录
clone_repository("https://github.com/user/repo.git", target_dir="my-repo", branch="main")
```

#### `pull_repository`
拉取最新代码：
```python
# 更新本地仓库
pull_repository("path/to/repo")
```

### 文件下载工具

#### `download_file`
下载单个文件：
```python
# 下载文件到指定位置
download_file("https://raw.githubusercontent.com/user/repo/main/file.py", "downloads/file.py")
```

#### `download_repository_archive`
下载仓库压缩包：
```python
# 下载整个仓库的压缩包
download_repository_archive("owner", "repo", ref="main", save_path="repo.zip")
```

### GitHub API工具

#### `get_repository_info`
获取仓库信息：
```python
# 获取仓库详细信息
get_repository_info("torvalds", "linux")
```

#### `get_repository_contents`
获取仓库文件列表：
```python
# 获取仓库根目录内容
get_repository_contents("owner", "repo", path="", ref="main")
```

## 在Cursor中配置

1. 打开Cursor设置 → MCP
2. 添加新的MCP服务器：
```json
{
    "mcpServers": {
        "github-mcp": {
            "command": "python",
            "args": ["D:/one/AIworker/test2/github_mcp_server.py"]
        }
    }
}
```

## 开发和测试

### 开发模式
使用MCP开发工具进行测试：
```bash
mcp dev github_mcp_server.py
```

### 单元测试
```bash
pytest tests/
```

### 代码格式化
```bash
black github_mcp_server.py
```

### 类型检查
```bash
mypy github_mcp_server.py
```

## API限制说明

- 未认证用户：每小时60次请求
- 认证用户：每小时5000次请求
- 搜索API：每分钟最多10次请求

建议设置GitHub Token以提高API限制。

## 安全注意事项

- 不要在代码中硬编码GitHub Token
- 使用环境变量管理敏感信息
- 定期轮换API Token
- 遵守GitHub API使用条款

## 故障排除

### 常见问题

1. **API限制超出**
   - 解决方案：设置GitHub Token或等待限制重置

2. **Git命令失败**
   - 解决方案：确保系统已安装Git且在PATH中

3. **网络连接问题**
   - 解决方案：检查网络连接和防火墙设置

4. **权限问题**
   - 解决方案：确保有足够的文件系统权限

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 实现四大核心功能
- 支持GitHub API v3
- 包含完整的错误处理