---
name: clawshire-investment
version: 1.0.0
description: "ClawShire 投资逻辑分析技能。通过 clawshire CLI 查询基于价值投资方法论的公告 delta 研判，支持公司研判变化记录、综合摘要和行业景气汇总。"
triggers: ["clawshire investment", "投资逻辑", "研判", "delta", "利好利空", "行业景气", "公司研判", "investment company", "investment industry", "多空研判"]
invocable: true
argument-hint: "[industries|company|industry|summary] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire investment --help"
---

# /clawshire-investment - Investment Logic

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)。**

通过 `clawshire` CLI 查询 A 股投资逻辑研判，基于价值投资方法论对公告做 delta 分析。

## Agent Invariants

1. 不确定行业标准名时，**必须先** `investment industries` 拿到申万一级行业列表再查，行业名须精确匹配。
2. 查公司研判时，`investment company` 返回变化历史；`investment summary` 返回综合摘要，优先用 summary 回答"这家公司投资逻辑怎么样"。
3. 研判结果是缓存数据，最新公告可能有延迟，需向用户说明。
4. 给脚本或 Agent 返回时加 `--format json`。
5. Agent 调用时命令前带 `--client skill --skill-name clawshire-investment --agent-name <name> --rationale <why>`。

## Quick Reference

| 任务 | 命令 |
|------|------|
| 获取行业名称列表（必须先查） | `clawshire investment industries` |
| 查公司研判变化记录 | `clawshire investment company <sec_code>` |
| 查公司综合研判摘要 | `clawshire investment summary <sec_code>` |
| 查行业景气研判 | `clawshire investment industry <行业名>` |

## Decision Tree

```
用户想了解什么？
├── 某家公司的投资逻辑是否有变化 → investment company <sec_code>
├── 某家公司整体投资逻辑怎么样  → investment summary <sec_code>
├── 某个行业最近景气如何        → investment industries 先确认名称
│                               → investment industry <行业名>
└── 不知道行业标准名             → investment industries 先查列表
```

## Common Workflows

### 查某家公司最近的研判变化

```bash
clawshire investment company 000001 --size 5 --format json
```

### 查行业景气（先确认行业名）

```bash
clawshire investment industries --format json
# 找到标准行业名后
clawshire investment industry 银行 --format json
```

### 查公司综合投资逻辑

```bash
clawshire investment summary 000001 --format json
```

## Output Rules

- 向用户总结 delta 方向（利好强化/利空削弱/稳定/待观察）、关键 bull/bear points。
- 行业研判总结 dominant_delta 和各公司分布。
- 明确说明数据是基于已入库公告的研判，实时性有限。

## References

- 命令与示例：[`references/commands.md`](references/commands.md)
