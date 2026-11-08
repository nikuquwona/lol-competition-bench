# Claude Code × DeepSeek V4 Pro

五局十个预测时点，使用 Claude Code 2.1.270 与 DeepSeek 官方 `deepseek-v4-pro`。每次运行都在独立 macOS Seatbelt 沙箱，通过宿主网关请求 `api.deepseek.com/anthropic/v1/messages`。费用记入提供 `DEEPSEEK_API_KEY` 的用户账户。此报告未读取账单。

[完整预测和逐题工具轨迹](report.md) · [机器可读结果及分片来源](report.json) · [预先固定的五场](../../suites/featured-five.json)

每个时点都有一次正式尝试。报告保留运行失败、超时、推理错误和工具重试，按原始题面与预算结算。以下 token 数字取自原生 CLI 的终态 usage。

| 已评分 / 计划 | 平均 reward | 胜负 Brier | 15 分钟领先 Brier |
| ---: | ---: | ---: | ---: |
| 10/10 | 0.68065 | 0.33700 | 0.30170 |

| 输入 token | 缓存读取 token | 输出 token |
| ---: | ---: | ---: |
| 144,025 | 1,315,072 | 95,281 |

## 复现

```sh
./bench e2e --release worlds-lpl-2026 --suite featured-five --backend macos \
  --mode live --harness claude --model deepseek-v4-pro
```

本例以五个双时点分片运行，最多同时处理两场。公开副本替换了会话标识、签名与临时工作路径，保留工具指令、回显、模型消息、预测及赛后评分。`sources/*-redactions.json` 提供原始文件和公开副本的 SHA-256。
