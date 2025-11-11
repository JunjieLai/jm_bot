#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JMComic Telegram Bot
一个用于搜索和下载 JMComic 漫画的 Telegram 机器人
"""
import asyncio
import logging
from pathlib import Path
import shutil
from typing import Optional
from functools import wraps

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)

from telegram_config import TelegramConfig
from jmcomic_wrapper import JMComicAPI

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if TelegramConfig.VERBOSE_LOGGING else logging.WARNING
)
logger = logging.getLogger(__name__)

# 初始化 JMComic API
jm_api = JMComicAPI(TelegramConfig.DOWNLOAD_DIR)

# 存储用户状态
user_states = {}

# 对话状态
SELECTING_ACTION, WAITING_INPUT = range(2)

# 主菜单键盘
def get_main_keyboard():
    """获取主菜单键盘"""
    keyboard = [
        [KeyboardButton("🔍 搜索漫画"), KeyboardButton("📥 下载漫画")],
        [KeyboardButton("ℹ️ 查看信息"), KeyboardButton("❓ 帮助")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def authorized_only(func):
    """装饰器：仅允许授权用户使用"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if TelegramConfig.ALLOWED_USERS and user_id not in TelegramConfig.ALLOWED_USERS:
            await update.message.reply_text(
                "❌ 未授权访问\n\n"
                f"您的 Telegram ID: {user_id}\n"
                "请联系管理员添加授权。"
            )
            logger.warning(f"未授权用户尝试访问: {user_id}")
            return

        return await func(update, context)

    return wrapper


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    user_id = update.effective_user.id
    welcome_text = (
        "👋 欢迎使用 JMComic Bot！\n\n"
        "🤖 我可以帮你搜索和下载漫画\n\n"
        "📱 使用方式：\n"
        "1️⃣ 点击下方按钮选择操作\n"
        "2️⃣ 输入关键词或漫画 ID\n\n"
        "💡 也可以使用命令：\n"
        "/search <关键词> - 搜索漫画\n"
        "/download <ID> - 下载漫画\n"
        "/info <ID> - 查看漫画信息\n\n"
    )

    # 检查授权
    if TelegramConfig.ALLOWED_USERS and user_id not in TelegramConfig.ALLOWED_USERS:
        welcome_text += (
            f"⚠️ 您的 ID: {user_id}\n"
            "请联系管理员添加授权后使用。"
        )
        await update.message.reply_text(welcome_text)
    else:
        welcome_text += "✅ 请选择操作："
        await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

    return SELECTING_ACTION


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    help_text = (
        "📚 JMComic Bot 使用指南\n\n"
        "📱 按钮操作：\n"
        "点击下方按钮选择操作，然后输入关键词或 ID\n\n"
        "⌨️ 命令操作：\n"
        "🔍 /search 僕の乳母メイド\n"
        "📥 /download 1222345\n"
        "ℹ️ /info 1222345\n\n"
        "💡 提示：\n"
        "• 搜索结果会显示按钮，可直接点击下载\n"
        "• 下载默认为 PDF 格式\n"
        f"• 单文件最大 {TelegramConfig.MAX_FILE_SIZE_MB}MB\n"
        "• 大文件会自动压缩\n\n"
        "❓ 需要帮助？访问 @Jm6271_bot"
    )

    await update.message.reply_text(help_text, reply_markup=get_main_keyboard())
    return SELECTING_ACTION


async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理菜单按钮选择"""
    text = update.message.text
    user_id = update.effective_user.id

    # 检查授权
    if TelegramConfig.ALLOWED_USERS and user_id not in TelegramConfig.ALLOWED_USERS:
        await update.message.reply_text(
            "❌ 未授权访问\n\n"
            f"您的 Telegram ID: {user_id}\n"
            "请联系管理员添加授权。"
        )
        return ConversationHandler.END

    if text == "🔍 搜索漫画":
        context.user_data['action'] = 'search'
        await update.message.reply_text(
            "🔍 搜索漫画\n\n"
            "请输入搜索关键词：\n"
            "例如：僕の乳母メイド"
        )
        return WAITING_INPUT

    elif text == "📥 下载漫画":
        context.user_data['action'] = 'download'
        await update.message.reply_text(
            "📥 下载漫画\n\n"
            "请输入漫画 ID：\n"
            "例如：1222345"
        )
        return WAITING_INPUT

    elif text == "ℹ️ 查看信息":
        context.user_data['action'] = 'info'
        await update.message.reply_text(
            "ℹ️ 查看漫画信息\n\n"
            "请输入漫画 ID：\n"
            "例如：1222345"
        )
        return WAITING_INPUT

    elif text == "❓ 帮助":
        return await help_command(update, context)

    return SELECTING_ACTION


async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户输入"""
    action = context.user_data.get('action')
    user_input = update.message.text.strip()

    if action == 'search':
        # 模拟命令调用
        context.args = user_input.split()
        await search_command(update, context)

    elif action == 'download':
        # 模拟命令调用
        context.args = [user_input]
        await download_command(update, context)

    elif action == 'info':
        # 模拟命令调用
        context.args = [user_input]
        await info_command(update, context)

    # 清除用户数据并返回主菜单
    context.user_data.clear()
    return SELECTING_ACTION


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """取消当前操作"""
    await update.message.reply_text(
        "操作已取消\n\n"
        "请选择新的操作：",
        reply_markup=get_main_keyboard()
    )
    context.user_data.clear()
    return SELECTING_ACTION


@authorized_only
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /search 命令"""
    # 获取搜索关键词
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供搜索关键词\n\n"
            "示例: /search 僕の乳母メイド"
        )
        return

    keyword = " ".join(context.args)

    # 发送搜索中消息
    searching_msg = await update.message.reply_text(
        f"🔍 正在搜索: {keyword}\n"
        "请稍候..."
    )

    try:
        # 搜索
        results = await jm_api.search(keyword, limit=5)

        if not results:
            await searching_msg.edit_text(
                f"❌ 没有找到匹配的漫画\n\n"
                f"关键词: {keyword}"
            )
            return

        # 构建结果消息
        result_text = f"📚 找到 {len(results)} 个结果：\n\n"

        for i, comic in enumerate(results, 1):
            result_text += (
                f"{i}️⃣ ID: {comic['id']}\n"
                f"   📖 {comic['title'][:50]}...\n"
                f"   ✍️ {comic['author']}\n\n"
            )

        # 创建按钮
        keyboard = []
        for comic in results:
            keyboard.append([
                InlineKeyboardButton(
                    f"📥 {comic['id']} - {comic['title'][:20]}...",
                    callback_data=f"download_{comic['id']}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await searching_msg.edit_text(
            result_text,
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"搜索错误: {e}", exc_info=True)
        await searching_msg.edit_text(
            f"❌ 搜索失败: {str(e)}"
        )


@authorized_only
async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /download 命令"""
    # 获取漫画 ID
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供漫画 ID\n\n"
            "示例: /download 1222345"
        )
        return

    album_id = context.args[0]

    await handle_download(update, album_id)


async def handle_download(update: Update, album_id: str):
    """处理下载逻辑"""
    # 发送下载中消息
    if update.callback_query:
        await update.callback_query.answer("开始下载...")
        downloading_msg = await update.callback_query.message.reply_text(
            f"📥 开始下载 ID: {album_id}\n"
            "⏳ 请稍候..."
        )
    else:
        downloading_msg = await update.message.reply_text(
            f"📥 开始下载 ID: {album_id}\n"
            "⏳ 请稍候..."
        )

    try:
        # 进度回调
        last_percent = 0

        async def progress_callback(current, total):
            nonlocal last_percent
            percent = int(current / total * 100)

            # 每 20% 更新一次
            if percent - last_percent >= 20:
                last_percent = percent
                bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
                await downloading_msg.edit_text(
                    f"📥 下载中: {album_id}\n"
                    f"⏳ 进度: [{bar}] {percent}%\n"
                    f"📄 {current}/{total} 页"
                )

        # 下载
        logger.info(f"开始下载漫画 {album_id}")
        download_dir = await jm_api.download(album_id, progress_callback)

        if not download_dir:
            logger.error(f"下载失败: {album_id}")
            await downloading_msg.edit_text(
                f"❌ 下载失败\n\n"
                f"漫画 ID: {album_id}\n"
                "请检查 ID 是否正确"
            )
            return

        logger.info(f"下载完成，目录: {download_dir}")
        await downloading_msg.edit_text(
            f"✅ 下载完成！\n"
            f"📦 正在生成 PDF..."
        )

        # 创建 PDF
        pdf_file = TelegramConfig.TEMP_DIR / f"{album_id}.pdf"
        logger.info(f"开始生成 PDF: {pdf_file}")
        success = await jm_api.create_pdf(download_dir, pdf_file)

        if not success:
            logger.error(f"生成 PDF 失败: {album_id}")
            await downloading_msg.edit_text(
                f"❌ 生成 PDF 失败"
            )
            return

        logger.info(f"PDF 生成成功: {pdf_file}")

        # 检查文件大小
        file_size_mb = pdf_file.stat().st_size / (1024 * 1024)

        if file_size_mb > TelegramConfig.MAX_FILE_SIZE_MB:
            await downloading_msg.edit_text(
                f"⚠️ 文件过大 ({file_size_mb:.1f}MB)\n"
                f"Telegram 限制: {TelegramConfig.MAX_FILE_SIZE_MB}MB\n\n"
                "建议：使用其他方式传输或压缩文件"
            )
            # 清理
            pdf_file.unlink()
            return

        # 发送文件
        logger.info(f"开始上传 PDF: {file_size_mb:.1f}MB")
        await downloading_msg.edit_text(
            f"📤 正在上传 PDF ({file_size_mb:.1f}MB)...\n"
            "请稍候..."
        )

        try:
            with open(pdf_file, 'rb') as f:
                await update.effective_chat.send_document(
                    document=f,
                    filename=f"{album_id}.pdf",
                    caption=f"📖 漫画 ID: {album_id}\n📦 大小: {file_size_mb:.1f}MB",
                    read_timeout=120,
                    write_timeout=120
                )
            logger.info(f"PDF 上传成功")
        except Exception as e:
            logger.error(f"上传 PDF 失败: {e}", exc_info=True)
            await downloading_msg.edit_text(
                f"❌ 上传 PDF 失败: {str(e)}"
            )
            return

        # 删除下载消息
        try:
            await downloading_msg.delete()
        except:
            pass

        # 清理文件
        try:
            pdf_file.unlink()
            logger.info(f"已删除临时 PDF 文件")
        except Exception as e:
            logger.warning(f"删除 PDF 文件失败: {e}")

        if TelegramConfig.AUTO_CLEANUP:
            try:
                shutil.rmtree(download_dir, ignore_errors=True)
                logger.info(f"已清理下载目录")
            except Exception as e:
                logger.warning(f"清理下载目录失败: {e}")

        logger.info(f"成功完成整个流程: {album_id} ({file_size_mb:.1f}MB)")

    except Exception as e:
        logger.error(f"下载错误: {e}", exc_info=True)
        await downloading_msg.edit_text(
            f"❌ 下载失败: {str(e)}"
        )


@authorized_only
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /info 命令"""
    # 获取漫画 ID
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供漫画 ID\n\n"
            "示例: /info 1222345"
        )
        return

    album_id = context.args[0]

    # 发送查询中消息
    info_msg = await update.message.reply_text(
        f"ℹ️ 正在获取信息...\n"
        f"ID: {album_id}"
    )

    try:
        # 获取信息
        info = await jm_api.get_info(album_id)

        if not info:
            await info_msg.edit_text(
                f"❌ 获取失败\n\n"
                f"漫画 ID: {album_id}"
            )
            return

        # 构建信息文本
        info_text = (
            f"📖 漫画信息\n\n"
            f"ID: {info['id']}\n"
            f"标题: {info['title']}\n"
            f"作者: {info['author']}\n"
            f"类别: {info['category']}\n"
            f"页数: {info['page_count']} 页\n"
        )

        if info.get('tags'):
            tags = ', '.join(info['tags'][:5])
            info_text += f"标签: {tags}\n"

        info_text += f"\n更新: {info['update_date']}"

        # 添加下载按钮
        keyboard = [[
            InlineKeyboardButton("📥 下载 PDF", callback_data=f"download_{album_id}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await info_msg.edit_text(
            info_text,
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"获取信息错误: {e}", exc_info=True)
        await info_msg.edit_text(
            f"❌ 获取失败: {str(e)}"
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮回调"""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("download_"):
        album_id = data.replace("download_", "")
        await handle_download(update, album_id)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理未知命令"""
    await update.message.reply_text(
        "❌ 未知命令\n\n"
        "请使用 /help 查看可用命令"
    )


def main():
    """主函数"""
    try:
        # 验证配置
        TelegramConfig.validate()

        logger.info("启动 JMComic Telegram Bot...")
        logger.info(f"Bot: @Jm6271_bot")

        # 创建应用
        application = Application.builder().token(TelegramConfig.TELEGRAM_TOKEN).build()

        # 创建对话处理器
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", start_command),
                CommandHandler("help", help_command),
                MessageHandler(filters.Regex("^(🔍 搜索漫画|📥 下载漫画|ℹ️ 查看信息|❓ 帮助)$"), handle_menu_selection),
            ],
            states={
                SELECTING_ACTION: [
                    MessageHandler(filters.Regex("^(🔍 搜索漫画|📥 下载漫画|ℹ️ 查看信息|❓ 帮助)$"), handle_menu_selection),
                    CommandHandler("search", search_command),
                    CommandHandler("download", download_command),
                    CommandHandler("info", info_command),
                    CommandHandler("cancel", cancel_command),
                ],
                WAITING_INPUT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input),
                    CommandHandler("cancel", cancel_command),
                ],
            },
            fallbacks=[
                CommandHandler("cancel", cancel_command),
                CommandHandler("start", start_command),
            ],
            allow_reentry=True,
        )

        # 注册对话处理器
        application.add_handler(conv_handler)

        # 注册按钮回调处理器
        application.add_handler(CallbackQueryHandler(button_callback))

        # 注册未知命令处理器
        application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

        # 启动机器人
        logger.info("机器人已启动，正在监听消息...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except ValueError as e:
        print(f"\n❌ 配置错误:\n{e}\n")
    except Exception as e:
        logger.error(f"启动失败: {e}", exc_info=True)
    finally:
        jm_api.cleanup()


if __name__ == "__main__":
    main()
