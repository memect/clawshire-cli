# Task Lifecycle

## 提交结果

执行提交命令后，通常会返回：

- `task_id`
- `message`
- `selected_report`
- `next_command`

如果返回了 `next_command`，优先直接继续执行它。

## 任务查询

若任务已完成并存在报告地址，可使用 `--save-report-to` 下载 HTML 报告。

## 输出规则

若输出给人看，至少总结：

- 当前分析对象
- 任务 ID
- 当前状态
- 下一步命令
- 若完成，则给出报告路径或报告 URL

若输出给脚本或 Agent，优先使用：

```bash
clawshire ... --format json
```
