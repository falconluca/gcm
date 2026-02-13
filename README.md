# Auto Gitmsg

基于 LLM 的 Git Commit Message 自动生成工具。

## 功能

- 自动获取 Git 暂存区变更
- 支持 OpenAI 协议的各类大模型
- 支持精简/详细两种 commit message 风格
- 遵循 Conventional Commits 规范
- 支持自定义配置

## 安装

```bash
# 从源码安装
pip install -e .

# 或直接安装依赖后使用
pip install -r requirements.txt
```

## 配置

### 1. 设置 API Key

```bash
# 设置环境变量（推荐）
export OPENAI_API_KEY="your-api-key"
```

### 2. 配置文件（可选）

在项目目录或用户主目录创建 `.gitmsg.yaml`：

```yaml
api_base: https://api.openai.com/v1
model: gpt-4o-mini
temperature: 0.7
max_tokens: 1000
```

## 使用

```bash
# 生成精简 commit message
gitmsg

# 生成详细 commit message
gitmsg -v

# 指定模型
gitmsg -m gpt-4

# 使用自定义配置文件
gitmsg -c /path/to/config.yaml

# 查看帮助
gitmsg --help
```

### 与 Git 集成

```bash
# 直接使用生成的 message 提交
git commit -m "$(gitmsg)"

# 或创建别名
git config --global alias.cm '!git commit -m "$(gitmsg)"'
# 之后可以用 git cm
```

## 支持的模型

任何兼容 OpenAI API 的模型，包括：

- OpenAI: gpt-4o, gpt-4o-mini, gpt-4, gpt-3.5-turbo
- Azure OpenAI
- 本地部署模型（Ollama, vLLM 等）
- 第三方 API 服务

只需修改 `api_base` 和 `model` 配置即可。

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
- 添加登录状态持久化

Closes #123
```

## 开发

```bash
# 安装开发依赖
pip install -e .

# 运行测试
python -m pytest
```

## License

MIT
