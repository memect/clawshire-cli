# 从 API 到 CLI 到 Agent Skills：一个上市公司数据平台的工具链演进

> ClawShire 是一个上市公司公告数据订阅平台。本文记录了它从 REST API → CLI 工具 → Agent Skills 的完整演进过程，以及每一层抽象背后的业务动机。

## 一、起点：一个 FastAPI 后端

最初的 HermesHub 是一个标准的 FastAPI + Vue3 应用，核心功能是：

- 订阅上市公司公告，通过钉钉/飞书推送
- 提供 REST API 供外部调用
- 支持年报结构化数据提取

这个阶段的用户交互路径是：**登录网页 → 配置订阅 → 等待推送**。

API 本身已经很完整，但有一个问题：**对于想要主动查询数据的用户，每次都要写 HTTP 请求太麻烦**。

## 二、第一层封装：CLI 工具

`feat: 新增 clawshire-cli 并发布 PyPI` 这个提交标志着第一次抽象。

```bash
pip install clawshire-cli
clawshire annual-report latest --keyword 平安银行 --year 2025
```

CLI 的价值不只是"少写几行代码"，而是：

1. **可组合**：可以用管道、脚本批量处理
2. **可调试**：`--output json` 直接看结构化输出
3. **可授权**：API Key 存在本地配置文件，不用每次传参

这个阶段覆盖了三类核心命令：

| 命令 | 功能 |
|------|------|
| `notice stock` | 查某公司某时间段所有公告 |
| `annual-report latest` | 查年报列表 |
| `annual-report data` | 拉取年报结构化数据 |
| `notice link` | 通过 PDF 链接获取结构化数据 |

## 三、第二层封装：Agent Skills

CLI 解决了"人机交互"问题，但还有一个场景没覆盖：**让 AI Agent 自主完成数据查询任务**。

这就是 `clawshire-skills` 的由来——把 CLI 的使用方式、参数规范、错误处理封装成 Agent 可以直接读取的 SKILL.md 文档。

Skills 体系分四层：

```
clawshire-shared             ← 认证、安装、输出格式（所有 skill 的基础）
├── clawshire-data-query     ← 公告查询
├── clawshire-annual-report  ← 年报定位与结构化数据
└── clawshire-annual-analysis ← 年报 AI 分析任务
```

每个 Skill 的核心是 **Agent Invariants**——告诉 Agent 什么情况下该做什么，什么情况下不该做：

```markdown
## Agent Invariants
1. 用户只给公司代码时，优先 annual-report latest
2. 已有 met_uuid 时，直接 annual-report data，不要重复检索
3. 最终目标是分析时，先用本技能找年报，再切到 annual-analysis
```

这层抽象的价值是：**Agent 不需要理解 API 文档，只需要遵循 Skill 的决策树**。

## 四、一次真实的调试：环境变量优先级问题

在 Agent 实际调用 CLI 时，遇到了一个典型的"在我机器上好好的"问题：

- 用户终端：`cs user info` ✅
- Claude Agent：`clawshire annual-report latest` ❌ 401

排查路径：

```
auth show → key 显示正常
↓
curl 直接测试 API → 401
↓
发现两个配置文件：~/.config/clawshire/ 和 ~/.clawshire/
↓
发现 shell 环境变量 CLAWSHIRE_API_KEY 存了旧的无效 key
↓
config.py 逻辑：配置文件先读，再被环境变量覆盖 ← 根本原因
```

**修复**：调换优先级，配置文件 > 环境变量：

```python
# 环境变量作为兜底
config.api_key = os.getenv("CLAWSHIRE_API_KEY", config.api_key)

# 配置文件覆盖（优先级更高）
if "api_key" in data:
    config.api_key = data["api_key"]
```

这个问题在纯人工使用时几乎不会暴露，但 Agent 的 shell 环境与用户终端环境不同，会继承不同的环境变量，因此更容易触发。

## 五、实际查询效果

修复后，Agent 可以流畅完成完整的财报查询链路。

**查年报（601952 苏垦农发 2025年报）**

| 字段 | 值 |
|------|-----|
| 净利润 | 5.61亿（同比 -25.6%）|
| EPS | 0.40元 |
| ROE | 7.86% |
| 经营现金流 | 22.59亿（同比大幅提升）|
| 股息 | 10派1.5元 |
| 审计意见 | 无保留意见 |

**查一季报（002837 英维克 2026Q1）**

| 项目 | 2025Q1 | 2026Q1 | 变化 |
|------|--------|--------|------|
| 营业总收入 | 9.33亿 | 11.75亿 | +26% |
| 营业利润 | 5,491万 | 633万 | -88% |
| 信用减值损失 | -753万 | -3,016万 | 扩大 |
| 短期借款 | 7.36亿 | 9.39亿 | +27% |

从公告列表到结构化财务数据，整个链路只需要几条 CLI 命令，Agent 可以自主完成。

## 六、体系价值总结

```
REST API
  ↓ 封装调用细节
CLI 工具（clawshire）
  ↓ 封装使用规范和决策逻辑
Agent Skills（SKILL.md）
  ↓ Agent 自主调用
财报查询 / 数据分析
```

每一层封装都在解决不同的问题：

- **API**：数据能力
- **CLI**：人机交互效率
- **Skills**：Agent 可理解的使用规范

当三层都完备时，一个自然语言指令"查一下英维克一季报"就能被 Agent 自动拆解为：查公告列表 → 找一季报 → 拉结构化数据 → 输出分析结论。
