# Railway 设置指南

## 必须在 Railway Dashboard 中进行的设置

### 1. 环境变量 (Variables)
```
TELEGRAM_TOKEN = 8226987850:AAE-RYMD84QgFnlFKH7t7W5nvz_w4ytiNoc
```

### 2. 服务设置 (Settings)

#### 关键设置：

**Networking:**
- ❌ **禁用公开网络 (Public Networking)** - Telegram Bot 不需要公开端口
- 或者如果启用了，忽略生成的域名，Bot 只通过 Telegram API 通信

**Deploy:**
- ✅ 确保使用 `Dockerfile` 作为构建方式
- ✅ 重启策略已在 `railway.json` 中配置

**Health Checks:**
- ❌ **禁用健康检查** - 因为 Bot 使用 polling 模式，不暴露 HTTP 端点
- 如果 Railway UI 中有健康检查选项，设置为：
  - Health Check Path: (留空或删除)
  - Health Check Timeout: (留空或删除)

### 3. 资源限制 (可选)

如果下载大文件时遇到问题，可能需要增加：
- **Memory**: 至少 512MB（免费版已足够）
- **Timeout**: 确保没有设置过短的超时时间

## 验证设置

部署后，检查以下内容：

1. **日志显示**：
   ```
   启动 JMComic Telegram Bot...
   Bot: @Jm6271_bot
   机器人已启动，正在监听消息...
   ```

2. **服务状态**: Active (绿色)

3. **没有频繁重启**: 如果看到反复重启，检查：
   - 健康检查是否已禁用
   - 日志中的错误信息

## 常见问题

### Q: Bot 在下载时被重启
**A**: 禁用健康检查，或者增加健康检查超时时间

### Q: 显示 "No Public Port"
**A**: 正常！Telegram Bot 不需要公开端口

### Q: 下载完成后没有返回 PDF
**A**: 检查日志，查看具体在哪一步失败了。现在日志非常详细，会显示每个步骤。

## 推荐的 Railway 项目设置截图位置

1. 进入项目 → Settings
2. 找到 "Networking" 部分 → 禁用或忽略
3. 找到 "Health Check" 部分 → 禁用
4. Variables → 添加 TELEGRAM_TOKEN

---

**提示**: Railway 的 UI 可能会变化，以上是基于当前版本的建议。关键是确保没有健康检查干扰 Bot 的长时间运行任务。
