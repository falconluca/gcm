# GCM

基于 AI 的 Git Commit Message 自动生成工具，支持所有 OpenAI 协议兼容的大模型服务。

## 安装

```bash
make build
```

## 配置

设置环境变量：

```bash
export GCM_API_KEY="your-api-key"
export GCM_API_URL="https://api.openai.com/v1"
export GCM_MODEL="gpt-4o-mini"
```

## 使用

```bash
git add .
gcm           # 生成精简 commit message
gcm -v        # 生成详细 commit message
```

## 示例

**精简模式：**

```
feat(auth): 添加用户登录功能
```

**详细模式 (`-v`)：**

```
feat(auth): 添加用户登录功能

- 实现 JWT token 认证
- 添加登录表单验证
- 集成第三方 OAuth 登录
```

## Git 集成

```bash
git commit -m "$(gcm)"
```

MIT License
