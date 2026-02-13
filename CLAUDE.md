# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

GCM 是一个基于 AI 的 Git Commit Message 自动生成工具，支持所有 OpenAI 协议兼容的大模型服务。

## 常用命令

```bash
# 安装（开发模式）
make install
# 或
pip install -e .

# 卸载
make uninstall

# 清理缓存和构建文件
make clean

# 测试命令是否可用
make test

# 重新安装
make rebuild

# 直接运行模块（调试用）
python -m gcm.cli -v
```

## 架构

```
gcm/
├── cli.py          # 命令行入口，协调各模块
├── git_utils.py    # Git 操作（获取暂存区、diff）
├── llm_client.py   # LLM 客户端（OpenAI 协议兼容）
└── prompts.py      # 提示词模板（系统提示词、用户提示词构建）
```

### 核心流程

1. **cli.py:main()** 加载 .env 配置，解析命令行参数
2. **git_utils.py** 获取暂存区变更（文件列表 + diff 内容）
3. **prompts.py** 根据变更构建用户提示词
4. **llm_client.py** 调用 LLM API 生成 commit message

### 关键数据结构

- `FileChange`: 单文件变更（status, old_path, new_path）
- `StagedChanges`: 完整暂存区信息（files 列表 + diff_content）
- `LLMConfig`: LLM 配置（api_base, api_key, model 等）

## 配置系统

通过 `.env` 文件配置，支持三个环境变量：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | API Key（必需） | - |
| `OPENAI_API_URL` | API 基础 URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 模型名称 | `gpt-4o-mini` |

### .env 查找顺序

1. 用户主目录 `~/.env`（优先级较低）
2. 当前目录 `.env`
3. 向上查找父目录直到 Git 根目录

## 支持的 LLM 服务

只需配置不同的 `OPENAI_API_URL` 和 `OPENAI_MODEL`：

- OpenAI: `https://api.openai.com/v1`
- 智谱 AI: `https://open.bigmodel.cn/api/paas/v4`
- DeepSeek: `https://api.deepseek.com`
- Ollama: `http://localhost:11434/v1`

## 命令行参数

| 参数 | 说明 |
|------|------|
| `-v, --verbose` | 生成详细的 commit message |
| `-m, --model` | 覆盖 OPENAI_MODEL |
| `--api-base` | 覆盖 OPENAI_API_URL |
| `--api-key` | 覆盖 OPENAI_API_KEY |
