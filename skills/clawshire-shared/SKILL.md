---
name: clawshire-shared
version: 1.0.0
description: "ClawShire CLI 共享规则：安装、认证、输出格式、错误处理与安全约束。首次使用或遇到认证/配置问题时优先读取。"
triggers: ["clawshire", "/clawshire", "clawshire auth", "clawshire login", "api key", "auth status", "auth check", "clawshire 配置", "clawshire 安装"]
invocable: true
argument-hint: "[command] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire --help"
---

# /clawshire - Shared Rules

所有 ClawShire CLI 场景都先遵守这份共享规则。

## Agent Invariants

1. 先确认运行前提：`clawshire` 是否可用、是否需要 API Key、输出格式该选什么。
2. 永远不要明文回显 API Key，只能展示掩码或提醒用户自行配置。
3. 对 `user info`、`annual-report`、`annual-analysis` 这类需要认证的命令，优先建议先跑 `clawshire auth status` 或 `clawshire auth check`。
4. 面向脚本或 Agent，优先用 `clawshire --output json ...`；面向终端用户阅读，优先用默认表格输出。
5. 对会产生费用、上传文件、提交分析任务、批量查询的命令，先说明行为，不要在用户意图不明确时自动扩大范围。
6. 如果用户只是问“怎么配”“为什么报错”“怎么升级”，先用本技能，不要直接跳到业务型 skill。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 检查 CLI 是否已安装 | `clawshire --help` |
| 查看 CLI 版本 | `clawshire version` |
| 查看认证配置 | `clawshire auth show` |
| 查看认证状态 | `clawshire auth status` |
| 检查认证是否可用 | `clawshire auth check` |
| 保存 API Key | `clawshire auth set-key <your_api_key>` |
| 清除 API Key | `clawshire auth logout` |
| 升级 CLI | `clawshire update` |
| 只看升级命令 | `clawshire update --dry-run` |

## Output Modes

| 目标 | 推荐写法 |
|------|----------|
| 给人看 | `clawshire ...` |
| 给脚本或 Agent 消费 | `clawshire --output json ...` |
| 写到文档或聊天里 | `clawshire --output markdown ...` |
| 导出表格 | `clawshire --output csv ...` |

总规则：不要依赖默认格式推断，想要结构化结果时显式加 `--output json`。

## Decision Tree

```
用户现在要做什么？
├── 先安装 / 升级 CLI → 检查 `clawshire --help` 或 `clawshire update`
├── 配 API Key / 查认证状态 → 用 `auth show/status/check/logout`
├── 问公告怎么查 → 切到 clawshire-data-query
├── 问年报怎么查 → 切到 clawshire-annual-report
└── 问年报分析怎么做 → 切到 clawshire-annual-analysis
```

## Common Workflows

### 首次安装到验证

```bash
clawshire --help
clawshire auth set-key <your_api_key>
clawshire auth status
clawshire user info
```

### 临时环境变量方式

```bash
export CLAWSHIRE_API_KEY="<your_api_key>"
clawshire auth status
clawshire user info
```

### 升级当前 CLI

```bash
clawshire update --dry-run
clawshire update
```

## References

- 安装、认证、输出格式：[`references/setup.md`](references/setup.md)
- 常见报错与处理：[`references/errors.md`](references/errors.md)
