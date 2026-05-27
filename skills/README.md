# ClawShire Skills

该目录是 `clawshire-cli` 仓库内 Skills 的正式源码目录。

它的定位不是本地临时说明，而是：

- 跟随 `clawshire-cli` 一起开源和版本化
- 作为整仓 `skills bundle` 的分发源
- 适用于按整个仓库安装技能的分发方式

## 目录约定

每个 Skill 目录至少包含：

```text
skill-name/
├── SKILL.md
└── references/
```

其中：

- `SKILL.md`：Skill 的触发说明、核心工作流和何时读取参考资料
- `references/`：详细命令、路由、错误处理、输出规范等补充资料

## SKILL.md 模板约束

所有 Skill 都应尽量遵循同一模板，避免后续新增技能时风格漂移。

### 必备 frontmatter

每个 `SKILL.md` 顶部都应包含 YAML frontmatter，至少包含：

```yaml
---
name: clawshire-example
version: 1.0.0
description: "一句话说明这个 skill 的职责"
triggers: ["example trigger"]
invocable: true
argument-hint: "[subcommand] [args...]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire example --help"
---
```

约束如下：

- `name` 必须与目录名一致
- `version` 当前统一为 `1.0.0`
- `triggers` 不能为空
- `invocable` 当前统一为 `true`
- `argument-hint` 不能为空
- `metadata.requires.bins` 当前统一为 `["clawshire"]`
- `metadata.cliHelp` 必须是可执行的 `clawshire ... --help`

### 必备正文章节

每个 Skill 都至少包含以下章节：

- `## Agent Invariants`
- `## Quick Reference`
- `## Decision Tree`
- `## Common Workflows`
- `## References`

此外：

- 共享技能 `clawshire-shared` 应包含 `## Output Modes`
- 业务型技能应包含 `## Output Rules`

### 业务型 Skill 的额外要求

除 `clawshire-shared` 外，其他 Skill 还应满足：

- 开头显式要求先读取 `../clawshire-shared/SKILL.md`
- 明确说明何时切换到其他 skill，而不是在当前 skill 中兜圈子
- 说明何时不要扩大查询范围，例如不要默认全量拉取或重复提交任务
- 至少提供一个可执行的 `clawshire ... --format json` 样例

### 派生 Skill 的来源声明

当前 `skills/` 是 canonical source。如果未来为特定 agent 生成裁剪版或复制版 skill，派生 `SKILL.md` 必须在 frontmatter 中声明来源：

```yaml
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire notice --help"
  sourceSkill: "../../../skills/clawshire-data-query/SKILL.md"
```

约束如下：

- `sourceSkill` 必须是相对路径
- 它必须指向 canonical `skills/` 下的某个 `SKILL.md`
- 新增派生 bundle 后，应通过 `python scripts/check_skill_drift.py` 校验

### 推荐写法

建议在 `SKILL.md` 中显式写出以下信息：

- 输入类型：用户给的是证券代码、日期范围、PDF 链接，还是 `met_uuid`
- 推荐输出模式：给人看时默认表格，给 Agent/脚本时优先 `--format json`
- 路由分支：什么条件下调用哪个子命令
- 风险边界：何时可能消耗额度、上传文件或触发异步任务

### 参考结构

推荐结构如下：

```text
---
frontmatter
---

# 标题

一句话说明

## Agent Invariants
## Quick Reference
## Decision Tree
## Common Workflows
## Output Rules / Output Modes
## References
```

## 设计原则

1. `clawshire-cli/skills/` 是单一真源
2. Skills 优先复用 `clawshire` CLI，而不是各自维护独立 HTTP 脚本
3. 共享规则尽量收敛到 `clawshire-shared`
4. 任务型 Skills 只负责场景编排，不重复实现底层执行逻辑
5. 默认按整个仓库安装 skills bundle，而不是主推单个 skill 子路径安装

## 推荐安装方式

推荐安装整个仓库：

```bash
npx skills add memect/clawshire-cli -y -g
```

这类安装方式下，`skills/` 下的多个技能会一起进入本地环境，因此 `clawshire-shared` 这类共享技能可以作为 bundle 中的公共规则层存在。

## 反馈渠道

如果发现 Skill 说明不清、命令路由错误、CLI 能力缺失或 Agent 使用中被阻塞，可反馈到：agent2agi.memect@claw.163.com

## 当前技能

- `clawshire-shared`
- `clawshire-data-query`
- `clawshire-annual-report`
- `clawshire-annual-analysis`

## 后续建议

可继续补齐以下技能，与 CLI 能力域对齐：

- `clawshire-doc-extract-engine`
