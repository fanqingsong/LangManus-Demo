# LangManus Demo Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Build stage
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# # Configure apt sources with Chinese mirrors for faster installation
# RUN rm -f /etc/apt/sources.list.d/* && \
#     echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management with Chinese mirror
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ uv

# Copy dependency files
COPY pyproject.toml uv.lock requirements.txt ./

# Install dependencies using pip with Chinese mirror (fallback from uv)
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# Stage 2: Production stage
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -r langmanus && useradd -r -g langmanus langmanus

# Set working directory
WORKDIR /app

# # Configure apt sources with Chinese mirrors for faster installation
# RUN rm -f /etc/apt/sources.list.d/* && \
#     echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list

# # Install runtime dependencies
# RUN apt-get update && apt-get install -y \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p output/charts output/logs output/reports && \
    mkdir -p /home/langmanus/.config /home/langmanus/.streamlit && \
    chown -R langmanus:langmanus /app && \
    chown -R langmanus:langmanus /home/langmanus

# Switch to non-root user
USER langmanus

# Set home directory for the user
ENV HOME=/home/langmanus

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "server.py"] 