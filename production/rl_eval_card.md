---
pretty_name: LoL Competition Bench
language:
- en
configs:
- config_name: training
  data_files:
  - split: train
    path: rl/train.jsonl.gz
- config_name: training-tools
  data_files:
  - split: train
    path: rl/train-workspace.jsonl.gz
- config_name: evaluation
  data_files:
  - split: train
    path: eval/train.jsonl.gz
  - split: validation
    path: eval/validation.jsonl.gz
  - split: test
    path: eval/test.jsonl.gz
---

# LoL competition forecasts for training and evaluation

Each example covers one game at the pre-draft lobby or at draft lock. Stable IDs include the benchmark namespace, Harbor release and task ID. See `manifest.json` for exact counts, file checksums, release archive SHA-256 and split boundaries. Storing snapshots by SHA-256 in an indexed ZIP allows random access to the exact frozen input for one rollout.

| Path | Consumer | Contents |
| --- | --- | --- |
| `rl/train.jsonl.gz` | RL trainer | Chat-template `prompt` with the full frozen JSON inline; `data_source`, `ability`, `extra_info`, and a separate `reward_model.ground_truth`. The policy receives only the message list. |
| `rl/train.parquet` | verl / Arrow loader | Identical training rows when exported with `--parquet`. |
| `rl/train-workspace.jsonl.gz` | Agentic RL runner | The same training IDs and reward labels with the original Harbor prompt and tool workspace references. |
| `eval/{train,validation,test}.jsonl.gz` | Evaluation runner | Label-free rows. `prompt` is the original Harbor instruction. `extra_info` identifies the snapshot, game, phase and Harbor task. |
| `snapshots.zip` | Trusted runner | One member named `<snapshot_sha256>.json` per distinct frozen view. Mount only the current row's materialized workspace for the model. |
| `verifier/{train,validation,test}.jsonl.gz` | Organizer / reward callback | Outcome labels joined by full example ID. Keep these files outside agent workspaces. |

## Split and temporal policy

Series starting before 2026-10-28 00:00 UTC enter training. Series from that time until 2026-11-03 00:00 UTC enter validation. Later series enter test. These cutoffs follow the historical tournament calendar and remain fixed on regeneration. Both phases and every game in one series share a split. Rows in each file follow series start, series identifier, game number, and then lobby before draft lock. Each view may include already-public games from its own split when the benchmark history rules allow it. Training never consumes validation or test rows. When mixing releases, deduplicate by series, game and phase before splitting.

The scores measure retrospective replay. A model may remember these public games from training. For evidence about a genuinely unseen outcome, use a live observation with a timely sealed submission. Different harnesses or input protocols warrant separate scores.

## Load, mix and score

Run the following examples from the project checkout. The HF configs work on the local folder without uploading anything. For another compatible training dataset, first normalize its `prompt` to chat messages and align the selected Arrow schema. Preserve each row's `data_source` when dispatching rewards.

```python
from datasets import Dataset, concatenate_datasets, load_dataset
from pathlib import Path
from evaluation.dataset import compute_score

bundle = Path("datasets/rl-eval-v1")
train = load_dataset(str(bundle.resolve()), "training", split="train")
test = load_dataset(str(bundle.resolve()), "evaluation", split="test")
# A one-row example from a different source illustrates a heterogeneous training mix.
other = Dataset.from_list([{
    "id": "example/arithmetic/1", "data_source": "example/arithmetic", "ability": "arithmetic",
    "prompt": [{"role": "user", "content": "What is 2 + 2?"}],
    "reward_model": {"style": "rule", "ground_truth": "4"},
    "extra_info": {"id": "example/arithmetic/1", "split": "train"},
}])
mixed = concatenate_datasets([train, other])
assert mixed[-1]["data_source"] == "example/arithmetic"
row = mixed[0]
policy_messages = row["prompt"]                     # tokenizer.apply_chat_template(...)
reward = compute_score(row["data_source"], '{"p_blue_win":0.5,"p_blue_ahead_15":0.5}',
                       row["reward_model"]["ground_truth"], row["extra_info"])
assert reward == 0.75
```

For verl, point `data.train_files` at `rl/train.parquet` and register the checkout's `evaluation/dataset.py` as the custom reward file with function name `compute_score`. Keep the project root on the trainer's Python path. The callback expects the final JSON answer. Each target receives weight 1/2 and reward is 1 minus the mean squared probability error. Invalid answer JSON earns zero. A missing or mismatched target ID raises a dataset error. Set prompt length against the tokenizer you train with: each inline row includes the complete visible history. Silent truncation or filtering changes evidence and coverage. [verl data format](https://verl.readthedocs.io/en/latest/preparation/prepare_data.html) · [Custom reward function](https://verl.readthedocs.io/en/latest/preparation/reward_function.html)

## Evaluate or train with a tool workspace

The stdlib path works offline. Run the model in a sandbox with only the materialized directory mounted at `/app`; shell commands can inspect its `snapshot.json`. The scoring process receives the resulting `prediction.json`. In an agentic RL runner, materialize a row from `rl/train-workspace.jsonl.gz`, expose its `prompt` to the policy and keep `reward_model` in the trainer process.

```python
import json
import tempfile
from pathlib import Path
from evaluation.dataset import compute_score, inline_messages, iter_rows, materialize, snapshot_bytes

bundle = Path("datasets/rl-eval-v1")
row = next(iter_rows(bundle / "eval/test.jsonl.gz"))
with tempfile.TemporaryDirectory() as tmp:
    workspace = materialize(bundle, row, Path(tmp) / "app")
    assert sorted(p.name for p in workspace.iterdir()) == ["instruction.md", "snapshot.json"]
    messages = row["prompt"]                       # Give these instructions to the CLI.
# A tool-free evaluation can instead use the training protocol.
inline = inline_messages(snapshot_bytes(bundle, row))
# Organizer only. The 50/50 prediction here demonstrates the scoring contract.
key = next(r for r in iter_rows(bundle / "verifier/test.jsonl.gz") if r["id"] == row["id"])
value = compute_score(row["data_source"], '{"p_blue_win":0.5,"p_blue_ahead_15":0.5}',
                      json.dumps(key), row["extra_info"])
assert value == 0.75
```

The tool protocol uses the original Harbor instruction and reads a submitted file. The inline protocol delivers the frozen view in the prompt and parses a JSON reply. They score the same observable outcomes, while measuring different evidence-access and tool-use behavior. Keep the ZIP, other rows, organizer files, other sessions and web access outside the model's workspace.

## Provenance and reproduction

Riot and Tencent provide competition metadata and series records. Leaguepedia supplies the ordered picks/bans under CC BY-SA 3.0. RiftWise supplies the archived player and gold-at-15 data. The source archive and the export carry multiple upstream sources. Follow the corresponding attribution and licensing terms for redistribution. [Riot](https://lolesports.com/en-GB/news/worlds-2026-primer) · [Tencent](https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_HOMEPAGE_BMATCH_LIST_246.js) · [Leaguepedia picks and bans](https://lol.fandom.com/wiki/2026_Season_World_Championship/Main_Event/Picks_and_Bans) · [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) · [RiftWise](https://riftwise.gg/stats/data)

```sh
./bench export --release datasets/replay-v3 --out .work/rl-eval --parquet
```

To use a loader that names its message column `messages`, call `train.rename_column("prompt", "messages")`. Install the optional project extra with `uv pip install --python .venv/bin/python '.[datasets]'` for local HF loading and Parquet export.

JSONL, ZIP and data-card generation use Python 3.12's standard library. Parquet generation additionally requires PyArrow; use the version recorded in the exported manifest to reproduce the shipped Parquet bytes.
