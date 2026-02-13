# GCM

Git Commit Message 自动生成工具。

## 功能

- 自动获取 Git 暂存区变更
- 支持 OpenAI 协议的各类大模型
- 支持精简/详细两种 commit message 风格
- 遵循 Conventional Commits 规范
- 通过 `.env` 文件配置

## 安装

```bash
make install
```

## 配置

在项目目录创建 `.env` 文件：

```bash
# 必需：API Key
OPENAI_API_KEY="your-api-key"

# 可选：API URL（用于智谱 AI 等第三方服务）
OPENAI_API_URL="https://api.openai.com/v1"

# 可选：模型名称
OPENAI_MODEL="gpt-4o-mini"
```

### 支持的服务

| 服务 | OPENAI_API_URL | OPENAI_MODEL |
|------|----------------|--------------|
| OpenAI | https://api.openai.com/v1 | gpt-4o, gpt-4o-mini |
| 智谱 AI | https://open.bigmodel.cn/api/paas/v4 | glm-4-plus, glm-4-flash |
| DeepSeek | https://api.deepseek.com | deepseek-chat |
| Ollama | http://localhost:11434/v1 | llama3, qwen2 |

## 使用

```bash
# 生成精简 commit message
gcm

# 生成详细 commit message
gcm -v

# 指定模型（覆盖 .env）
gcm -m gpt-4

# 查看帮助
gcm --help
```

### 与 Git 集成

```bash
# 直接使用生成的 message 提交
git commit -m "$(gcm)"

# 或创建别名
git config --global alias.cm '!git commit -m "$(gcm)"'
# 之后可以用 git cm
```

## 输出示例

### 精简模式

```
feat(auth): 添加用户登录功能
```

### 详细模式

```
feat(auth): 添加用户登录功能

- 实现 JWT token 认证
- 添加登录表单验证
- 集成第三方 OAuth 登录

Closes #123
```

## License

MIT
