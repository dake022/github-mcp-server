#!/bin/bash

echo
echo "========================================"
echo "   GitHub MCP Server 一键部署脚本"
echo "========================================"
echo

# 检查Python环境
echo "[1/5] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.10或更高版本"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python环境检查通过"

# 创建虚拟环境
echo
echo "[2/5] 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "ℹ️  虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 创建虚拟环境失败"
        exit 1
    fi
    echo "✅ 虚拟环境创建成功"
fi

# 激活虚拟环境并安装依赖
echo
echo "[3/5] 安装依赖包..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装完成"

# 创建环境配置文件
echo
echo "[4/5] 配置环境..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ 已创建.env配置文件"
    echo "ℹ️  请编辑.env文件添加你的GitHub Token (可选)"
    echo "   获取Token: https://github.com/settings/tokens"
else
    echo "ℹ️  .env配置文件已存在"
fi

# 测试MCP服务器
echo
echo "[5/5] 测试MCP服务器..."
echo "ℹ️  启动测试中，请稍候..."

# 创建测试脚本
cat > test_mcp.py << 'EOF'
import asyncio
import json
from github_mcp_server import search_repositories

async def test():
    try:
        result = await search_repositories("python", 2)
        data = json.loads(result)
        if data["success"]:
            print("✅ MCP服务器测试成功!")
            print(f"找到 {data['count']} 个仓库")
        else:
            print("❌ MCP服务器测试失败")
    except Exception as e:
        print(f"❌ 测试出错: {e}")

asyncio.run(test())
EOF

python3 test_mcp.py
rm test_mcp.py

echo
echo "========================================"
echo "           部署完成！"
echo "========================================"
echo
echo "📋 使用方法:"
echo "   1. 启动MCP服务器: python3 github_mcp_server.py"
echo "   2. 在AI助手中配置MCP服务器"
echo "   3. 开始使用GitHub功能!"
echo
echo "📖 更多信息请查看 README.md"
echo