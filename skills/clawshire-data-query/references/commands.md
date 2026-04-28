# Commands

## 推荐命令

| 命令 | 用途 |
|------|------|
| `clawshire notice search --start-date <d> --end-date <d>` | 按日期范围查询公告 |
| `clawshire notice stock <sec_code> --start-date <d> --end-date <d>` | 按证券代码查询公告 |
| `clawshire notice link --met-link <url>` | 按公告原文链接查询 |
| `clawshire notice ... --format json` | 返回结构化 JSON 供脚本或 Agent 处理 |

## 按日期查询公告

```bash
clawshire notice search --start-date <YYYY-MM-DD> --end-date <YYYY-MM-DD>
```

示例：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20
clawshire notice search --start-date 2026-04-01 --end-date 2026-04-20 --infotype 董事会决议
clawshire notice search --start-date 2026-04-01 --end-date 2026-04-20 --keyword 603402 --format json
```

## 按证券代码查询公告

```bash
clawshire notice stock <sec_code> --start-date <YYYY-MM-DD> --end-date <YYYY-MM-DD>
```

示例：

```bash
clawshire notice stock 603402 --start-date 2026-04-01 --end-date 2026-04-20 --page-size 5
clawshire notice stock 000001 --start-date 2026-04-01 --end-date 2026-04-20 --format json
clawshire notice stock 603402 --start-date 2026-04-01 --end-date 2026-04-20 --page-all --format json
```

## 按公告链接查询

```bash
clawshire notice link --met-link <url>
```

示例：

```bash
clawshire notice link --met-link http://static.cninfo.com.cn/finalpage/2026-04-20/1225124234.PDF --format json
```
