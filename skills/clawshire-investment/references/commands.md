# Commands

## 推荐命令

| 命令 | 用途 |
|------|------|
| `clawshire investment industries` | 列出所有申万一级行业名称（免费） |
| `clawshire investment company <sec_code>` | 查公司研判变化记录 |
| `clawshire investment summary <sec_code>` | 查公司综合研判摘要 |
| `clawshire investment industry <行业名>` | 查行业景气研判 |

## 示例

```bash
# 先查行业列表确认标准名
clawshire investment industries --format json

# 查公司研判变化（最近 10 条）
clawshire investment company 000001 --size 10 --format json

# 查公司综合研判
clawshire investment summary 000001 --format json

# 查行业景气
clawshire investment industry 银行 --format json
clawshire investment industry 医药生物 --format json
```

## 注意

- `industry` 参数必须是申万一级行业标准名，先用 `industries` 命令确认。
- 研判结果基于已入库公告，最新公告可能有延迟。
