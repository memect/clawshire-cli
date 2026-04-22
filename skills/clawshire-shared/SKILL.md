---
name: clawshire-shared
version: 1.0.0
description: "ClawShire CLI 共享规则：安装、认证、输出格式、错误处理与安全约束。首次使用或遇到认证/配置问题时优先读取。"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire --help"
---

# ClawShire 共享规则

本技能提供所有 ClawShire CLI 场景共用的基础规则。

在执行任何 ClawShire 相关任务前，优先确认三件事：

1. 本机是否已安装 `clawshire`
2. 当前是否已经配置可用的 API Key
3. 这次调用该用哪种输出格式

需要时再读取以下参考资料：

- 安装、认证、输出格式：[`references/setup.md`](references/setup.md)
- 常见报错与处理：[`references/errors.md`](references/errors.md)

必须遵守的规则：

1. 禁止在输出中明文回显 API Key
2. 对可能产生费用或副作用的命令，先说明会发生什么
3. 对分析、上传、批量查询类操作，不要在用户意图不明确时自动扩大范围
