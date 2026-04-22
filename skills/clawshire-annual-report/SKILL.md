---
name: clawshire-annual-report
version: 1.0.0
description: "ClawShire 年报查询技能。通过 clawshire CLI 查询年报列表与结构化年报数据，适合按年份、公司简称、证券代码快速定位年报。"
triggers: ["clawshire annual-report", "年报查询", "查年报", "定位年报", "annual-report latest", "annual-report data", "met_uuid", "年报 pdf"]
invocable: true
argument-hint: "[latest|data] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire annual-report --help"
---

# /clawshire-annual-report - Annual Report Query

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)，其中包含安装、认证、错误处理与安全规则。**

通过 `clawshire` CLI 查询年报列表，以及读取具体年报的结构化数据。

## Agent Invariants

1. 本技能默认需要 API Key；若认证状态不明确，先回到 shared skill 检查。
2. 用户想“先找到年报”时，优先 `annual-report latest`。
3. 用户已经有 `met_uuid` 时，直接 `annual-report data`，不要重复检索列表。
4. 如果用户最终目标是做分析，先用本技能找到目标年报，再切到 `clawshire-annual-analysis`。
5. 返回给 Agent 时，优先 `--output json`，保留 `met_uuid`、`company_code`、`pdf_url`。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 查某公司某年年报 | `clawshire annual-report latest --year <YYYY> --keyword <kw>` |
| 按交易所过滤 | `clawshire annual-report latest --year <YYYY> --exchange <ex> --keyword <kw>` |
| 查结构化数据 | `clawshire annual-report data <met_uuid>` |
| 返回结构化 JSON | `clawshire --output json annual-report ...` |

## Decision Tree

```
用户现在缺什么？
├── 缺年报定位结果 → annual-report latest
├── 已有 met_uuid → annual-report data
└── 其实要提交分析任务 → 先 latest，再切 annual-analysis
```

## Common Workflows

### 先找到某公司的年报

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行 --page-size 3
```

### 返回 JSON 供脚本继续处理

```bash
clawshire --output json annual-report latest --year 2025 --keyword 000001
```

### 用 met_uuid 查询结构化年报

```bash
clawshire --output json annual-report data 10fd860b-c12e-54b3-a5b3-38c2ecdf5b2b
```

## Output Rules

- 面向用户：至少给出公司名、证券代码、发布时间、PDF 链接。
- 面向脚本：保留 `met_uuid` 作为后续分析和追踪的主键。
- 若结果有多条，优先解释为什么命中多条，再建议用户缩小关键词或年份。

## References

- 命令与示例：[`references/commands.md`](references/commands.md)
- 输出规则：[`references/output.md`](references/output.md)
