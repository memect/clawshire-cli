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

## 当前技能

- `clawshire-shared`
- `clawshire-data-query`
- `clawshire-annual-report`
- `clawshire-annual-analysis`

## 后续建议

可继续补齐以下技能，与 CLI 能力域对齐：

- `clawshire-doc-extract-engine`
