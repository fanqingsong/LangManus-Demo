# Docker 部署指南

本文档介绍如何使用 Docker 和 Docker Compose 部署 LangManus Demo。

## 前置要求

- Docker Engine 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存

## 国内镜像源加速

项目提供了多个使用国内镜像源的 Dockerfile 版本，以加速构建过程：

### 1. 阿里云镜像源（默认）
```bash
# 使用默认的 Dockerfile（已配置阿里云镜像）
docker-compose build
```

### 2. 腾讯云镜像源
```bash
# 使用腾讯云镜像源
docker-compose -f docker-compose.yml build --build-arg DOCKERFILE=Dockerfile.tencent
```

### 3. 网易云镜像源
```bash
# 使用网易云镜像源
docker-compose -f docker-compose.yml build --build-arg DOCKERFILE=Dockerfile.netease
```

### 4. 手动指定镜像源
```bash
# 构建时指定 Dockerfile
docker build -f Dockerfile.tencent -t langmanus-demo .
```

## 快速开始

### 1. 环境配置

首先复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置您的 API 密钥：

```env
# LLM API 配置
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# 可选：GitHub API
GITHUB_TOKEN=your_github_token_here

# 应用配置
DEBUG=False
APP_ENV=production
```

### 2. 构建镜像

```bash
# 使用默认配置（阿里云镜像源）
docker-compose build

# 或使用腾讯云镜像源
docker-compose build --build-arg DOCKERFILE=Dockerfile.tencent
```

### 3. 启动服务

#### 启动 FastAPI 服务（推荐）
```bash
docker-compose up langmanus-api
```

#### 启动 Streamlit Web 界面
```bash
docker-compose up langmanus-web
```

#### 启动开发模式（热重载）
```bash
docker-compose up langmanus-dev
```

#### 运行 CLI 演示
```bash
docker-compose run --rm langmanus-cli
```

#### 运行离线演示（无需 API 密钥）
```bash
docker-compose run --rm langmanus-offline
```

## 服务说明

### langmanus-api
- **端口**: 8000
- **描述**: FastAPI 服务器，提供 REST API 接口
- **用途**: 生产环境部署，API 集成

### langmanus-web
- **端口**: 8501
- **描述**: Streamlit Web 应用界面
- **用途**: 用户友好的 Web 界面

### langmanus-dev
- **端口**: 8000, 8501
- **描述**: 开发模式，支持热重载
- **用途**: 开发和调试

### langmanus-cli
- **描述**: 命令行演示模式
- **用途**: 快速测试和演示

### langmanus-offline
- **描述**: 离线演示模式，无需 API 密钥
- **用途**: 展示框架架构和核心功能

## 常用命令

### 启动所有服务
```bash
docker-compose up -d
```

### 查看服务状态
```bash
docker-compose ps
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs langmanus-api
docker-compose logs -f langmanus-api  # 实时日志
```

### 停止服务
```bash
docker-compose down
```

### 重新构建并启动
```bash
docker-compose up --build
```

### 清理资源
```bash
docker-compose down -v --rmi all
```

## 数据持久化

项目使用以下卷挂载来持久化数据：

- `./output:/app/output` - 输出文件（图表、报告、日志）
- `./assets:/app/assets` - 静态资源文件

## 健康检查

服务包含健康检查机制：

- **FastAPI**: `http://localhost:8000/health`
- **Streamlit**: `http://localhost:8501/_stcore/health`

## 故障排除

### 1. 端口冲突
如果端口被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8001:8000"  # 使用 8001 端口
```

### 2. 内存不足
如果遇到内存不足，可以增加 Docker 内存限制或使用更轻量的配置。

### 3. 权限问题
确保 `output` 目录有正确的权限：

```bash
mkdir -p output
chmod 755 output
```

### 4. 环境变量问题
检查 `.env` 文件是否正确配置，确保所有必需的 API 密钥都已设置。

### 5. 镜像拉取失败
如果遇到镜像拉取问题，可以尝试：

```bash
# 清理 Docker 缓存
docker system prune -f

# 使用不同的镜像源
docker-compose build --build-arg DOCKERFILE=Dockerfile.tencent

# 或手动拉取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/library/python:3.11-slim
```

## 生产环境部署

### 使用 Docker Swarm
```bash
# 初始化 swarm
docker swarm init

# 部署服务
docker stack deploy -c docker-compose.yml langmanus
```

### 使用 Kubernetes
可以使用 `docker-compose.yml` 作为基础创建 Kubernetes 配置文件。

## 性能优化

### 1. 多阶段构建
Dockerfile 使用多阶段构建来减少镜像大小。

### 2. 缓存优化
使用 `.dockerignore` 排除不必要的文件。

### 3. 资源限制
可以在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  langmanus-api:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## 安全考虑

1. **非 root 用户**: 容器以非 root 用户运行
2. **环境变量**: 敏感信息通过环境变量传递
3. **健康检查**: 定期检查服务状态
4. **资源限制**: 防止资源滥用

## 监控和日志

### 查看容器资源使用
```bash
docker stats
```

### 查看详细日志
```bash
docker-compose logs --tail=100 -f
```

### 进入容器调试
```bash
docker-compose exec langmanus-api bash
```

## 更新和升级

### 更新代码
```bash
git pull
docker-compose up --build -d
```

### 更新依赖
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 支持

如果遇到问题，请：

1. 检查日志：`docker-compose logs`
2. 验证环境配置：确保 `.env` 文件正确
3. 检查网络连接：确保能访问外部 API
4. 查看健康状态：访问健康检查端点
5. 尝试不同的镜像源：使用 `Dockerfile.tencent` 或 `Dockerfile.netease`

更多信息请参考项目 README 和官方文档。 