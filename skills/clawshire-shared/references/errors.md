# Errors

## 配置错误

若出现：

```text
配置错误: 该命令需要 API Key
```

处理方式：

```bash
clawshire auth set-key <your_api_key>
clawshire auth status
clawshire user info
```

## 认证错误

若出现：

```text
认证失败: Authorization 格式错误，应为 Bearer <api_key>
```

处理方式：

```bash
clawshire auth show
clawshire auth status
clawshire auth clear-key
clawshire auth set-key <your_api_key>
clawshire user info
```

## 服务端错误

若出现：

```text
接口错误: ...
```

规则：

1. 不要假设是 CLI 参数问题
2. 先区分是认证问题、参数问题还是服务端异常
3. 对长流程任务，优先建议用户改走更稳定的入口，例如 `annual-analysis company`
