#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 配置文件
"""
import os
from pathlib import Path

class TelegramConfig:
    """Telegram 机器人配置"""

    # ============ Telegram Bot 配置 ============
    # 从 @BotFather 获取你的 Bot Token
    # 优先使用环境变量，如果没有则使用硬编码的值（本地开发）
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8226987850:AAE-RYMD84QgFnlFKH7t7W5nvz_w4ytiNoc")

    # 授权用户的 Telegram ID 列表
    # 获取方式：发送消息给 @userinfobot
    # 空列表 = 允许所有用户使用（公开模式）
    ALLOWED_USERS = []  # 公开给所有人使用

    # ============ 下载配置 ============
    # 下载目录
    DOWNLOAD_DIR = Path(__file__).parent / "downloads"

    # 临时文件目录
    TEMP_DIR = Path(__file__).parent / "temp"

    # 默认下载格式 (pdf, zip, images)
    DEFAULT_FORMAT = "pdf"

    # 是否自动清理临时文件
    AUTO_CLEANUP = True

    # ============ 文件限制 ============
    # 最大文件大小 (MB) - Telegram 普通 Bot 限制 50MB
    MAX_FILE_SIZE_MB = 50

    # 如果文件超过限制，是否自动压缩
    AUTO_COMPRESS = True

    # 压缩质量 (1-100)
    COMPRESS_QUALITY = 85

    # ============ 并发限制 ============
    # 最大同时下载数
    MAX_CONCURRENT_DOWNLOADS = 3

    # ============ 速率限制 ============
    # 每个用户每小时最多下载次数
    MAX_DOWNLOADS_PER_HOUR = 10

    # 每个用户每小时最多搜索次数
    MAX_SEARCHES_PER_HOUR = 20

    # ============ JMComic 配置 ============
    # 是否使用代理
    USE_PROXY = False

    # 代理地址 (如果使用)
    PROXY_URL = None

    # 下载超时时间 (秒)
    DOWNLOAD_TIMEOUT = 600

    # ============ 预览配置 ============
    # 预览图片数量
    PREVIEW_IMAGE_COUNT = 5

    # 是否发送预览缩略图
    SEND_THUMBNAIL = True

    # ============ 其他配置 ============
    # 是否启用详细日志
    VERBOSE_LOGGING = True

    # 命令前缀
    COMMAND_PREFIX = "/"

    @classmethod
    def validate(cls):
        """验证配置"""
        if cls.TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
            raise ValueError(
                "请先配置 TELEGRAM_TOKEN！\n"
                "1. 打开 Telegram，搜索 @BotFather\n"
                "2. 发送 /newbot 创建新机器人\n"
                "3. 复制获得的 Token 到 telegram_config.py"
            )

        # ALLOWED_USERS 为空列表表示公开模式，允许所有用户
        # 不需要验证

        # 创建必要的目录
        cls.DOWNLOAD_DIR.mkdir(exist_ok=True, parents=True)
        cls.TEMP_DIR.mkdir(exist_ok=True, parents=True)

        return True
