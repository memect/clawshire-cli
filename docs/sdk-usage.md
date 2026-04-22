# ClawShire SDK Usage

`clawshire-cli` 仓库里同时包含 Python SDK，包名为 `clawshire_sdk`。

如果你不想通过 CLI 子进程调用，而是希望在 Python 代码里直接访问公告查询、年报查询、年报分析能力，可以直接使用这个 SDK。

## 安装

如果已经安装了 `clawshire-cli`，SDK 会一起安装，无需单独装第二个包：

```bash
pip install clawshire-cli
```

或：

```bash
uv tool install clawshire-cli
```

如果你是在项目源码里开发：

```bash
cd clawshire-cli
uv sync
```

## 基本初始化

最小示例：

```python
from clawshire_sdk import ClawShireClient

client = ClawShireClient(
    base_url="https://api.clawshire.cn",
    api_key="your_api_key",
    timeout=30.0,
)
```

参数说明：

- `base_url`: API 地址，当前线上默认是 `https://api.clawshire.cn`
- `api_key`: 可选。查询公告时可以不传；查用户、查年报、做分析时需要
- `timeout`: HTTP 超时，单位秒

## SDK 结构

`ClawShireClient` 当前暴露两组域能力：

- `client.filings`: 公告查询
- `client.annual`: 年报查询与年报分析

也保留了通用 HTTP 方法：

- `client.get(...)`
- `client.post(...)`
- `client.download(...)`

通常更推荐直接走 domain 方法，而不是自己手写 path。

## 公告查询

### 按日期范围查询

```python
from clawshire_sdk import ClawShireClient

client = ClawShireClient(base_url="https://api.clawshire.cn")

data = client.filings.search(
    start_date="2026-04-01",
    end_date="2026-04-20",
    keyword="603402",
    page=1,
    page_size=3,
)

print(data["total"])
print(data["items"][0]["met_title"])
```

### 按证券代码查询

```python
data = client.filings.stock(
    "603402",
    start_date="2026-04-01",
    end_date="2026-04-20",
    page=1,
    page_size=3,
)
```

### 按公告 PDF 链接查询

```python
data = client.filings.link(
    "http://static.cninfo.com.cn/finalpage/2026-04-20/1225124234.PDF"
)
```

## 年报查询

年报查询需要 API Key。

### 查询年报列表

```python
from clawshire_sdk import ClawShireClient

client = ClawShireClient(
    base_url="https://api.clawshire.cn",
    api_key="your_api_key",
)

data = client.annual.latest(
    year=2025,
    keyword="平安银行",
    page=1,
    page_size=3,
)

for item in data["items"]:
    print(item["company_name"], item["met_uuid"], item["pdf_url"])
```

### 查询单份年报结构化数据

```python
report = client.annual.data("10fd860b-c12e-54b3-a5b3-38c2ecdf5b2b")
print(report)
```

## 年报分析

### 通过公司代码或简称发起分析

这是当前最推荐的方式。

```python
task = client.annual.analyze_company(
    "000001",
    year=2025,
)

print(task["task_id"])
print(task["selected_report"]["company_name"])
```

返回结果里通常会带：

- `task_id`
- `message`
- `selected_report`

### 通过本地 PDF 发起分析

```python
job = client.annual.analyze_submit("./report.pdf", lang="zh")
print(job["job_id"])
```

如果你已经拿到了 PDF 二进制，也可以直接传 bytes：

```python
content = open("./report.pdf", "rb").read()
job = client.annual.analyze_submit_bytes(
    content,
    filename="report.pdf",
    lang="zh",
)
```

### 通过 PDF 链接发起分析

```python
job = client.annual.analyze_submit_pdf_url(
    "https://example.com/report.pdf",
    lang="zh",
)
```

注意：

- 这个方法会先下载 PDF，再上传到分析接口
- 若上游 PDF 地址不可访问，会直接抛 `ClawShireNetworkError`
- 对生产场景，通常更建议优先用 `analyze_company(...)`

### 查询分析任务状态

如果你拿到的是 `job_id`：

```python
job_result = client.annual.analyze_get("27")
print(job_result["status"])
```

如果你拿到的是 `task_id`：

```python
task_result = client.annual.get_analysis_task(74)
print(task_result["status"])
```

### 下载分析报告

当任务状态完成且有 `report_url` 时：

```python
saved = client.annual.download_report(
    met_uuid="10fd860b-c12e-54b3-a5b3-38c2ecdf5b2b",
    report_url="https://example.com/report.html",
    company_name="平安银行",
)

print(saved)
```

如果不传 `dest`，默认会按以下格式生成文件名：

```text
<company_name>-<met_uuid>.html
```

## 错误处理

SDK 当前统一抛这些异常：

```python
from clawshire_sdk import (
    ClawShireApiError,
    ClawShireAuthError,
    ClawShireConfigError,
    ClawShireNetworkError,
)
```

推荐写法：

```python
from clawshire_sdk import (
    ClawShireApiError,
    ClawShireAuthError,
    ClawShireClient,
    ClawShireConfigError,
    ClawShireNetworkError,
)

client = ClawShireClient(
    base_url="https://api.clawshire.cn",
    api_key="your_api_key",
)

try:
    data = client.annual.latest(year=2025, keyword="平安银行")
    print(data)
except ClawShireConfigError as exc:
    print("配置错误:", exc)
except ClawShireAuthError as exc:
    print("认证失败:", exc)
except ClawShireNetworkError as exc:
    print("网络错误:", exc)
except ClawShireApiError as exc:
    print("接口错误:", exc, exc.status_code)
```

## 最小完整示例

```python
from clawshire_sdk import ClawShireClient

client = ClawShireClient(
    base_url="https://api.clawshire.cn",
    api_key="your_api_key",
)

reports = client.annual.latest(
    year=2025,
    keyword="平安银行",
    page_size=1,
)

item = reports["items"][0]
print("命中年报:", item["company_name"], item["pdf_url"])

task = client.annual.analyze_company(
    item["company_code"],
    year=2025,
)

print("分析任务已提交:", task["task_id"])
```

## 当前边界

当前 SDK 还是 `clawshire-cli` 仓库的一部分，还不是独立发布的 `clawshire-sdk` 包。

这意味着：

- 对外安装入口目前仍然是 `pip install clawshire-cli`
- SDK API 适合先跟随 CLI 一起迭代
- 如果后续要独立开源 `clawshire-sdk`，再拆包会更合适
