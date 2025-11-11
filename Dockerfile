# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 先复制项目文件（包括 JMComic-Crawler-Python）
COPY . .

# 安装 Python 依赖（现在 JMComic-Crawler-Python 已经存在）
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p downloads temp logs

# 暴露端口（虽然 Telegram Bot 不需要，但 Railway 可能需要）
EXPOSE 8080

# 启动命令
CMD ["python", "telegram_bot.py"]
