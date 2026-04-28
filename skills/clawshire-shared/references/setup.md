# Setup

## 安装检查

先确认本机已安装 CLI：

```bash
clawshire --help
```

若命令不存在，引导用户安装：

```bash
uv tool install clawshire-cli
```

或：

```bash
pipx install clawshire-cli
```

## 认证

优先检查本地配置：

```bash
clawshire auth show
clawshire auth status
```

如未配置，引导用户设置：

```bash
clawshire auth set-key <your_api_key>
```

也支持环境变量：

```bash
export CLAWSHIRE_API_KEY="<your_api_key>"
```

## 首次可用性验证

在执行收费或长流程能力前，优先先做一次轻量验证：

```bash
clawshire user info
clawshire auth check
```

若用户只是查询公告，`notice` 相关接口通常可先直接使用。

## 输出格式

- 默认输出：给人看，适合终端阅读
- `--format json` / `--json`：给脚本或 Agent 消费
- `--format markdown`：适合粘贴到文档或对话中
- `--format csv`：适合导出表格

示例：

```bash
clawshire user info --format json
```

## Agent Attribution

Agent 或 Skill 调用 CLI 前，尽量设置来源和意图，便于后端观测：

```bash
export CLAWSHIRE_CLIENT=skill
export CLAWSHIRE_AGENT_NAME="<agent-name>"
export CLAWSHIRE_RATIONALE="<why-this-tool-is-called>"
export CLAWSHIRE_TRACE_ID="<trace-id>"
```

若工具调用被阻塞，提交结构化反馈：

```bash
clawshire agent feedback --intent "用户想完成的任务" --blocked-by "阻塞点" --expected-capability "期望能力" --related-tool notice.search --format json
```
