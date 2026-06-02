# Commands

## 推荐命令

| 命令 | 用途 |
|------|------|
| `clawshire wiki company <sec_code>` | 查公司 Wiki 画像（公告时间线、事实、标签） |
| `clawshire wiki entry <ann_id>` | 查单条公告详情（全文、结构化字段、事实） |
| `clawshire wiki search --code <code>` | 搜索公告 Wiki 条目 |
| `clawshire wiki resolve <q>` | 公司名/别名解析为证券代码 |
| `clawshire wiki tag <tag_name>` | 按 Tag 主题查询 |

## 示例

```bash
# 解析公司名拿 sec_code
clawshire wiki resolve 平安银行 --format json

# 查公司画像
clawshire wiki company 000001 --format json

# 查公告详情
clawshire wiki entry ann_20260601_000001 --format json

# 搜索某类公告
clawshire wiki search --code 000001 --ann-type 业绩预告 --size 10 --format json

# 按标签查询
clawshire wiki tag 股票回购 --format json
```
