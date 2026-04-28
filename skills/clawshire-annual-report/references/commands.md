# Commands

## 推荐命令

| 命令 | 用途 |
|------|------|
| `clawshire annual-report latest --year <YYYY> --keyword <kw>` | 查询年报列表 |
| `clawshire annual-report latest --year <YYYY> --exchange <ex> --keyword <kw>` | 按交易所过滤年报 |
| `clawshire annual-report data <met_uuid>` | 查询单份年报的结构化数据 |
| `clawshire annual-report ... --format json` | 返回结构化结果供脚本或 Agent 处理 |

## 定位年报

```bash
clawshire annual-report latest --year <YYYY> --keyword <关键词>
```

示例：

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行 --page-size 3
clawshire annual-report latest --year 2025 --keyword 000001 --format json
clawshire annual-report latest --year 2025 --exchange bj --keyword 920445 --format json
```

结果中优先关注：

- `met_uuid`
- `company_code`
- `company_name`
- `category_name`
- `publish_time`
- `pdf_url`

## 查询结构化年报数据

```bash
clawshire annual-report data <met_uuid>
```

示例：

```bash
clawshire annual-report data 10fd860b-c12e-54b3-a5b3-38c2ecdf5b2b --format json
```
