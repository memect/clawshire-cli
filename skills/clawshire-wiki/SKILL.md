---
name: clawshire-wiki
version: 1.0.0
description: "ClawShire 公告 Wiki 知识库查询技能。通过 clawshire CLI 查询 A 股公告结构化知识库，支持按公司、公告 ID、标签检索，返回结构化事实、事件时间线和公告全文。"
triggers: ["clawshire wiki", "公告 wiki", "wiki 查询", "公司画像", "公告事实", "结构化事实", "公告知识库", "wiki company", "wiki entry", "wiki search"]
invocable: true
argument-hint: "[search|company|entry|tag|resolve] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire wiki --help"
---

# /clawshire-wiki - Announcement Wiki

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)。**

通过 `clawshire` CLI 查询 A 股公告知识库，获取公司结构化画像、事实数据和公告详情。

## Agent Invariants

1. 用户要查"某家公司有哪些公告"或"公司最近动态"时，优先 `wiki company <sec_code>`，比逐条查 entry 更高效。
2. 用户要查"某条公告的具体内容/字段"时，用 `wiki entry <ann_id>`。
3. 不确定证券代码时，先用 `wiki resolve <公司名>` 获取 sec_code，再查 company。
4. 给脚本或 Agent 返回结果时加 `--format json`。
5. Agent 调用时命令前带 `--client skill --skill-name clawshire-wiki --agent-name <name> --rationale <why>`。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 查公司 Wiki 画像 | `clawshire wiki company <sec_code>` |
| 查公告详情 | `clawshire wiki entry <ann_id>` |
| 搜索公告 | `clawshire wiki search --code <sec_code> --ann-type <type>` |
| 别名/简称解析 | `clawshire wiki resolve <公司名>` |
| 按标签查询 | `clawshire wiki tag <tag_name>` |

## Decision Tree

```
用户要查什么？
├── 某家公司的公告列表/时间线 → wiki company <sec_code>
├── 某条具体公告的内容/字段  → wiki entry <ann_id>
├── 搜索某类公告             → wiki search --code / --ann-type / --q
├── 某个主题/Tag 的公告      → wiki tag <tag_name>
└── 不知道证券代码           → wiki resolve <公司名> 先拿 sec_code
```

## Common Workflows

### 查某家公司的公告时间线和知识统计

```bash
clawshire wiki resolve 平安银行 --format json
# 拿到 sec_code 后
clawshire wiki company 000001 --format json
```

### 查某条公告的结构化内容

```bash
clawshire wiki entry ann_20260601_000001 --format json
```

### 搜索某类公告

```bash
clawshire wiki search --code 000001 --ann-type 业绩预告 --format json
```

## Output Rules

- 向用户总结公司名、公告时间线条数、高频标签。
- 查 entry 时，至少输出标题、日期、公告类型、核心事实。
- 给脚本/Agent 用时加 `--format json`。

## References

- 命令与示例：[`references/commands.md`](references/commands.md)
