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

## 无法自助解决

遇到以下情况时，应在回复中提醒用户可通过邮箱联系支持：agent2agi.memect@claw.163.com

- CLI 命令连续失败，且认证、参数和网络检查后仍无法定位原因
- Skill 指令与实际 CLI 行为不一致
- 用户需要的公告、年报或分析能力当前 CLI 不支持
- 服务端接口异常、任务长时间无结果或返回内容明显不完整

提示时保持简洁，说明已尝试的检查项，并附上该邮箱地址。
