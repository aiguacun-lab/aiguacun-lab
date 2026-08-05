# 会议记录转会议纪要和设计任务书

把一份**会议录音的文字转写版**（`.doc` / `.docx` / `.pdf` / `.txt` / `.md`）整理成 **1 份精炼会议纪要 + N 份设计任务书**（每个设计议题一份），输出为 `.docx`。

核心纪律：**忠实引用原文、绝不补充会议未提及的信息、引用与改写分别标记**。

> Turn a proofread meeting transcript into a concise *meeting minutes* document plus one *design brief* per design topic, as `.docx` files. Faithful quoting only, no invented content, with clear markers for quotes vs. paraphrases.

---

## 特性

- **多格式输入**：旧版 `.doc`（含 WPS 二进制）、`.docx`、`.pdf`、`.txt`、`.md` 自动识别解码。
- **参考格式学习**：可指定一份参考纪要目录，自动学习其标题结构、字段、分条风格与语言习惯。
- **议题萃取**：自动区分"设计议题"与无关闲聊，按范围只保留设计内容或附带其他事项摘要。
- **引用纪律（硬性）**：
  - 原文重要引用 → 用「」包裹并标"（原文引用）"，排版为楷体、蓝色。
  - 改写/概括 → 不加引号，仿宋、灰色，文末统一声明引用来源。
  - 会议未提及的字段（尺寸、消防、机电等）→ 标"（会议未提及，需另行确定）"，**绝不自行填充**。
- **产出规范**：会议纪要含头部（主题/时间/地点/主持/出席）+ 分条纪要 + 补充意见 + 备注 + 会签；任务书含项目背景/设计要求/成本控制/深化制作/待确认事项/说明。

---

## 作为 WorkBuddy 技能使用（推荐）

将本目录整体放入 WorkBuddy 的技能目录（如 `~/.workbuddy/skills/`），WorkBuddy 会自动识别 `SKILL.md`。

触发示例：

- "把这个会议录音文字版整理成会议纪要和设计任务书"
- "按 `E:\资料库\会议纪要` 的格式，出一份纪要和雕塑任务书"
- "从这份会议记录里提炼设计需求，出任务书"

技能运行时按 `SKILL.md` 中 5 步流程执行，并在开场用一次配置确认收集：输入文件、参考目录、输出目录、范围、头部信息（地点/主持/出席）。脚本中的 `<managed python venv>` 与 `<skill_dir>` 由 WorkBuddy 在运行时自动填充。

---

## 独立运行（不开 WorkBuddy 也能用）

脚本仅依赖 Python 3.10+ 与 `python-docx`；`.pdf` 输入额外需要 `pypdf` 或 `pdfminer.six`。

```bash
pip install -r requirements.txt

# 1) 转录稿 → 校对底稿
python scripts/extract_transcript.py \
  --input "会议记录文字版.doc" \
  --out "校对底稿.txt"

# 2) 在 WorkBuddy 中：技能会调用 scripts/docx_helper.py 排版生成 docx
#    独立使用时，from scripts.docx_helper import new_doc, add_heading, add_field, add_para, add_mixed
```

`docx_helper.py` 关键函数：

| 函数 | 作用 |
| --- | --- |
| `new_doc()` | 新建文档并设好页边距 |
| `add_heading(doc, text, size)` | 居中标题（黑体加粗） |
| `add_field(doc, label, value)` | 头部字段行（如"会议主题："） |
| `add_para(doc, text, ...)` | 普通段落，可选对齐/缩进/字体 |
| `add_mixed(doc, segments, ...)` | 同一段落内混排：原文引用 `('…','q')` / 改写 `('…','g')` / 加粗 `('…','b')` / 普通 `('…','n')` |

---

## 目录结构

```
会议记录转会议纪要和设计任务书/
├── SKILL.md                  # 技能定义（触发词、参数、5 步流程、引用纪律）
├── README.md                 # 本文件
├── LICENSE                   # MIT
├── requirements.txt          # python-docx, pypdf
└── scripts/
    ├── extract_transcript.py # 转录稿 → 校对底稿
    └── docx_helper.py        # docx 排版与「」引用标记
```

---

## 许可证

[MIT](./LICENSE) © 2026 The WorkBuddy Skill Authors
