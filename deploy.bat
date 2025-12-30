@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    GitHub MCP Server 一键部署脚本
echo ========================================
echo.

REM 检查Python环境
echo [1/5] 检查Python环境...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.10或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境检查通过

REM 创建虚拟环境
echo.
echo [2/5] 创建虚拟环境...
if exist venv (
    echo ℹ️  虚拟环境已存在，跳过创建
) else (
    py -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

REM 激活虚拟环境并安装依赖
echo.
echo [3/5] 安装依赖包...
call venv\Scripts\activate.bat
py -m pip install --upgrade pip >nul 2>&1
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

REM 创建环境配置文件
echo.
echo [4/5] 配置环境...
if not exist .env (
    copy .env.example .env >nul 2>&1
    echo ✅ 已创建.env配置文件
    echo ℹ️  请编辑.env文件添加你的GitHub Token (可选)
    echo    获取Token: https://github.com/settings/tokens
) else (
    echo ℹ️  .env配置文件已存在
)

REM 测试MCP服务器
echo.
echo [5/5] 测试MCP服务器...
echo ℹ️  启动测试中，请稍候...

REM 创建测试脚本
echo import asyncio > test_mcp.py
echo import json >> test_mcp.py
echo from github_mcp_server import search_repositories >> test_mcp.py
echo. >> test_mcp.py
echo async def test(): >> test_mcp.py
echo     try: >> test_mcp.py
echo         result = await search_repositories("python", 2) >> test_mcp.py
echo         data = json.loads(result) >> test_mcp.py
echo         if data["success"]: >> test_mcp.py
echo             print("✅ MCP服务器测试成功!") >> test_mcp.py
echo             print(f"找到 {data['count']} 个仓库") >> test_mcp.py
echo         else: >> test_mcp.py
echo             print("❌ MCP服务器测试失败") >> test_mcp.py
echo     except Exception as e: >> test_mcp.py
echo         print(f"❌ 测试出错: {e}") >> test_mcp.py
echo. >> test_mcp.py
echo asyncio.run(test()) >> test_mcp.py

py test_mcp.py
del test_mcp.py

echo.
echo ========================================
echo           部署完成！
echo ========================================
echo.
echo 📋 使用方法:
echo    1. 启动MCP服务器: py github_mcp_server.py
echo    2. 在AI助手中配置MCP服务器
echo    3. 开始使用GitHub功能!
echo.
echo 📖 更多信息请查看 README.md
echo.
pause