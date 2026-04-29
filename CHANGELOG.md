# Changelog

## [Unreleased]

### 📝 Documentation

- README 精简安装说明，按"个人用户/AI Agent"两条路径重构快速上手
- README 新增 Star History 区块
- README 新增"通过自然语言让 Agent 安装和使用"小节，提供通用安装资源模板
- pyproject.toml 新增 `[project.urls]`（Homepage/Repository/Issues/Changelog）

## [0.2.0] - 2026-04-28

### ✨ Features

- `feedback` 命令：提交 Agent 执行反馈（--job-id / --agent / --rating / --comment）
- `auth` 交互式引导配置，首次运行无配置时自动提示输入 API Key
- `auth` 命令提示语改为英文，提升国际化体验
- `--output` / `-o` 格式参数支持 `json` / `text` / `markdown`

### 📝 Documentation

- README 更新开源仓库地址（memect/clawshire-cli），补充 GitHub stars 徽章
- README 改写为公开发布版本，补充安装说明与快速上手示例

## [0.1.0] - 2026-04-27

### ✨ Features

- Initial public release
- `notice` — 公告检索（按日期、证券代码、PDF 链接）
- `annual-report` — 年报列表与结构化数据查询
- `annual-analysis` — 年报 AI 分析任务（本地 PDF / PDF 链接 / 按公司）
- `user` — 用户信息与配额查询
- `auth` — API Key 管理
- `update` — 自动升级
- Python SDK (`clawshire_sdk`) 随包附带
- 4 个 Agent Skills（`skills/` 目录）
