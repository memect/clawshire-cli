---
name: clawshire-annual-analysis
version: 1.0.0
description: "ClawShire 年报分析技能。通过 clawshire CLI 发起年报分析任务，支持本地 PDF、PDF 直链、按公司定位年报三种方式，并可查询任务状态与下载报告。"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire annual-analysis --help"
---

# ClawShire 年报分析技能

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)，其中包含安装、认证、错误处理与安全规则。**

本技能用于通过 `clawshire` CLI 发起年报分析任务，并查询分析状态或下载报告。

适用场景：

- 用户已经有本地 PDF，希望直接提交分析
- 用户有 PDF 链接，希望提交分析
- 用户只给出证券代码或公司简称，希望自动定位年报并提交分析
- 用户已经有 `task_id` 或 `job_id`，希望查询状态

优先路由：

1. 用户只给公司代码或简称，优先用 `company`
2. 用户给本地 PDF，优先用 `pdf-file`
3. 用户给 PDF 链接，可尝试 `pdf-url`，但失败时优先回退到 `company`
4. 用户已经有 `task_id` 或 `job_id`，直接用 `get`

需要时再读取：

- 命令与示例：[`references/commands.md`](references/commands.md)
- 任务生命周期与输出规则：[`references/task-lifecycle.md`](references/task-lifecycle.md)
