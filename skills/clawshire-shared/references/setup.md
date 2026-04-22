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
- `--output json`：给脚本或 Agent 消费
- `--output markdown`：适合粘贴到文档或对话中
- `--output csv`：适合导出表格

示例：

```bash
clawshire --output json user info
```
