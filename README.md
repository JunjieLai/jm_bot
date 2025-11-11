# 📱 JMComic Telegram Bot

一个功能强大的 Telegram 机器人，用于搜索和下载 JMComic 漫画。

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## ✨ 功能特性

- 🔍 **搜索漫画** - 支持关键词搜索
- 📥 **一键下载** - 自动下载并转换为 PDF
- 📊 **实时进度** - 下载进度实时显示
- 🎯 **友好界面** - 按钮式操作，简单易用
- 🌐 **公开访问** - 任何人都可以使用
- ⚡ **24/7 运行** - 部署在 Railway，无休眠

## 🚀 快速开始

### 使用在线 Bot

直接访问：**[@Jm6271_bot](https://t.me/Jm6271_bot)**

1. 发送 `/start` 开始
2. 点击下方按钮选择操作
3. 输入关键词或漫画 ID
4. 等待下载完成

### 部署你自己的 Bot

#### 方法 1：一键部署到 Railway（推荐）

1. Fork 这个仓库
2. 访问 [Railway](https://railway.app)
3. 用 GitHub 登录
4. New Project → Deploy from GitHub
5. 选择你的仓库
6. 添加环境变量：`TELEGRAM_TOKEN`
7. 部署完成！

**详细步骤：** 查看 [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

#### 方法 2：Docker 部署

```bash
docker build -t jmcomic-bot .
docker run -d \
  -e TELEGRAM_TOKEN="你的_BOT_TOKEN" \
  --name jmcomic-bot \
  jmcomic-bot
```

#### 方法 3：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export TELEGRAM_TOKEN="你的_BOT_TOKEN"

# 运行
python telegram_bot.py
```

## 📖 使用方法

### 按钮操作（推荐）

1. 发送 `/start` 显示主菜单
2. 点击按钮：
   - 🔍 搜索漫画
   - 📥 下载漫画
   - ℹ️ 查看信息
   - ❓ 帮助
3. 按提示输入关键词或 ID

### 命令操作

- `/search 关键词` - 搜索漫画
- `/download ID` - 下载漫画
- `/info ID` - 查看漫画信息
- `/help` - 查看帮助

## 🛠️ 技术栈

- **Bot 框架**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- **爬虫库**: [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python)
- **图片处理**: Pillow
- **部署平台**: Railway
- **容器化**: Docker

## 📦 项目结构

```
jm_bot/
├── telegram_bot.py          # Bot 主程序
├── telegram_config.py       # 配置文件
├── jmcomic_wrapper.py       # JMComic API 封装
├── requirements.txt         # Python 依赖
├── Dockerfile              # Docker 配置
├── railway.json            # Railway 配置
├── JMComic-Crawler-Python/ # JMComic 爬虫库
└── README.md               # 本文件
```

## ⚙️ 配置说明

在 `telegram_config.py` 中可以调整：

```python
# Bot Token（优先使用环境变量）
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "默认值")

# 授权用户（空列表 = 公开模式）
ALLOWED_USERS = []

# 文件大小限制
MAX_FILE_SIZE_MB = 50

# 自动清理临时文件
AUTO_CLEANUP = True
```

## 🔒 安全提示

⚠️ **重要提醒：**

1. 不要将 `TELEGRAM_TOKEN` 提交到公开仓库
2. 使用环境变量管理敏感信息
3. 考虑设置 `ALLOWED_USERS` 限制访问
4. 本项目仅供学习交流使用

## 💰 部署成本

**Railway 免费套餐：**
- $5/月 免费额度
- 约 410 小时运行时间
- 足够 24/7 运行一个 Bot
- 超额后自动停止（不扣费）

## 🔄 更新部署

```bash
git add .
git commit -m "更新功能"
git push
```

Railway 会自动检测并重新部署！

## 📝 开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 本地测试

```bash
export TELEGRAM_TOKEN="你的_TOKEN"
python telegram_bot.py
```

### Docker 测试

```bash
docker build -t jmcomic-bot .
docker run -e TELEGRAM_TOKEN="你的_TOKEN" jmcomic-bot
```

## 🙏 致谢

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - 优秀的 Telegram Bot 框架
- [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) - 强大的 JMComic 爬虫库
- [Railway](https://railway.app) - 优秀的云部署平台

## 📄 许可证

MIT License

## 📮 反馈

有问题或建议？欢迎提 Issue 或 Pull Request！

---

**免责声明**: 本项目仅供技术学习交流，请勿用于非法用途。使用本项目产生的任何后果由使用者自行承担。
