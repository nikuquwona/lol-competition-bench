# KC–T1 第二局 · 原生 Codex CLI × DeepSeek

Codex CLI 0.167.0，DeepSeek 官方 Responses API，指定 deepseek-v4-pro。两个时点使用独立的临时 macOS Seatbelt 沙箱，外部网关持有本机凭证。任务目录里只有当题冻结快照；题目里 /app/ 替换为当前目录。两组共用相同的 40 请求硬上限和 600 秒超时。记录中的临时路径和本机用户名已作脱敏。CLI 报告没有此模型的本地元数据并使用默认元数据；模型请求仍发往 DeepSeek。

| 轮次 | 时点 | KC 胜率 | KC 15 分钟领先概率 | reward |
|---|---|---:|---:|---:|
| 原始任务说明 | BP 前 | 未交卷，达到请求上限 | — | — |
| 原始任务说明 | BP 后 | 未交卷，达到时间上限 | — | — |
| 相同预算提示的配对重试 | BP 前 | 30% | 55% | 0.80375 |
| 相同预算提示的配对重试 | BP 后 | 32% | 44% | 0.85200 |

第一轮的两份轨迹均保存在 initial-attempt。重试另起两个会话，在相同的任务说明中补充了尽早写出预测和最多六次 shell 调用的提示，并把 zsh 的临时文件前缀设在沙箱内。这是提示中的软预算；BP 后实际执行了七次 shell 工具。表中的概率均为 CLI 最终写入文件的值，执行中的临时估计未用于打分。两局任务对应同一真实小局，实际 T1 获胜，KC 在 15:00 落后 4,026 金。历史名局可能存在预训练记忆。

- [BP 前工具轨迹](lobby/transcript.md)
- [BP 后工具轨迹](draft-lock/transcript.md)
- [BP 前评分](lobby/score.json)
- [BP 后评分](draft-lock/score.json)

使用 macOS 系统 sandbox-exec 运行 cli.macos_pair 的 --budget-prompt 模式可以复现本轮配置。GitHub 的 Regrade KC–T1 DeepSeek predictions 工作流选 harness=codex 会向 Harbor 提交本次保存的两个预测，并校验独立 verifier 的 reward。
