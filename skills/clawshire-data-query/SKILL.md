---
name: clawshire-data-query
version: 1.0.0
description: "ClawShire 公告数据查询技能。通过 clawshire CLI 查询 A 股上市公司公告，支持按日期范围、证券代码、公告原文链接检索结构化提取结果。"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire notice --help"
---

# ClawShire 公告数据查询技能

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)，其中包含安装、认证、错误处理与安全规则。**

本技能用于通过 `clawshire` CLI 查询 A 股上市公司公告及其结构化提取结果。

适用场景：

- 查询某天或某段时间内的公告
- 查询某个证券代码近期公告
- 用户已经有公告 PDF 链接，想直接回查结构化结果

优先路由：

1. 用户要“看某家公司最近公告”，优先用 `notice stock`
2. 用户要“查某一天/某一段时间所有公告”，优先用 `notice search`
3. 用户已经给出 PDF 直链，优先用 `notice link`
4. 用户下一步不是查公告，而是查年报或做年报分析，应切换到对应年报技能

需要时再读取：

- 命令与示例：[`references/commands.md`](references/commands.md)
- 输出与路由规则：[`references/routing.md`](references/routing.md)
