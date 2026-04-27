# ClawShire CLI

[![PyPI version](https://img.shields.io/pypi/v/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![Python](https://img.shields.io/pypi/pyversions/clawshire-cli)](https://pypi.org/project/clawshire-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/memect/clawshire-cli)](https://github.com/memect/clawshire-cli/issues)
[![GitHub stars](https://img.shields.io/github/stars/memect/clawshire-cli)](https://github.com/memect/clawshire-cli)

**clawshire-cli** 是 ClawShire 开源的命令行工具，支持人类用户和 AI Agent 在终端查询 A 股上市公司公告与年报数据。

核心亮点：

- 覆盖公告检索、年报定位、年报结构化数据、AI 智能分析等核心能力
- 内置 4 个 Agent Skills，开箱即用，适配主流 AI 工具
- 同时提供 Python SDK，安装 CLI 即可在代码中直接调用
- `pip install clawshire-cli` 即可安装，支持 `clawshire` 和 `cs` 两个入口

---

## 能力概览

| 能力域 | 说明 |
| --- | --- |
| 公告检索 | 按日期范围、证券代码、PDF 链接查询沪深北三市公告 |
| 年报查询 | 按公司名称或代码定位年报列表，获取结构化数据 |
| 年报 AI 分析 | 上传本地 PDF、PDF 链接或按公司发起智能分析任务 |
| 用户与认证 | API Key 管理、用户信息、配额查询 |

---

## 安装

要求：`Python >= 3.12`

推荐使用 `uv`（隔离环境）：

```bash
uv tool install clawshire-cli
```

或使用 pip：

```bash
pip install clawshire-cli
```

安装后提供两个等价入口：

```bash
clawshire --help
cs --help
```

升级：

```bash
clawshire update
```

---

## 快速上手

```bash
# 1. 注册并获取 API Key：https://clawshire.cn
# 2. 配置
clawshire auth set-key <your_api_key>
# 3. 验证
clawshire user info
# 4. 查公告
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402
# 5. 查年报
clawshire annual-report latest --year 2025 --keyword 平安银行
# 6. 发起年报 AI 分析
clawshire annual-analysis company 000001 --year 2025
```

### 在 AI Agent 中使用

Agent 使用前需确认已配置 API Key（环境变量或本地配置文件均可）：

```bash
export CLAWSHIRE_API_KEY="<your_api_key>"
clawshire auth check   # 退出码 0 = 认证可用
```

推荐安装配套 Skills bundle，让 Agent 直接调用工作流：

```bash
npx skills add memect/clawshire-cli -y -g
```

---

## 认证

```bash
clawshire auth set-key <key>   # 保存 API Key 到本地
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
clawshire notice search --start-date 2026-04-01 --end-date 2026-04-20 --keyword 603402

# 按证券代码查询
clawshire notice stock 000001 --start-date 2026-04-01 --end-date 2026-04-20

# 按公告 PDF 链接查询
clawshire notice link --met-link https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
```

### 年报查询

```bash
# 查年报列表
clawshire annual-report latest --year 2025 --keyword 平安银行

# 查年报结构化数据
clawshire annual-report data <met_uuid>
```

### 年报 AI 分析

```bash
# 按公司发起分析（推荐）
clawshire annual-analysis company 000001 --year 2025

# 通过本地 PDF 发起
clawshire annual-analysis pdf-file ./report.pdf

# 通过 PDF 链接发起
clawshire annual-analysis pdf-url https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF

# 查询分析任务状态
clawshire annual-analysis get <task_id_or_job_id>
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

全局参数 `--output` 必须放在子命令**前面**：

```bash
clawshire --output json notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402
clawshire --output json annual-report latest --year 2025 --keyword 平安银行
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

---

## 配置

支持环境变量：

| 变量 | 说明 |
| --- | --- |
| `CLAWSHIRE_API_KEY` | API Key |
| `CLAWSHIRE_BASE_URL` | API 地址（默认 `https://api.clawshire.cn`） |
| `CLAWSHIRE_OUTPUT` | 输出格式（`text` / `json`） |
| `CLAWSHIRE_TIMEOUT` | HTTP 超时（秒） |

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

全局参数要放在子命令前面：

```bash
# 正确
clawshire --output json notice search --start-date 2026-04-19 --end-date 2026-04-20
```

### `未找到与 XXX 匹配的年报`

```bash
clawshire annual-report latest --year 2025 --keyword 000001
```

如果仍找不到，去掉 `--exchange` 参数再试。

---

## 发布

```bash
# 修改 pyproject.toml 中的 version，然后：
cd clawshire-cli
uv build
uv publish

# 发布到 TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/
```

本地验证：

```bash
uv tool install .
clawshire --help
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402
```

---

## 测试

```bash
./scripts/e2e_local_check.sh
```

脚本执行：测试集 → CLI 基础命令检查 → skills 目录结构检查。若环境中存在 `CLAWSHIRE_API_KEY`，还会执行真实线上链路验证。

完整测试说明见 [`docs/local-e2e.md`](docs/local-e2e.md)。
