# GCM

**Git Commit Message 自动生成工具** - 基于 AI 的智能 commit message 生成器，支持所有 OpenAI 协议兼容的大模型服务。

## 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [前置要求](#前置要求)
- [快速开始](#快速开始)
- [配置](#配置)
- [使用方法](#使用方法)
- [架构设计](#架构设计)
- [环境变量](#环境变量)
- [可用命令](#可用命令)
- [支持的 LLM 服务](#支持的-llm-服务)
- [输出示例](#输出示例)
- [与 Git 集成](#与-git-集成)
- [故障排除](#故障排除)
- [贡献指南](#贡献指南)
- [License](#license)

---

## 功能特性

- **自动获取 Git 暂存区变更** - 智能解析 `git diff --cached` 输出
- **支持多种 LLM 服务** - 兼容 OpenAI 协议的各类大模型（OpenAI、智谱 AI、DeepSeek、Ollama 等）
- **双模式输出** - 支持精简/详细两种 commit message 风格
- **Conventional Commits 规范** - 自动生成符合规范的 commit message
- **灵活配置** - 通过 `.env` 文件配置，支持命令行参数覆盖
- **智能 .env 查找** - 自动从当前目录向上查找直到 Git 根目录

## 技术栈

| 类别 | 技术 |
|------|------|
| **语言** | Python 3.8+ |
| **包管理** | pip / pipx |
| **构建系统** | setuptools |
| **LLM SDK** | OpenAI Python SDK (>= 1.0.0) |
| **配置管理** | python-dotenv |

## 前置要求

- **Python 3.8+** - 推荐使用 Python 3.10 或更高版本
- **Git** - 需要在 Git 仓库中使用
- **LLM API Key** - OpenAI 或兼容服务的 API Key

### 检查环境

```bash
# 检查 Python 版本
python --version  # 需要 3.8+

# 检查 Git 是否安装
git --version
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/gcm.git
cd gcm
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.\.venv\Scripts\activate   # Windows
```

### 3. 安装

```bash
make install
```

或手动安装：

```bash
pip install -e .
```

### 4. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```bash
OPENAI_API_KEY="your-api-key-here"
```

### 5. 使用

```bash
# 添加一些变更到暂存区
git add .

# 生成 commit message
gcm
```

## 配置

### 环境变量配置

在项目目录或用户主目录创建 `.env` 文件：

```bash
# 必需：API Key
OPENAI_API_KEY="your-api-key"

# 可选：API URL（用于第三方服务）
OPENAI_API_URL="https://api.openai.com/v1"

# 可选：模型名称
OPENAI_MODEL="gpt-4o-mini"
```

### .env 文件查找顺序

GCM 会按以下顺序查找 `.env` 文件（后找到的优先级更高）：

1. 用户主目录 `~/.env`（优先级较低）
2. 当前目录的 `.env`
3. 向上查找父目录直到 Git 根目录

这意味着你可以在主目录配置通用的 API Key，在项目中配置特定模型。

## 使用方法

### 基本用法

```bash
# 生成精简 commit message
gcm

# 生成详细 commit message
gcm -v

# 指定模型（覆盖 .env 配置）
gcm -m gpt-4

# 指定 API URL
gcm --api-base https://api.deepseek.com

# 查看帮助
gcm --help

# 查看版本
gcm --version
```

### 命令行参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--verbose` | `-v` | 生成详细的 commit message |
| `--model MODEL` | `-m` | 使用的模型名称（覆盖 OPENAI_MODEL） |
| `--api-base URL` | | API 基础 URL（覆盖 OPENAI_API_URL） |
| `--api-key KEY` | | API Key（覆盖 OPENAI_API_KEY，不推荐在命令行中使用） |
| `--version` | | 显示版本号 |
| `--help` | `-h` | 显示帮助信息 |

## 架构设计

### 目录结构

```
gcm/
├── gcm/                    # 主包
│   ├── __init__.py        # 包初始化，版本信息
│   ├── cli.py             # 命令行入口
│   ├── git_utils.py       # Git 操作工具
│   ├── llm_client.py      # LLM 客户端
│   └── prompts.py         # 提示词模板
├── .env.example           # 环境变量示例
├── .gitignore             # Git 忽略文件
├── Makefile               # 构建命令
├── pyproject.toml         # 项目配置
├── README.md              # 项目文档
└── requirements.txt       # 依赖列表
```

### 模块说明

#### [cli.py](gcm/cli.py) - 命令行入口

- 解析命令行参数
- 加载 `.env` 配置文件
- 协调各模块完成 commit message 生成

#### [git_utils.py](gcm/git_utils.py) - Git 操作

- `is_git_repo()` - 检查是否在 Git 仓库中
- `get_staged_files()` - 获取暂存区文件列表
- `get_staged_diff()` - 获取暂存区 diff 内容
- `get_staged_changes()` - 获取完整暂存区变更

#### [llm_client.py](gcm/llm_client.py) - LLM 客户端

- `LLMConfig` - 配置数据类
- `LLMClient` - 与大模型交互的客户端
- 懒加载 OpenAI 客户端
- 支持自定义 API URL

#### [prompts.py](gcm/prompts.py) - 提示词模板

- `SYSTEM_PROMPT` - 系统提示词（定义输出规则和格式）
- `build_user_prompt()` - 根据变更内容构建用户提示词

### 工作流程

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  git add    │ ──▶ │  gcm 命令    │ ──▶ │ LLM 生成    │
│  (暂存变更)  │     │  (读取 diff) │     │ (commit msg)│
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ 检查 Git 仓库 │
                    │ 获取暂存变更  │
                    │ 构建 prompt  │
                    │ 调用 LLM API │
                    │ 输出结果     │
                    └──────────────┘
```

## 环境变量

### 必需变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `OPENAI_API_KEY` | LLM 服务的 API Key | `sk-xxx` |

### 可选变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_URL` | API 基础 URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 使用的模型名称 | `gpt-4o-mini` |

## 可用命令

### Makefile 命令

| 命令 | 说明 |
|------|------|
| `make install` | 安装到本地（开发模式） |
| `make uninstall` | 卸载 gcm |
| `make clean` | 清理缓存和构建文件 |
| `make test` | 测试 gcm 命令是否可用 |
| `make rebuild` | 重新安装（clean + install） |

### 手动安装/卸载

```bash
# 安装
pip install -e .

# 卸载
pip uninstall -y gcm

# 清理缓存
rm -rf build/ dist/ *.egg-info __pycache__
```

## 支持的 LLM 服务

| 服务 | OPENAI_API_URL | 推荐模型 |
|------|----------------|----------|
| **OpenAI** | `https://api.openai.com/v1` | `gpt-4o`, `gpt-4o-mini` |
| **智谱 AI** | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-plus`, `glm-4-flash` |
| **DeepSeek** | `https://api.deepseek.com` | `deepseek-chat` |
| **Ollama** | `http://localhost:11434/v1` | `llama3`, `qwen2` |
| **其他** | 任何 OpenAI 兼容 API | 查看服务商文档 |

### 配置示例

**使用智谱 AI：**

```bash
# .env
OPENAI_API_KEY="your-zhipu-api-key"
OPENAI_API_URL="https://open.bigmodel.cn/api/paas/v4"
OPENAI_MODEL="glm-4-flash"
```

**使用 DeepSeek：**

```bash
# .env
OPENAI_API_KEY="your-deepseek-api-key"
OPENAI_API_URL="https://api.deepseek.com"
OPENAI_MODEL="deepseek-chat"
```

**使用本地 Ollama：**

```bash
# 先启动 Ollama 服务
ollama serve

# .env
OPENAI_API_KEY="ollama"  # Ollama 不需要真实 key
OPENAI_API_URL="http://localhost:11434/v1"
OPENAI_MODEL="llama3"
```

## 输出示例

### 精简模式（默认）

```
feat(auth): 添加用户登录功能
```

### 详细模式（`-v`）

```
feat(auth): 添加用户登录功能

- 实现 JWT token 认证
- 添加登录表单验证
- 集成第三方 OAuth 登录（Google、GitHub）
- 添加登录状态持久化

Closes #123
```

### Conventional Commits 类型说明

| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响代码运行） |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 增加测试 |
| `chore` | 构建过程或辅助工具变动 |
| `ci` | CI 配置变动 |
| `build` | 构建系统或依赖变更 |
| `revert` | 回滚 |

## 与 Git 集成

### 直接提交

```bash
# 生成并直接提交
git commit -m "$(gcm)"

# 详细模式
git commit -m "$(gcm -v)"
```

### 创建 Git 别名

```bash
# 添加全局别名
git config --global alias.cm '!git commit -m "$(gcm)"'

# 使用别名
git cm
```

### 作为 prepare-commit-msg 钩子

创建 `.git/hooks/prepare-commit-msg`：

```bash
#!/bin/sh
# 如果已有 commit message，跳过
if [ -n "$2" ] || [ -n "$3" ]; then
    exit 0
fi

# 生成 commit message
gcm > "$1"
```

```bash
chmod +x .git/hooks/prepare-commit-msg
```

之后每次 `git commit`（不带 `-m`）会自动生成 message。

## 故障排除

### 常见错误

#### `错误: 当前目录不在 Git 仓库中`

**原因：** 在非 Git 目录中运行了 `gcm`

**解决：**
```bash
cd your-git-repo
gcm
```

#### `暂存区没有变更`

**原因：** 没有使用 `git add` 添加变更

**解决：**
```bash
git add .
gcm
```

#### `配置错误: API Key 未配置`

**原因：** 未设置 `OPENAI_API_KEY` 环境变量

**解决：**
```bash
# 创建 .env 文件
echo 'OPENAI_API_KEY="your-key"' > .env

# 或设置环境变量
export OPENAI_API_KEY="your-key"
```

#### `生成失败: API 调用失败`

**可能原因：**
1. API Key 无效或过期
2. API URL 配置错误
3. 网络连接问题
4. 模型名称错误

**解决：**
```bash
# 检查配置
cat .env

# 测试 API 连接
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### `ModuleNotFoundError: No module named 'gcm'`

**原因：** 未安装 gcm

**解决：**
```bash
make install
# 或
pip install -e .
```

### 调试模式

查看详细的错误信息：

```bash
# 直接运行模块
python -m gcm.cli -v
```

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git add . && gcm`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/gcm.git
cd gcm

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装开发依赖
pip install -e .

# 运行测试
make test
```

## License

[MIT](LICENSE) © 2024
