---
name: clawshire-annual-report
version: 1.0.0
description: "ClawShire 年报查询技能。通过 clawshire CLI 查询年报列表与结构化年报数据，适合按年份、公司简称、证券代码快速定位年报。"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire annual-report --help"
---

# ClawShire 年报查询技能

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../clawshire-shared/SKILL.md`](../clawshire-shared/SKILL.md)，其中包含安装、认证、错误处理与安全规则。**

本技能用于通过 `clawshire` CLI 查询指定公司的年报列表，以及读取具体年报的结构化数据。

适用场景：

- 查询某家公司某一年的年报
- 通过证券代码或公司简称定位年报 PDF
- 拿到 `met_uuid` 后继续查询结构化年报数据
- 为后续 `annual-analysis` 提供输入

优先路由：

1. 用户想“先找到年报”，优先用 `annual-report latest`
2. 用户已经有 `met_uuid`，优先用 `annual-report data`
3. 用户最终目标是发起分析任务，应在找到年报后切换到 `clawshire-annual-analysis`

需要时再读取：

- 命令与示例：[`references/commands.md`](references/commands.md)
- 输出规则：[`references/output.md`](references/output.md)
