#!/usr/bin/env python3
"""
Docker 配置文件验证脚本
验证 Dockerfile 和 docker-compose.yml 的语法和配置
"""

import yaml
import os
import sys

def test_dockerfile():
    """测试 Dockerfile 语法"""
    print("🔍 检查 Dockerfile...")
    
    if not os.path.exists("Dockerfile"):
        print("❌ Dockerfile 不存在")
        return False
    
    try:
        with open("Dockerfile", "r") as f:
            content = f.read()
        
        # 基本检查
        required_commands = [
            "FROM",
            "WORKDIR",
            "COPY",
            "CMD"
        ]
        
        for cmd in required_commands:
            if cmd not in content:
                print(f"❌ 缺少必要的 Docker 命令: {cmd}")
                return False
        
        print("✅ Dockerfile 语法检查通过")
        return True
        
    except Exception as e:
        print(f"❌ Dockerfile 检查失败: {e}")
        return False

def test_docker_compose():
    """测试 docker-compose.yml 语法"""
    print("🔍 检查 docker-compose.yml...")
    
    if not os.path.exists("docker-compose.yml"):
        print("❌ docker-compose.yml 不存在")
        return False
    
    try:
        with open("docker-compose.yml", "r") as f:
            config = yaml.safe_load(f)
        
        # 检查基本结构
        if "version" not in config:
            print("❌ 缺少 version 字段")
            return False
        
        if "services" not in config:
            print("❌ 缺少 services 字段")
            return False
        
        # 检查服务配置
        services = config["services"]
        required_services = ["langmanus-api", "langmanus-web"]
        
        for service in required_services:
            if service not in services:
                print(f"❌ 缺少服务: {service}")
                return False
        
        print("✅ docker-compose.yml 语法检查通过")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML 语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ docker-compose.yml 检查失败: {e}")
        return False

def test_dockerignore():
    """测试 .dockerignore 文件"""
    print("🔍 检查 .dockerignore...")
    
    if not os.path.exists(".dockerignore"):
        print("❌ .dockerignore 不存在")
        return False
    
    try:
        with open(".dockerignore", "r") as f:
            content = f.read()
        
        # 检查是否包含重要排除项
        important_excludes = [
            ".git",
            "__pycache__",
            ".env",
            ".venv"
        ]
        
        for exclude in important_excludes:
            if exclude not in content:
                print(f"⚠️  建议在 .dockerignore 中包含: {exclude}")
        
        print("✅ .dockerignore 检查通过")
        return True
        
    except Exception as e:
        print(f"❌ .dockerignore 检查失败: {e}")
        return False

def test_env_example():
    """测试环境变量模板"""
    print("🔍 检查 .env.example...")
    
    if not os.path.exists(".env.example"):
        print("❌ .env.example 不存在")
        return False
    
    try:
        with open(".env.example", "r") as f:
            content = f.read()
        
        # 检查是否包含必要的环境变量
        required_vars = [
            "OPENAI_API_KEY",
            "TAVILY_API_KEY"
        ]
        
        for var in required_vars:
            if var not in content:
                print(f"⚠️  建议在 .env.example 中包含: {var}")
        
        print("✅ .env.example 检查通过")
        return True
        
    except Exception as e:
        print(f"❌ .env.example 检查失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🚀 === Docker 配置验证 ===")
    print()
    
    results = []
    
    # 运行所有测试
    results.append(test_dockerfile())
    results.append(test_docker_compose())
    results.append(test_dockerignore())
    results.append(test_env_example())
    
    print()
    print("📊 === 测试结果 ===")
    
    if all(results):
        print("🎉 所有 Docker 配置检查通过！")
        print()
        print("💡 使用说明:")
        print("   1. 确保已安装 Docker 和 Docker Compose")
        print("   2. 配置 .env 文件中的 API 密钥")
        print("   3. 运行: docker-compose up -d")
        print("   4. 访问: http://localhost:8000 (API) 或 http://localhost:8501 (Web)")
    else:
        print("❌ 部分配置检查失败，请查看上述错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main() 