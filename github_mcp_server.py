#!/usr/bin/env python3
"""
GitHub MCP Server - 为LLM提供GitHub相关功能的MCP服务器
包含：搜索、Git操作、文件下载、API访问四大功能
"""

import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP, Context

# 初始化MCP服务器
mcp = FastMCP("GitHub MCP Server")

# GitHub API配置
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")  # 从环境变量获取GitHub token

# HTTP客户端
http_client = httpx.AsyncClient(
    headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-MCP-Server/1.0"
    }
)
if GITHUB_TOKEN:
    http_client.headers["Authorization"] = f"token {GITHUB_TOKEN}"


# ==================== GitHub搜索工具 ====================

@mcp.tool()
async def search_repositories(query: str, limit: int = 10) -> str:
    """搜索GitHub仓库
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量限制，默认10个
        
    Returns:
        JSON格式的搜索结果
    """
    try:
        params = {"q": query, "per_page": min(limit, 100)}  # GitHub API限制最大100
        response = await http_client.get(f"{GITHUB_API_BASE}/search/repositories", params=params)
        response.raise_for_status()
        
        data = response.json()
        repos = []
        
        for repo in data.get("items", []):
            repos.append({
                "name": repo["full_name"],
                "description": repo.get("description", ""),
                "stars": repo["stargazers_count"],
                "language": repo.get("language", ""),
                "url": repo["html_url"],
                "clone_url": repo["clone_url"],
                "updated_at": repo["updated_at"]
            })
        
        return json.dumps({
            "success": True,
            "count": len(repos),
            "repositories": repos
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
async def search_code(query: str, repo: str = "", language: str = "", limit: int = 10) -> str:
    """搜索GitHub代码
    
    Args:
        query: 搜索关键词
        repo: 限定搜索的仓库（可选）
        language: 编程语言（可选）
        limit: 返回结果数量限制，默认10个
        
    Returns:
        JSON格式的搜索结果
    """
    try:
        # 构建搜索查询
        search_query = query
        if repo:
            search_query += f" repo:{repo}"
        if language:
            search_query += f" language:{language}"
            
        params = {"q": search_query, "per_page": min(limit, 100)}
        response = await http_client.get(f"{GITHUB_API_BASE}/search/code", params=params)
        response.raise_for_status()
        
        data = response.json()
        files = []
        
        for item in data.get("items", []):
            files.append({
                "name": item["name"],
                "path": item["path"],
                "repository": item["repository"]["full_name"],
                "url": item["html_url"],
                "git_url": item["git_url"]
            })
        
        return json.dumps({
            "success": True,
            "count": len(files),
            "files": files
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


# ==================== Git操作工具 ====================

@mcp.tool()
async def clone_repository(repo_url: str, target_dir: str = "", branch: str = "master") -> str:
    """克隆Git仓库
    
    Args:
        repo_url: 仓库URL（支持HTTPS或SSH）
        target_dir: 目标目录，默认使用仓库名
        branch: 分支名，默认main
        
    Returns:
        操作结果信息
    """
    try:
        if not target_dir:
            # 从URL提取仓库名
            repo_name = repo_url.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            target_dir = repo_name
            
        # 检查目录是否已存在
        if Path(target_dir).exists():
            return json.dumps({
                "success": False,
                "error": f"目录 '{target_dir}' 已存在"
            }, ensure_ascii=False, indent=2)
        
        # 执行git clone命令
        cmd = ["git", "clone", "--branch", branch, repo_url, target_dir]
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return json.dumps({
                    "success": True,
                    "message": f"成功克隆仓库到 '{target_dir}'",
                    "directory": str(Path(target_dir).absolute())
                }, ensure_ascii=False, indent=2)
            else:
                error_msg = stderr.decode('utf-8', errors='ignore').strip()
                if not error_msg:
                    error_msg = f"Git命令执行失败，退出码: {process.returncode}"
                return json.dumps({
                    "success": False,
                    "error": f"克隆失败: {error_msg}"
                }, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            return json.dumps({
                "success": False,
                "error": "Git未安装或不在系统PATH中。请先安装Git: https://git-scm.com/"
            }, ensure_ascii=False, indent=2)
            
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
async def pull_repository(repo_dir: str) -> str:
    """拉取仓库最新代码
    
    Args:
        repo_dir: 仓库目录路径
        
    Returns:
        操作结果信息
    """
    try:
        if not Path(repo_dir).exists():
            return json.dumps({
                "success": False,
                "error": f"目录 '{repo_dir}' 不存在"
            }, ensure_ascii=False, indent=2)
        
        # 执行git pull命令
        cmd = ["git", "pull"]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=repo_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return json.dumps({
                "success": True,
                "message": "成功拉取最新代码",
                "output": stdout.decode('utf-8', errors='ignore')
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": stderr.decode('utf-8', errors='ignore')
            }, ensure_ascii=False, indent=2)
            
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


# ==================== 文件下载工具 ====================

@mcp.tool()
async def download_file(download_url: str, save_path: str) -> str:
    """下载文件
    
    Args:
        download_url: 文件下载URL
        save_path: 保存路径
        
    Returns:
        操作结果信息
    """
    try:
        # 确保保存目录存在
        save_dir = Path(save_path).parent
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 下载文件，允许重定向
        response = await http_client.get(download_url, follow_redirects=True)
        response.raise_for_status()
        
        # 保存文件
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return json.dumps({
            "success": True,
            "message": f"文件已下载到 '{save_path}'",
            "size": len(response.content)
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"下载失败: {str(e)}"
        }, ensure_ascii=False, indent=2)


@mcp.tool()
async def download_repository_archive(owner: str, repo: str, ref: str = "master", save_path: str = "") -> str:
    """下载仓库压缩包
    
    Args:
        owner: 仓库所有者
        repo: 仓库名
        ref: 分支或tag，默认master
        save_path: 保存路径，默认为当前目录
        
    Returns:
        操作结果信息
    """
    try:
        if not save_path:
            save_path = f"{repo}-{ref}.zip"
        
        # GitHub codeload URL (更稳定的下载地址)
        archive_url = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{ref}"
        
        return await download_file(archive_url, save_path)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"下载仓库压缩包失败: {str(e)}"
        }, ensure_ascii=False, indent=2)


# ==================== GitHub API访问工具 ====================

@mcp.tool()
async def get_repository_info(owner: str, repo: str) -> str:
    """获取仓库详细信息
    
    Args:
        owner: 仓库所有者
        repo: 仓库名
        
    Returns:
        JSON格式的仓库信息
    """
    try:
        response = await http_client.get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}")
        response.raise_for_status()
        
        data = response.json()
        
        # 提取关键信息
        repo_info = {
            "name": data["full_name"],
            "description": data.get("description", ""),
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "language": data.get("language", ""),
            "license": data.get("license", {}).get("name", "No license") if data.get("license") else "No license",
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "size": data["size"],
            "default_branch": data["default_branch"],
            "open_issues": data["open_issues_count"],
            "url": data["html_url"],
            "clone_url": data["clone_url"],
            "topics": data.get("topics", [])
        }
        
        return json.dumps({
            "success": True,
            "repository": repo_info
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_repository_contents(owner: str, repo: str, path: str = "", ref: str = "master") -> str:
    """获取仓库文件内容列表
    
    Args:
        owner: 仓库所有者
        repo: 仓库名
        path: 路径，默认为根目录
        ref: 分支或tag，默认main
        
    Returns:
        JSON格式的文件列表
    """
    try:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
        if ref:
            url += f"?ref={ref}"
            
        response = await http_client.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, list):
            # 目录内容
            contents = []
            for item in data:
                contents.append({
                    "name": item["name"],
                    "type": item["type"],
                    "path": item["path"],
                    "size": item.get("size", 0),
                    "url": item["html_url"]
                })
        else:
            # 单个文件
            contents = [{
                "name": data["name"],
                "type": data["type"],
                "path": data["path"],
                "size": data.get("size", 0),
                "url": data["html_url"],
                "download_url": data.get("download_url", "")
            }]
        
        return json.dumps({
            "success": True,
            "contents": contents
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


# ==================== 资源定义 ====================

@mcp.resource("github://help")
def get_help() -> str:
    """获取GitHub MCP服务器使用帮助"""
    return """
# GitHub MCP Server 使用指南

## 可用工具：

### GitHub搜索工具
- `search_repositories`: 搜索GitHub仓库
- `search_code`: 搜索GitHub代码

### Git操作工具
- `clone_repository`: 克隆Git仓库
- `pull_repository`: 拉取最新代码

### 文件下载工具
- `download_file`: 下载单个文件
- `download_repository_archive`: 下载仓库压缩包

### GitHub API访问工具
- `get_repository_info`: 获取仓库详细信息
- `get_repository_contents`: 获取仓库文件列表

## 使用示例：
1. 搜索仓库：`search_repositories("python machine learning", 5)`
2. 克隆仓库：`clone_repository("https://github.com/user/repo.git")`
3. 获取仓库信息：`get_repository_info("torvalds", "linux")`

## 环境变量：
- `GITHUB_TOKEN`: GitHub个人访问令牌（可选，用于提高API限制）
"""


# ==================== 主程序入口 ====================

async def cleanup():
    """清理资源"""
    await http_client.aclose()

if __name__ == "__main__":
    try:
        # 运行MCP服务器
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("服务器正在关闭...")
    finally:
        # 确保清理资源
        asyncio.run(cleanup())