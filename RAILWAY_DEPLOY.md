# 🚂 Railway 部署指南

## 📋 前置准备

- ✅ GitHub 账号
- ✅ Railway 账号（https://railway.app）
- ✅ 信用卡（验证用，不会扣费）

---

## 🚀 部署步骤（5分钟）

### 第1步：推送到 GitHub

```bash
# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Deploy to Railway"

# 创建 GitHub 仓库后，添加远程仓库
git remote add origin https://github.com/你的用户名/jm_bot.git

# 推送
git branch -M main
git push -u origin main
```

### 第2步：在 Railway 部署

1. 访问 **https://railway.app**
2. 用 GitHub 登录
3. 点击 **"New Project"**
4. 选择 **"Deploy from GitHub repo"**
5. 选择你的 `jm_bot` 仓库
6. Railway 会自动检测到 Dockerfile

### 第3步：配置环境变量

在 Railway Dashboard：

1. 点击你的项目
2. 进入 **"Variables"** 标签
3. 添加环境变量：

```
TELEGRAM_TOKEN = 8226987850:AAE-RYMD84QgFnlFKH7t7W5nvz_w4ytiNoc
```

4. 点击 **"Deploy"**

### 第4步：验证部署

1. 等待 2-3 分钟构建完成
2. 查看 **"Deployments"** 标签，状态应为 "Success"
3. 查看 **"Logs"**，应显示：
   ```
   启动 JMComic Telegram Bot...
   Bot: @Jm6271_bot
   机器人已启动，正在监听消息...
   ```
4. 在 Telegram 测试 `/start` 命令

---

## ✅ 完成！

你的 Bot 现在 24/7 运行在 Railway 上，无休眠问题！

**分享链接：** https://t.me/Jm6271_bot

---

## 🔄 更新部署

代码更新后：

```bash
git add .
git commit -m "更新功能"
git push
```

Railway 会自动检测并重新部署！

---

## 💰 费用说明

- **免费额度：** $5/月（约 410 小时运行时间）
- **超额后：** 自动停止（不会扣费）
- **估算：** 对于 Telegram Bot，足够 24/7 运行

---

## 🐛 故障排查

### 问题 1：构建失败

**查看 Logs 标签，常见原因：**
- 依赖安装失败 → 检查 `requirements.txt`
- Dockerfile 错误 → 检查语法

### 问题 2：运行失败

**检查：**
- 环境变量 `TELEGRAM_TOKEN` 是否设置
- 查看运行日志找错误信息

### 问题 3：Bot 无响应

**确认：**
- Railway 显示 "Active" 状态
- Logs 中没有错误
- Token 正确

---

## 📊 监控

Railway Dashboard 提供：
- ✅ 实时日志
- ✅ CPU/内存使用
- ✅ 网络流量
- ✅ 部署历史

---

## 🎉 享受你的 Bot！

现在你的 Bot 已经在云端稳定运行了！
