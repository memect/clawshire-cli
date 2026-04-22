---
name: clawshire-data-query
version: 1.0.0
description: "ClawShire 公告数据查询技能。通过 clawshire CLI 查询 A 股上市公司公告，支持按日期范围、证券代码、公告原文链接检索结构化提取结果。"
triggers: ["clawshire notice", "公告查询", "查公告", "最近公告", "证券代码公告", "公告 pdf", "notice search", "notice stock", "notice link"]
invocable: true
argument-hint: "[search|stock|link] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire notice --help"
---

# /clawshire-data-query - Notice Query

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)，其中包含安装、认证、错误处理与安全规则。**

通过 `clawshire` CLI 查询 A 股上市公司公告及其结构化提取结果。

## Agent Invariants

1. 先判断用户给的是日期范围、证券代码，还是公告 PDF 链接。
2. 用户给了证券代码时，优先 `notice stock`，比裸 `search` 更收敛。
3. 用户给了公告 PDF 直链时，直接用 `notice link`，不要先走日期搜索。
4. 默认控制结果规模；若用户没有明确要全量数据，不要主动加 `--page-all`。
5. 如果下一步目标其实是查年报或做年报分析，切到对应年报技能，不要继续在公告技能里兜圈子。
6. 给脚本或 Agent 返回结果时，优先 `clawshire --output json ...`。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 按日期范围查公告 | `clawshire notice search --start-date <d> --end-date <d>` |
| 按证券代码查公告 | `clawshire notice stock <sec_code> --start-date <d> --end-date <d>` |
| 按 PDF 链接回查 | `clawshire notice link --met-link <url>` |
| 返回结构化 JSON | `clawshire --output json notice ...` |

## Decision Tree

```
用户给了什么输入？
├── 证券代码 + 日期范围 → notice stock
├── 只有日期范围 / 公告类型 / 关键词 → notice search
├── 公告 PDF 链接 → notice link
└── 其实想查年报 / 做分析 → 切到年报 skill
```

## Common Workflows

### 查某家公司近期公告

```bash
clawshire notice stock 603402 --start-date 2026-04-01 --end-date 2026-04-20 --page-size 5
```

### 查某段时间内带关键词的公告

```bash
clawshire --output json notice search --start-date 2026-04-01 --end-date 2026-04-20 --keyword 603402
```

### 用公告原文链接回查

```bash
clawshire --output json notice link --met-link http://static.cninfo.com.cn/finalpage/2026-04-20/1225124234.PDF
```

## Output Rules

- 面向用户：至少总结公司名、标题、公告日期、原文链接。
- 面向脚本：优先 `--output json`。
- 查询范围较大时，优先先缩小日期范围或证券代码，再考虑 `--page-all`。

## References

- 命令与示例：[`references/commands.md`](references/commands.md)
- 输出与路由规则：[`references/routing.md`](references/routing.md)
