# Commands

## 推荐命令

| 命令 | 用途 |
|------|------|
| `clawshire annual-analysis pdf-file <path>` | 用本地 PDF 提交分析 |
| `clawshire annual-analysis pdf-url <url>` | 用 PDF 链接提交分析 |
| `clawshire annual-analysis company <kw> --year <YYYY>` | 自动定位年报并发起分析 |
| `clawshire annual-analysis get <id>` | 查询任务状态 |
| `clawshire --output json ...` | 返回结构化结果供脚本或 Agent 处理 |

## 按公司发起分析

这是优先推荐路径，通常比直接走 `pdf-url` 更稳定。

```bash
clawshire annual-analysis company <证券代码或简称> --year <YYYY>
```

示例：

```bash
clawshire --output json annual-analysis company 000001 --year 2025
clawshire --output json annual-analysis company 920445 --year 2025 --exchange bj
```

## 用本地 PDF 提交分析

```bash
clawshire annual-analysis pdf-file <本地路径>
```

示例：

```bash
clawshire --output json annual-analysis pdf-file ./report.pdf
clawshire --output json annual-analysis pdf-file ./report.pdf --wait
```

## 用 PDF 链接提交分析

```bash
clawshire annual-analysis pdf-url <url>
```

示例：

```bash
clawshire --output json annual-analysis pdf-url https://example.com/report.pdf
```

注意：

- `pdf-url` 依赖上游 PDF 可访问
- 某些 PDF 可能返回服务端错误
- 若 `pdf-url` 失败，优先建议用户改走 `company` 模式

## 查询分析任务

```bash
clawshire annual-analysis get <task_or_job_id>
```

示例：

```bash
clawshire --output json annual-analysis get 74
clawshire --output json annual-analysis get 27
clawshire annual-analysis get 74 --save-report-to report.html
```
