# 🚀 快速开始 - Railway 部署

## ✅ GitHub 仓库已创建

**仓库地址：** https://github.com/JunjieLai/jm_bot

代码已成功推送！

---

## 📋 下一步：Railway 部署（5分钟）

### 第 1 步：访问 Railway

打开浏览器访问：**https://railway.app**

### 第 2 步：GitHub 登录

点击 **"Login with GitHub"**

### 第 3 步：创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 找到并选择 **JunjieLai/jm_bot**
4. 点击 **"Deploy Now"**

### 第 4 步：添加环境变量

1. 等待初始部署完成（会失败，因为缺少环境变量）
2. 点击你的项目
3. 点击 **"Variables"** 标签
4. 点击 **"New Variable"**
5. 添加：
   ```
   TELEGRAM_TOKEN
   ```
   值：
   ```
   8226987850:AAE-RYMD84QgFnlFKH7t7W5nvz_w4ytiNoc
   ```
6. 点击 **"Add"**

### 第 5 步：重新部署

1. 点击 **"Deployments"** 标签
2. 点击右上角的 **"Deploy"** 按钮
3. 等待 2-3 分钟

### 第 6 步：验证

1. 查看 **"Deployments"**，状态应为 **"Success"** ✅
2. 点击 **"View Logs"**，应显示：
   ```
   启动 JMComic Telegram Bot...
   Bot: @Jm6271_bot
   机器人已启动，正在监听消息...
   ```
3. 打开 Telegram 测试：https://t.me/Jm6271_bot
4. 发送 `/start`

---

## 🎉 完成！

如果看到 Bot 回复，说明部署成功！

你的 Bot 现在 24/7 运行在 Railway 上，无休眠！

---

## 📊 Railway Dashboard

访问 https://railway.app/dashboard 查看：
- ✅ 实时日志
- ✅ CPU/内存使用
- ✅ 部署历史
- ✅ 环境变量

---

## 🔄 更新部署

以后更新代码只需：

```bash
git add .
git commit -m "更新说明"
git push
```

Railway 会自动检测并重新部署！

---

## 💰 费用

- **免费额度：** $5/月
- **预计使用：** ~$3-4/月（24/7运行）
- **超额处理：** 自动停止（不会扣费）

---

## 🆘 遇到问题？

1. **查看详细指南：**
   ```bash
   cat RAILWAY_DEPLOY.md
   ```

2. **检查日志：**
   - Railway Dashboard → Your Project → Logs

3. **常见问题：**
   - 构建失败 → 检查依赖
   - 运行失败 → 检查环境变量
   - Bot 无响应 → 查看日志错误

---

## 📞 需要帮助？

- 📖 查看 [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)
- 📖 查看 [README.md](README.md)
- 🌐 访问 [Railway 文档](https://docs.railway.app)

---

**🎊 开始部署吧！** 🚂
