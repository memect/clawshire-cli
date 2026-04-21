# ClawShire CLI

独立可安装的 ClawShire 命令行客户端。

## 安装

```bash
pip install clawshire-cli
```

或使用 uv（推荐）：

```bash
uv tool install clawshire-cli
```

本地开发从源码安装：

```bash
uv tool install ./clawshire-cli
```

安装后可使用两个命令入口：

```bash
clawshire --help
cs --help
```

如果你只想快速确认安装成功，先跑：

```bash
clawshire --help
clawshire auth --help
clawshire user info --api-key <your_api_key>
```

## 3 分钟上手

把下面几条命令直接复制执行即可：

```bash
pip install clawshire-cli
clawshire auth set-key <your_api_key>
clawshire user info
clawshire annual-analysis pdf-url https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
```

如果你要查公告或年报，再继续：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20
clawshire annual-report latest --year 2025 --keyword 平安银行
```

## 先配置 API Key

建议先把 API Key 保存到本地，这样后续不用每次手动加 `--api-key`。

```bash
clawshire auth set-key <your_api_key>
clawshire auth show
clawshire user info
```

如果想临时覆盖本地配置，也可以直接传：

```bash
clawshire --api-key <your_api_key> user info
```

清除本地保存的 Key：

```bash
clawshire auth clear-key
```

## 命令

主命令分组：

1. `notice`
2. `annual-report`
3. `annual-analysis`

高频简写：

1. `gg` -> `notice`
2. `ar` -> `annual-report`
3. `aa` -> `annual-analysis`

## 全部命令能力

| 能力 | 命令 | 是否需要 API Key | 说明 |
|------|------|------------------|------|
| 保存 Key | `clawshire auth set-key <key>` | 否 | 保存本地 API Key |
| 查看认证配置 | `clawshire auth show` | 否 | 查看当前 base_url、key 掩码、输出格式、超时 |
| 清除 Key | `clawshire auth clear-key` | 否 | 清除本地保存的 API Key |
| 检查当前 Key | `clawshire auth whoami` | 是 | 校验当前 API Key 是否有效 |
| 用户信息 | `clawshire user info` | 是 | 查询余额、免费次数、配额等用户信息 |
| 公告按日期查询 | `clawshire notice search --start-date <d> --end-date <d> --keyword 603402` | 否/建议有 | 按日期范围查询公告，示例默认限定证券代码避免结果过大 |
| 公告按证券代码查询 | `clawshire notice stock <sec_code> --start-date <d> --end-date <d>` | 否/建议有 | 查询某证券代码公告 |
| 公告按链接查询 | `clawshire notice link --met-link <pdf_link>` | 否/建议有 | 按公告 PDF 链接查询 |
| 年报列表 | `clawshire annual-report latest --year <YYYY> --keyword <kw>` | 是 | 查询指定年份年报列表 |
| 年报结构化数据 | `clawshire annual-report data <met_uuid>` | 是 | 查询指定年报的结构化数据 |
| 年报分析: 本地文件 | `clawshire annual-analysis pdf-file <path>` | 是 | 上传本地 PDF 分析 |
| 年报分析: PDF 链接 | `clawshire annual-analysis pdf-url <url>` | 是 | 下载 PDF 链接后分析 |
| 年报分析: 公司 | `clawshire annual-analysis company <代码或简称> --year <YYYY>` | 是 | 先查询指定年份年报，再自动发起分析 |
| 查询分析任务 | `clawshire annual-analysis get <task_id_or_job_id>` | 是 | 查询分析任务状态或结果 |

简写命令：

| 简写 | 全称 | 示例 |
|------|------|------|
| `gg` | `notice` | `cs gg search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402` |
| `ar` | `annual-report` | `cs ar latest --year 2025 --keyword 平安银行` |
| `aa` | `annual-analysis` | `cs aa company 000001 --year 2025` |

按命令分组查看帮助：

```bash
clawshire auth --help
clawshire user --help
clawshire notice --help
clawshire annual-report --help
clawshire annual-analysis --help
```

## 示例

```bash
clawshire user info
clawshire notice search --start-date 2026-04-01 --end-date 2026-04-20 --keyword 603402
clawshire annual-report latest --year 2025 --keyword 平安银行
clawshire annual-analysis pdf-file ./report.pdf
clawshire annual-analysis pdf-url https://example.com/report.pdf
clawshire annual-analysis company 000001 --year 2025
```

年报分析测试 PDF 示例：

```text
https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
```

推荐直接试：

```bash
clawshire annual-analysis pdf-url https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
```

## 配置

支持环境变量：

1. `CLAWSHIRE_API_KEY`
2. `CLAWSHIRE_BASE_URL`
3. `CLAWSHIRE_OUTPUT`
4. `CLAWSHIRE_TIMEOUT`

如果你更习惯环境变量，可直接这样配置：

```bash
export CLAWSHIRE_API_KEY=<your_api_key>
clawshire user info
```

## 最常用命令

查询用户信息：

```bash
clawshire user info
```

查询公告：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402
clawshire notice stock 000001 --start-date 2026-04-01 --end-date 2026-04-20
clawshire notice link --met-link <pdf_link>
```

查询年报：

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行
clawshire annual-report data <met_uuid>
```

发起年报分析：

```bash
clawshire annual-analysis pdf-file ./report.pdf
clawshire annual-analysis pdf-url https://static.cninfo.com.cn/finalpage/2026-04-20/1225116956.PDF
clawshire annual-analysis company 000001 --year 2025
```

查询分析任务：

```bash
clawshire annual-analysis get <task_id_or_job_id>
```

## 必要提示

1. 全局参数要放在子命令前面，例如：`clawshire --output json user info`
2. `notice` 查询通常不需要 API Key，但如果本地配置了错误的 Key，可能会带上错误认证头
3. `annual-report`、`annual-analysis`、`user info` 都需要有效 API Key
4. CLI 不单独实现计费，仍然走服务端原有配额和计费逻辑

## 常见报错与处理

### 1. `认证失败: Authorization 格式错误，应为 Bearer <api_key>`

原因：

1. 本地保存了错误的 API Key
2. 环境变量里有错误的 `CLAWSHIRE_API_KEY`
3. 你传入的不是完整 API Key

处理：

```bash
clawshire auth show
clawshire auth clear-key
clawshire auth set-key <your_api_key>
clawshire user info
```

如果你使用环境变量，也检查：

```bash
echo $CLAWSHIRE_API_KEY
```

### 2. `配置错误: 该命令需要 API Key`

原因：

1. 你在调用需要认证的命令，但还没有配置 Key

处理：

```bash
clawshire auth set-key <your_api_key>
clawshire user info
```

或者临时传参：

```bash
clawshire --api-key <your_api_key> user info
```

### 3. `unrecognized arguments: --output json`

原因：

1. 把全局参数写在了子命令后面

错误示例：

```bash
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402 --output json
```

正确写法：

```bash
clawshire --output json notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402
```

### 4. `未找到与 XXX 匹配的年报`

原因：

1. 公司代码或简称不匹配
2. 指定年份没有收录对应年报
3. 交易所筛选过窄

处理：

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行
clawshire annual-report latest --year 2025 --keyword 000001
clawshire annual-analysis company 000001 --year 2025
```

如果仍然找不到，先去掉 `--exchange` 再试。

### 5. `查询分析任务` 没返回结果

原因：

1. `annual-analysis get` 传错了 ID
2. `pdf-file/pdf-url` 用的是 `job_id`
3. `company` 用的是平台异步分析 `task_id`

处理：

1. `pdf-file` / `pdf-url` 后续查询传 `job_id`
2. `company` 后续查询优先传 `task_id`

示例：

```bash
clawshire annual-analysis get 123
clawshire annual-analysis get job_xxx
```

## 发布流程

### 版本更新

1. 修改 [pyproject.toml](/Users/memect/work/code/sz_extract/hermeshub/clawshire-cli/pyproject.toml) 中的 `version`
2. 如有命令变化，同步更新本 README 与根目录 [README.md](/Users/memect/work/code/sz_extract/hermeshub/README.md)

### 本地构建

```bash
cd clawshire-cli
uv build
```

构建产物位于：

```text
clawshire-cli/dist/
```

### 本地安装验证

```bash
cd clawshire-cli
uv tool install .
clawshire --help
cs --help
clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402
```

如果本机已安装 `pipx`，再补一轮：

```bash
cd clawshire-cli
pipx install .
clawshire --help
```

### 发布测试版

建议先发测试版，再发正式版，例如：

1. `0.1.0a1`
2. `0.1.0b1`
3. `0.1.0rc1`

发布命令示例：

```bash
cd clawshire-cli
uv build
uv publish
```

如果要发到 TestPyPI：

```bash
cd clawshire-cli
uv build
uv publish --publish-url https://test.pypi.org/legacy/
```

安装验证：

```bash
pip install clawshire-cli
clawshire --help
cs --help
```
