# Local E2E

这份文档用于在本地模拟一个真实用户，从安装 `clawshire-cli` 到安装 Skills，再到实际执行查询命令的完整流程。

目标不是替代单元测试，而是验证以下问题：

1. CLI 是否能被正常安装和发现
2. 认证链路是否可用
3. 真实核心命令是否能跑通
4. `skills/` 目录是否适合按整个仓库作为 bundle 分发
5. 本地源码态和未来独立开源后的仓库结构是否一致

## 1. 准备

进入 CLI 项目目录：

```bash
cd clawshire-cli
```

如使用项目内虚拟环境，可先确认：

```bash
.venv/bin/python --version
.venv/bin/pytest --version
```

若要跑真实线上链路，需提前准备：

```bash
export CLAWSHIRE_API_KEY="<your_api_key>"
```

## 2. 先跑测试

先确认当前测试集通过：

```bash
.venv/bin/pytest -q
.venv/bin/python scripts/check_skill_drift.py
```

这一步现在同时覆盖：

1. CLI 命令解析与版本检查
2. `skills/` 目录结构校验
3. 每个 `SKILL.md` 的 frontmatter 校验
4. `SKILL.md` 与 `references/` 内相对链接可达性校验
5. skills 文档中真实 `clawshire` 示例命令的可解析性校验
6. 如果存在派生 skill bundle，其 `metadata.sourceSkill` 来源声明校验

## 3. 本地安装 CLI

模拟用户从源码安装：

```bash
uv tool install .
```

安装后检查命令可见性：

```bash
clawshire --help
clawshire version
clawshire auth --help
```

如果你不想污染全局环境，也可以只验证本地虚拟环境入口：

```bash
.venv/bin/clawshire --help
.venv/bin/clawshire version
```

## 4. 认证链路检查

如果使用环境变量：

```bash
clawshire auth status
clawshire auth check
clawshire user info
```

如果要模拟首次配置：

```bash
clawshire auth set-key <your_api_key>
clawshire auth show
clawshire auth status
clawshire auth check
clawshire user info
```

退出登录验证：

```bash
clawshire auth logout
clawshire auth status
```

## 5. 真实业务链路

建议至少验证以下 3 条主链路。

### 公告查询

```bash
clawshire notice stock 603402 --start-date 2026-04-01 --end-date 2026-04-20 --page-size 3
clawshire notice link --met-link http://static.cninfo.com.cn/finalpage/2026-04-20/1225124234.PDF --format json
```

### 年报定位

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行 --page-size 3
```

### 年报分析

```bash
clawshire annual-analysis company 000001 --year 2025 --format json
```

如果返回 `task_id` 或 `next_command`，继续查状态：

```bash
clawshire annual-analysis get <task_id> --format json
```

## 6. Skills bundle 验证

当前推荐安装方式是按整个仓库安装 skills bundle，而不是安装单个 skill 子目录。

推荐检查项：

```text
skills/
  clawshire-shared/
  clawshire-data-query/
  clawshire-annual-report/
  clawshire-annual-analysis/
```

并确认每个 skill 都包含：

```text
SKILL.md
references/
```

可以直接检查：

```bash
find skills -maxdepth 3 -type f | sort
```

如果仓库已经公开到 GitHub，再补一轮真实安装验证：

```bash
npx skills add <owner>/clawshire-cli -y -g
```

当前在本地源码阶段，最关键的是先保证仓库内的 `skills/` 结构稳定，等独立仓库上线后再补 GitHub 安装冒烟。

## 7. 已验证的真实样例

以下样例已于 `2026-04-22` 用真实 API Key 跑通，可直接作为对外文档和本地验收参考。

### 认证状态

```bash
clawshire auth status --format json
```

关键结果：

```json
{
  "api_key_source": "env",
  "authenticated": true,
  "message": "认证可用"
}
```

### 用户信息

```bash
clawshire user info --format json
```

关键结果：

```json
{
  "balance_yuan": 95.59,
  "month_cost_yuan": 3.79
}
```

### 公告查询

```bash
clawshire notice stock 603402 --start-date 2026-04-01 --end-date 2026-04-20 --page-size 3 --format json
```

关键结果：

```json
{
  "sec_code": "603402",
  "total": 25,
  "page_size": 3
}
```

样例命中公告包括：

1. `陕西旅游：关于陕西旅游文化产业股份有限公司2025年非经营性资金占用及其他关联资金往来情况汇总表的专项审计报告`
2. `陕西旅游：关于审计委员会对会计师事务所2025年度履行监督职责情况的报告`
3. `陕西旅游：薪酬管理制度`

### 年报定位

```bash
clawshire annual-report latest --year 2025 --keyword 平安银行 --page-size 3 --format json
```

关键结果：

```json
{
  "total": 1,
  "company_count": 1,
  "items": [
    {
      "company_name": "平安银行",
      "publish_time": "2026-03-21T00:00:00"
    }
  ]
}
```

### 年报分析提交

```bash
clawshire annual-analysis company 000001 --year 2025 --format json
```

关键结果：

```json
{
  "task_id": 74,
  "message": "分析任务已提交，请稍后查看结果",
  "next_command": "clawshire annual-analysis get 74"
}
```

继续查询状态：

```bash
clawshire annual-analysis get 74 --format json
```

当次返回：

```json
{
  "task_id": 74,
  "company_name": "平安银行",
  "status": "processing"
}
```

注意：`annual-analysis company` 会消耗一次真实分析额度，本地冒烟时建议按需执行。

如果对同一公司和年份重复执行，服务端可能返回“该年报已有分析任务在进行中，请稍后再试”。这类结果说明提交链路已到达服务端，重复冒烟时可视为通过。

## 8. 推荐验收清单

```text
[ ] .venv/bin/pytest -q 通过
[ ] clawshire --help 可运行
[ ] clawshire version 返回版本号
[ ] clawshire auth status 可返回认证状态
[ ] clawshire auth check 返回正确退出码
[ ] clawshire user info 可用
[ ] notice 主链路可用
[ ] annual-report 主链路可用
[ ] annual-analysis 主链路可用
[ ] skills/ 目录结构完整
```

## 9. 一键检查脚本

仓库已提供：

```bash
./scripts/e2e_local_check.sh
```

默认执行：

1. 单元测试
2. CLI 基础命令检查
3. skills 目录结构检查

其中第 1 步的 `pytest` 已包含 skills 专项测试。

如果环境中存在 `CLAWSHIRE_API_KEY`，还会继续执行线上真实命令检查，包括：

1. `auth status`
2. `auth check`
3. `user info`
4. `notice stock`
5. `annual-report latest`
6. `annual-analysis company`

其中 `annual-analysis company` 在重复执行时，如果命中同一份年报已有进行中的任务，脚本会将该结果视为可接受的冒烟通过。
