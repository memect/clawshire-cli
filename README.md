# ClawShire CLI

[![PyPI version](https://img.shields.io/pypi/v/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![Python](https://img.shields.io/pypi/pyversions/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/memect/clawshire-cli)](https://github.com/memect/clawshire-cli/issues)
[![GitHub stars](https://img.shields.io/github/stars/memect/clawshire-cli)](https://github.com/memect/clawshire-cli)

**clawshire-cli** 是 ClawShire 开源的命令行工具，支持用户、开发者和 AI Agent 在终端查询 A 股上市公司的临时公告、年报数据，并发起年报智能分析。

相关链接：

- 官网：<https://clawshire.cn>
- PyPI：<https://pypi.org/project/clawshire-cli/>
- Issues：<https://github.com/memect/clawshire-cli/issues>
- 更新日志：[CHANGELOG.md](CHANGELOG.md)
- 贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md)
- 许可证：[MIT License](LICENSE)

ClawShire 面向上市公司信息披露数据的程序化使用场景。A 股上市公司会持续发布临时公告、定期报告等公开文件，但原始公告通常分散在交易所、巨潮资讯等渠道，人工检索、下载、比对和结构化处理成本较高。`clawshire-cli` 将这些能力封装为稳定的命令行入口，适合投研、风控、财务分析、舆情监控、数据工程和 AI Agent 工作流使用。

当前重点支持：

- A 股上市公司临时公告查询：按日期范围、证券代码、公司名称或公告 PDF 链接检索公告数据
- 年报数据查询：按公司名称、证券代码、年份定位年报，并获取结构化年报数据
- 年报数据分析：基于本地 PDF、PDF 链接或公司年报自动发起 AI 分析任务

核心亮点：

- 覆盖临时公告检索、年报定位、年报结构化数据、AI 智能分析等核心能力
- 内置 4 个 Agent Skills，开箱即用，适配主流 AI 工具
- 同时提供 Python SDK，安装 CLI 即可在代码中直接调用
- `pip install clawshire-cli` 即可安装，支持 `clawshire` 和 `cs` 两个入口

---

## 能力概览

| 能力域 | 说明 |
| --- | --- |
| 临时公告查询 | 按日期范围、证券代码、公司名称、PDF 链接查询沪深北三市公告 |
| 年报查询 | 按公司名称或代码定位年报列表，获取结构化数据 |
| 年报 AI 分析 | 上传本地 PDF、PDF 链接或按公司发起智能分析任务 |
| 用户与认证 | API Key 管理、用户信息、配额查询 |

---

## 安装 & 快速上手

安装后可在终端、脚本或 AI Agent 工作流中调用 ClawShire 的公告查询、年报查询和年报 AI 分析能力。首次使用需要 API Key，可在 <https://clawshire.cn> 获取。

要求：`Python >= 3.12`

```bash
# 推荐（uv 隔离环境）
uv tool install clawshire-cli

# 或 pip
pip install clawshire-cli
```

安装后提供两个等价入口：`clawshire` 和 `cs`。升级：`clawshire update`

### 个人用户（3 步）

```bash
# 第 1 步：注册并获取 API Key：https://clawshire.cn
# 第 2 步：配置认证（交互式引导）
clawshire auth

# 第 3 步：验证并开始使用
clawshire user info
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --keyword 000001
```

### AI Agent（3 步）

```bash
# 第 1 步：安装 CLI 和 Skills bundle
pip install clawshire-cli
npx skills add memect/clawshire-cli -y -g

# 第 2 步：配置 API Key（环境变量，推荐）
export CLAWSHIRE_API_KEY="<your_api_key>"

# 第 3 步：验证认证可用性（退出码 0 = 可用）
clawshire auth check
```

---

## 认证

```bash
clawshire auth                 # 交互式引导配置（推荐首次使用）
clawshire auth set-key <key>   # 直接保存 API Key 到本地
clawshire auth show            # 查看当前配置（key 掩码、base_url 等）
clawshire auth status          # 查看 key 来源与认证状态
clawshire auth check           # 检查认证可用性（退出码 0=ok）
clawshire auth whoami          # 校验当前 key 是否有效
clawshire auth clear-key       # 清除本地保存的 key
clawshire auth logout          # clear-key 的别名
```

临时使用（不落盘）：

```bash
export CLAWSHIRE_API_KEY="<your_api_key>"
# 或单次传参
clawshire --api-key <your_api_key> user info
```

不要把 API Key 写入源码、日志、公开仓库或可共享的 Agent 配置。CI、脚本和 Agent 工作流中推荐通过环境变量传入。

---

## 命令

### 命令分组与简写

| 分组 | 简写 | 说明 |
| --- | --- | --- |
| `notice` | `gg` | 公告检索 |
| `annual-report` | `ar` | 年报查询 |
| `annual-analysis` | `aa` | 年报 AI 分析 |

### 公告检索

```bash
# 按日期范围查询（keyword 可传证券代码或公司名）
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --keyword 603402

# 按公告类别过滤
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --infotype 年度报告

# 自动翻页获取全部结果
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --keyword 000001 --page-all

# 按证券代码查询
clawshire notice stock 000001 --start-date 2025-01-01 --end-date 2025-01-31

# 按公告 PDF 链接查询
clawshire notice link --met-link https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
```

### 年报查询

```bash
# 查年报列表
clawshire annual-report latest --year 2025 --keyword 平安银行

# 按交易所过滤（sz / sh / bj）
clawshire annual-report latest --year 2025 --exchange bj

# 查年报结构化数据
clawshire annual-report data <met_uuid>
```

### 年报 AI 分析

```bash
# 按公司发起分析（推荐）
clawshire annual-analysis company 000001 --year 2025

# 指定报告语言（zh / en，默认 zh）
clawshire annual-analysis company 000001 --year 2025 --lang en

# 阻塞等待分析完成
clawshire annual-analysis company 000001 --year 2025 --wait

# 分析完成后发送邮件通知
clawshire annual-analysis company 000001 --year 2025 --notify-email you@example.com

# 通过本地 PDF 发起
clawshire annual-analysis pdf-file ./report.pdf

# 通过 PDF 链接发起
clawshire annual-analysis pdf-url https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF

# 查询分析任务状态
clawshire annual-analysis get <task_id_or_job_id>

# 查询并保存 HTML 报告
clawshire annual-analysis get <task_id_or_job_id> --save-report-to ./report.html
```

> `pdf-file` / `pdf-url` 返回 `job_id`；`company` 返回 `task_id`，后续查询传对应 ID。

### 用户信息

```bash
clawshire user info
```

### 升级

```bash
clawshire update           # 升级到最新版
clawshire update --dry-run # 预览将执行的操作
clawshire update -y        # 跳过确认
```

---

## 输出格式

`--format` 是具体命令的展示参数，放在业务参数后面：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402 --format json
clawshire annual-report latest --year 2025 --keyword 平安银行 --format json
```

支持的格式：`table`、`json`、`markdown`、`csv`。也可以使用 `--json` 作为 `--format json` 的快捷写法：

```bash
clawshire user info --json
```

JSON 输出适合脚本、CI 和 Agent 工作流处理。示例：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402 --format json
```

返回结构会随接口能力扩展，自动化脚本建议按字段名读取必要字段，不要依赖字段顺序：

```json
{
  "total": 1,
  "items": [
    {
      "met_uuid": "example-met-uuid",
      "sec_code": "603402",
      "sec_name": "示例公司",
      "announcement_title": "示例公告标题",
      "announcement_time": "2026-04-20",
      "pdf_url": "https://static.cninfo.com.cn/finalpage/example.PDF"
    }
  ]
}
```

---

## Python SDK

安装 `clawshire-cli` 后 SDK 随包附带，无需单独安装：

```python
from clawshire_sdk import ClawShireClient

client = ClawShireClient(
    base_url="https://api.clawshire.cn",
    api_key="your_api_key",
)

# 查年报
reports = client.annual.latest(year=2025, keyword="平安银行", page_size=1)
print(reports["items"][0]["pdf_url"])

# 发起分析
task = client.annual.analyze_company("000001", year=2025)
print(task["task_id"])

# 查公告
data = client.filings.search(
    start_date="2026-04-01",
    end_date="2026-04-20",
    keyword="603402",
)
print(data["total"])
```

SDK 暴露两组域能力：

- `client.filings` — 公告查询
- `client.annual` — 年报查询与分析

完整 SDK 文档见 [`docs/sdk-usage.md`](docs/sdk-usage.md)。

---

## Agent Skills

`clawshire-cli` 仓库同时维护配套 Agent Skills，位于 `skills/` 目录：

| Skill | 说明 |
| --- | --- |
| `clawshire-shared` | 共享规则：认证、输出格式、错误处理 |
| `clawshire-data-query` | 公告数据查询工作流 |
| `clawshire-annual-report` | 年报定位工作流 |
| `clawshire-annual-analysis` | 年报 AI 分析工作流 |

推荐按整个仓库安装 skills bundle：

```bash
npx skills add memect/clawshire-cli -y -g
```

Skills 复用 `clawshire` CLI，将公告查询、年报定位、年报分析组织成适合 Agent 调用的工作流，而不是各自维护独立 HTTP 脚本。

安装后，可以直接在支持 Skills 的 Agent 中用自然语言调用，例如：

```text
帮我查询 603402 在 2026-04-01 到 2026-04-20 之间发布的公告，返回标题、日期和 PDF 链接。
```

```text
帮我查找平安银行 2025 年年报，并提取年报 PDF 链接和 met_uuid。
```

```text
请基于 000001 的 2025 年年报发起一份中文 AI 分析，完成后告诉我任务 ID。
```

Agent 会根据任务选择对应 Skill，并通过本地 `clawshire` 命令完成查询或分析。使用前请确保运行环境中已经配置 `CLAWSHIRE_API_KEY`，或已经通过 `clawshire auth` 保存过 API Key。

---

## 配置

支持环境变量：

| 变量 | 说明 |
| --- | --- |
| `CLAWSHIRE_API_KEY` | API Key |
| `CLAWSHIRE_BASE_URL` | API 地址（默认 `https://api.clawshire.cn`） |
| `CLAWSHIRE_FORMAT` | 输出格式（`table` / `json` / `markdown` / `csv`） |
| `CLAWSHIRE_TIMEOUT` | HTTP 超时（秒） |

---

## 本地开发

```bash
git clone https://github.com/memect/clawshire-cli.git
cd clawshire-cli
uv sync
uv run pytest
uv run clawshire --help
```

提交 PR 前建议运行端到端检查：

```bash
./scripts/e2e_local_check.sh
```

更多说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 使用数据前请了解

`clawshire-cli` 主要处理上市公司公开披露的信息。公告、年报和结构化结果可能因为来源更新、发布时间、解析过程或网络服务等原因出现延迟、缺失或误差。用于投研、风控、财务分析或生产流程前，请再对照交易所、巨潮资讯或上市公司正式披露文件复核。

使用年报 AI 分析时，CLI 可能会把本地 PDF、PDF 链接或公司年报标识发送到 ClawShire 服务，用来生成分析结果。请不要上传无权处理的文件、未公开资料或包含敏感信息的文档。上传文件、任务结果和 API 日志的处理方式以 ClawShire 服务条款和隐私政策为准。

CLI 和 AI 分析结果只作为信息整理和分析辅助，不构成投资建议、法律意见、审计意见或财务顾问意见。

---

## 支持与安全

- Bug 和功能建议请提交到 [GitHub Issues](https://github.com/memect/clawshire-cli/issues)。
- 代码贡献请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 如果发现安全问题，请不要公开披露漏洞细节，建议通过 ClawShire 官网联系方式或项目维护者渠道私下报告。

---

## 常见问题

### `认证失败: Authorization 格式错误`

```bash
clawshire auth show
clawshire auth clear-key
clawshire auth set-key <your_api_key>
```

### `该命令需要 API Key`

```bash
clawshire auth set-key <your_api_key>
# 或临时传参
clawshire --api-key <your_api_key> user info
```

### `unrecognized arguments: --output json`

`--output` 已改为 `--format`，并放在具体命令后面：

```bash
# 正确
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --format json
```

### `未找到与 XXX 匹配的年报`

尝试用证券代码代替公司名称：

```bash
clawshire annual-report latest --year 2025 --keyword 000001
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=memect/clawshire-cli&type=Date)](https://star-history.com/#memect/clawshire-cli&Date)
