# ClawShire CLI

[![PyPI version](https://img.shields.io/pypi/v/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![Python](https://img.shields.io/pypi/pyversions/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/memect/clawshire-cli)](https://github.com/memect/clawshire-cli/issues)
[![GitHub stars](https://img.shields.io/github/stars/memect/clawshire-cli)](https://github.com/memect/clawshire-cli)

**clawshire-cli** 是 ClawShire 开源的命令行工具，用于查询 A 股上市公司公告、年报、公告 Wiki 知识库和投资逻辑研判，同时提供 Python SDK 和 Agent Skills。

- 官网：<https://clawshire.cn>
- PyPI：<https://pypi.org/project/clawshire-cli/>
- 更新日志：[CHANGELOG.md](CHANGELOG.md) · 贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md) · [MIT License](LICENSE)

| 能力域 | 说明 |
| --- | --- |
| 公告查询 | 按日期范围、证券代码、PDF 链接查询沪深北三市公告 |
| 年报查询 | 按公司名称或代码定位年报列表，获取结构化数据 |
| 年报 AI 分析 | 上传本地 PDF、PDF 链接或按公司发起智能分析任务 |
| 公告 Wiki | 公司画像、公告详情、Tag 主题、结构化事实 |
| 投资逻辑分析 | 基于价值投资方法论的公告 delta 研判，含行业景气汇总 |

---

## 安装

要求：`Python >= 3.12`

```bash
uv tool install clawshire-cli   # 推荐
# 或
pip install clawshire-cli
```

安装后提供两个等价入口：`clawshire` 和 `cs`。

---

## 快速上手

**第 1 步：获取 API Key**

前往 <https://clawshire.cn> 注册，免费赠送 100 次调用额度。

**第 2 步：配置认证**

```bash
clawshire auth set-key <your_api_key>
```

**第 3 步：开始查询**

```
$ clawshire notice stock 000001 --start-date 2026-05-01 --end-date 2026-05-31

sec_code: 000001  total: 1

met_uuid                             | sec_code | sec_name | met_title                                        | met_date
-------------------------------------+----------+----------+--------------------------------------------------+----------
bebf7a2f-3eb2-5efe-b4a2-4ffde446c166 | 000001   | 平安银行   | 北京市海问律师事务所关于平安银行股份有限公司2025年年度股东会的法律意见书 | 2026-05-23
```

---

## 命令

### 命令分组与简写

| 分组 | 简写 | 说明 |
| --- | --- | --- |
| `notice` | `gg` | 公告检索 |
| `annual-report` | `ar` | 年报查询 |
| `annual-analysis` | `aa` | 年报 AI 分析 |
| `wiki` | — | 公告 Wiki 知识库 |
| `investment` | — | 投资逻辑分析 |

### 公告检索

```bash
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --keyword 603402
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --infotype 年度报告
clawshire notice stock 000001 --start-date 2025-01-01 --end-date 2025-01-31
clawshire notice link --met-link https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
clawshire notice detect-events --sec-code 000001 --start-date 2025-01-01 --end-date 2025-01-31
clawshire notice search --start-date 2025-01-01 --end-date 2025-01-31 --keyword 000001 --page-all
```

### 年报查询

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行
clawshire annual-report latest --year 2025 --exchange bj
clawshire annual-report data <met_uuid>
```

### 年报 AI 分析

```bash
clawshire annual-analysis company 000001 --year 2025          # 发起分析
clawshire annual-analysis company 000001 --year 2025 --wait   # 等待完成
clawshire annual-analysis pdf-file ./report.pdf               # 本地 PDF
clawshire annual-analysis pdf-url <pdf_url>                   # PDF 链接
clawshire annual-analysis get <task_id>                       # 查询进度
clawshire annual-analysis get <task_id> --save-report-to ./report.html
```

> `pdf-file` / `pdf-url` 返回 `job_id`；`company` 返回 `task_id`，后续查询传对应 ID。

### 公告 Wiki

```bash
clawshire wiki company 000001                                 # 公司画像
clawshire wiki entry <ann_id>                                 # 公告详情
clawshire wiki search --code 000001 --date-from 2026-01-01   # 搜索
clawshire wiki search --q 退市风险 --quality-min 3
clawshire wiki tag 退市风险                                    # Tag 主题页
clawshire wiki backlinks company 000001                       # 反链查询
clawshire wiki resolve 平安银行                               # 别名解析
clawshire wiki special statistics                             # 知识库统计
```

### 投资逻辑分析

```bash
clawshire investment industries                               # 行业名称列表（先查，免费）
clawshire investment company 000001 --size 10 --format json  # 公司研判变化
clawshire investment summary 000001 --format json             # 公司综合研判
clawshire investment industry 银行 --format json              # 行业景气研判
```

> 查询行业研判前，先用 `investment industries` 确认申万一级行业标准名。

### 其他

```bash
clawshire user info     # 用户信息与配额
clawshire update        # 升级到最新版
clawshire auth --help   # 认证相关命令
```

---

## 认证

```bash
clawshire auth set-key <key>   # 保存 API Key
clawshire auth check           # 检查认证可用性（退出码 0=ok）
clawshire auth show            # 查看当前配置
clawshire auth clear-key       # 清除本地 key
```

CI / 脚本 / Agent 工作流推荐通过环境变量传入，不要写入源码或公开仓库：

```bash
export CLAWSHIRE_API_KEY="<your_api_key>"
```

---

## 输出格式

`--format` 放在具体命令后面，支持 `table`（默认）、`json`、`markdown`、`csv`：

```bash
clawshire notice stock 000001 --start-date 2026-04-01 --end-date 2026-04-20 --format json
```

`--json` 是 `--format json` 的快捷写法。JSON 输出适合脚本和 Agent 工作流，建议按字段名读取，不依赖字段顺序。

---

## Python SDK

安装 `clawshire-cli` 后 SDK 随包附带：

```python
from clawshire_sdk import ClawShireClient

client = ClawShireClient(base_url="https://api.clawshire.cn", api_key="your_api_key")

# 公告查询
data = client.filings.search(start_date="2026-04-01", end_date="2026-04-20", keyword="603402")

# 年报
reports = client.annual.latest(year=2025, keyword="平安银行", page_size=1)
task = client.annual.analyze_company("000001", year=2025)

# 公告 Wiki
profile = client.wiki.company("000001")

# 投资逻辑
industries = client.investment.industries()
deltas = client.investment.company_deltas("000001", size=10)
thesis = client.investment.industry_thesis("银行")
```

完整 SDK 文档见 [`docs/sdk-usage.md`](docs/sdk-usage.md)。

---

## Agent Skills

`clawshire-cli` 仓库同时维护配套 Agent Skills，位于 `skills/` 目录：

| Skill | 说明 |
| --- | --- |
| `clawshire-shared` | 共享规则：认证、输出格式、错误处理 |
| `clawshire-data-query` | 公告数据查询 |
| `clawshire-annual-report` | 年报定位 |
| `clawshire-annual-analysis` | 年报 AI 分析 |
| `clawshire-wiki` | 公告 Wiki 知识库查询 |
| `clawshire-investment` | 投资逻辑分析 |

安装：

```bash
npx skills add memect/clawshire-cli -y -g
export CLAWSHIRE_API_KEY="<your_api_key>"
```

安装后可在 Claude Code、Cursor 等支持 Shell 的 Agent 中直接用自然语言调用：

```text
帮我查 603402 在 2026-06-01 到 2026-06-02 之间发布的公告，返回标题和 PDF 链接。
```

```text
000001 最近有什么投资逻辑上的变化？
```

---

## 配置

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

提交 PR 前运行端到端检查：

```bash
./scripts/e2e_local_check.sh
```

更多说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 说明

数据来源于上市公司公开披露文件，可能存在延迟或误差，重要决策请以交易所、巨潮资讯正式文件为准。年报 AI 分析结果和投资逻辑研判不构成投资建议。

---

## 支持

- Bug 和功能建议：[GitHub Issues](https://github.com/memect/clawshire-cli/issues)
- 贡献代码：[CONTRIBUTING.md](CONTRIBUTING.md)
- 安全问题请通过官网联系方式私下报告，不要公开披露漏洞。

---

## 常见问题

**`认证失败: Authorization 格式错误`**

```bash
clawshire auth clear-key
clawshire auth set-key <your_api_key>
```

**`该命令需要 API Key`**

```bash
clawshire auth set-key <your_api_key>
```

**`unrecognized arguments: --output json`**

`--output` 已改为 `--format`，放在具体命令后面：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --format json
```

**`未找到与 XXX 匹配的年报`**

```bash
clawshire annual-report latest --year 2025 --keyword 000001   # 用证券代码替代公司名
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=memect/clawshire-cli&type=Date)](https://star-history.com/#memect/clawshire-cli&Date)
