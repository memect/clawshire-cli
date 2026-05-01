---
name: clawshire-annual-analysis
version: 1.0.0
description: "ClawShire 年报分析技能。通过 clawshire CLI 发起年报分析任务，支持本地 PDF、PDF 直链、按公司定位年报三种方式，并可查询任务状态与下载报告。"
triggers: ["clawshire annual-analysis", "年报分析", "分析年报", "pdf 分析", "annual-analysis company", "annual-analysis pdf-file", "annual-analysis pdf-url", "annual-analysis get"]
invocable: true
argument-hint: "[company|pdf-file|pdf-url|get] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire annual-analysis --help"
---

# /clawshire-annual-analysis - Annual Analysis

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)，其中包含安装、认证、错误处理与安全规则。**

通过 `clawshire` CLI 发起年报分析任务，并查询分析状态或下载报告。

## Agent Invariants

1. 本技能会触发真实分析任务，可能消耗额度；用户意图不明确时不要自动提交。
2. 用户只给公司代码或简称时，优先 `annual-analysis company`，这是最稳定入口。
3. 用户给本地 PDF 时，才用 `pdf-file`；给 PDF 直链时，才用 `pdf-url`。
4. 用户已经有 `task_id` 或 `job_id` 时，优先 `get`，不要重复提交。
5. `pdf-url` 依赖上游 PDF 可访问；失败时优先回退到 `company` 模式。
6. 如果服务端提示“已有分析任务在进行中”，这通常说明链路已到达服务端，重复提交没有意义。
7. Agent 调用 CLI 时，命令前必须带 `--client skill --skill-name clawshire-annual-analysis --agent-name <agent-name-or-unknown-agent> --rationale <why-this-call>`。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 按公司提交分析 | `clawshire annual-analysis company <kw> --year <YYYY>` |
| 用本地 PDF 提交 | `clawshire annual-analysis pdf-file <path>` |
| 用 PDF 链接提交 | `clawshire annual-analysis pdf-url <url>` |
| 查询任务状态 | `clawshire annual-analysis get <task_or_job_id>` |
| 下载完成后的 HTML 报告 | `clawshire annual-analysis get <id> --save-report-to report.html` |

## Decision Tree

```
用户手里有什么？
├── 证券代码或公司简称 → annual-analysis company
├── 本地 PDF 文件 → annual-analysis pdf-file
├── PDF 直链 → annual-analysis pdf-url
└── task_id / job_id → annual-analysis get
```

## Common Workflows

### 最推荐：按公司提交分析

```bash
clawshire annual-analysis company 000001 --year 2025 --format json
```

### 用本地 PDF 提交

```bash
clawshire annual-analysis pdf-file ./report.pdf --format json
```

### 查询任务状态

```bash
clawshire annual-analysis get 74 --format json
```

### 下载已完成报告

```bash
clawshire annual-analysis get 74 --save-report-to report.html
```

## Output Rules

- 面向用户：至少说明当前分析对象、任务 ID、状态、下一步命令。
- 面向脚本：优先 `--format json`。
- 如果提交结果里带 `next_command`，优先直接提示执行它。

## References

- 命令与示例：[`references/commands.md`](references/commands.md)
- 任务生命周期与输出规则：[`references/task-lifecycle.md`](references/task-lifecycle.md)
