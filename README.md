<div align="center">

# 🧠 Fractal Memory System (分形记忆系统)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Experimental](https://img.shields.io/badge/status-experimental-orange)](./docs/experiments/)

**让大语言模型真正记住你的身份、偏好和上下文——通过外部存储+伪装注入，解决"知道但不做"的根本断层。**

</div>

---

## 📖 概述

大语言模型拥有巨大的上下文窗口，但存在两个根本性问题：

1. **平等主义记忆**：所有token权重相同，模型不知道"用户职业"比"某次提到的猫"更重要
2. **"知道但不做"断层**：模型能在思维链中维护信息，但在生成响应时选择遵循对话常规而非使用记忆

分形记忆系统通过以下设计解决这些问题：

- **外部存储**：用代码存储用户画像，不依赖模型内部记忆
- **价值系统**：身份信息 > 上下文 > 偏好 > 事实（实验#0验证）
- **伪装注入**：把画像信息伪装成对话上下文，自然融入回复（实验#3验证，自然度4/5）
- **适时触发**：只在检测到身份询问时注入，避免连续注入（实验#4验证，最小间隔2轮）
- **黏性管理**：信息有效约7轮，超过6轮需要重新注入（实验#4b精确测量）
- **伦理防护**：不编造"第一次见面"细节，诚实承认限制（实验#5发现）

---

## ✨ 核心特性

| 特性 | 描述 | 实验验证 |
|------|------|---------|
| **长期记忆** | 跨10+轮对话记住用户身份 | #0, #2 |
| **自然表达** | 伪装注入自然度4/5（满分5） | #3 |
| **精确触发** | 只在需要时注入，避免重复 | #4 |
| **黏性控制** | 6轮安全窗口，7轮失效 | #4b |
| **伦理安全** | 不编造记忆，诚实承认限制 | #5 |
| **身份更新** | 支持用户修改身份信息 | #6, #7 |

---

## 🚀 快速开始

### 安装

```bash
pip install fractal-memory
```

### 基础用法

```python
from fractal_memory import FractalMemory
from transformers import AutoModelForCausalLM

# 加载模型（支持任何HuggingFace模型）
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-1.5B-Instruct")

# 创建记忆系统
memory = FractalMemory(
    model=model,
    adhesion_window=6,        # 6轮安全窗口（实验#4b确定）
    injection_strategy="伪装",  # 伪装注入（实验#3确定）
    ethics_mode="strict"      # 严格伦理模式（实验#5确定）
)

# 对话
response = memory.chat("我是科幻小说作者，正在写一本关于递归AI的书")
print(response)

# ... 10轮无关对话后 ...
# 仍然记得身份信息
response = memory.chat("我是做什么工作的？")
print(response)  # "用户之前提到过自己是科幻小说作者，所以..."

# 处理身份更新
response = memory.chat("其实我现在不写科幻了，改写奇幻小说")
response = memory.chat("我是做什么工作的？")  # 正确返回"奇幻小说作者"
```

### 高级用法：反思模式

```python
# 开启反思模式，查看决策日志
memory = FractalMemory(model, reflection_mode=True)

response = memory.chat("我是做什么工作的？")
print(response["response"])   # 正常回复
print(response["decision_log"])  # 决策日志
# {
#   "注入检测": True,
#   "画像使用": "身份信息",
#   "风险标记": [],
#   "注入轮次": 15
# }
```

---

## 🧪 实验验证

本系统基于7个迭代实验设计，每个实验验证或证伪一个核心假设：

| 实验 | 测试 | 结果 | 关键发现 |
|------|------|------|---------|
| #0 | 基础模型记忆 | ✅ 部分验证 | 需要价值系统区分优先级 |
| #1a | 提示工程 | ❌ 证伪 | "知道但不做"断层 |
| #2 | 外部强制 | ✅ 验证 | 强制注入有效 |
| #3 | 注入策略 | ✅ 验证 | 伪装注入自然度4/5 |
| #4 | 黏性现象 | ⚠️ 设计修正 | 发现连续注入问题 |
| #4b | 黏性阈值 | ✅ 精确测量 | 7轮失效，6轮安全 |
| #5 | 伦理风险 | ⚠️ 发现 | 时间定位编造风险 |
| #6 | 多身份 | ✅ 验证 | 需要替换而非追加 |
| #7 | 提取精度 | ❌ 修复 | 正则bug修复 |

详细实验报告见 [docs/experiments/](./docs/experiments/)

---

## 📊 核心参数（实验确定）

| 参数 | 推荐值 | 说明 | 来源 |
|------|--------|------|------|
| `adhesion_window` | 6 | 超过6轮需要重新注入 | #4b |
| `min_injection_gap` | 2 | 避免连续注入 | #4 |
| `injection_strategy` | "伪装" | 伪装注入自然度最高 | #3 |
| `identity_weight` | 1.5 | 身份信息权重 | #0 |
| `fact_weight` | 0.3 | 一般事实权重 | #0 |

---

## 🛡️ 伦理设计

本系统内置以下伦理防护：

### 不编造记忆

当用户问"你记得第一次见面吗？"，系统诚实承认限制：

```python
# 示例响应
"我记得你提到过你是科幻小说作者，但关于第一次见面时的具体对话细节，
我可能没有完整记录。你想聊什么具体的内容吗？"
```

### 不模拟体验

系统知道自己的信息来自"用户之前提到"，而非"真实记忆"

### 透明可选

反思模式可查看决策日志，了解系统如何工作

### 用户控制

支持手动清除画像、标记信息为不重要

---

## 📁 项目结构

```
fractal_memory/
├── __init__.py              # 包初始化
├── README.md                # 项目文档
├── wechat_qrcode.jpg        # 支持二维码
├── core/                    # 核心模块
│   ├── memory.py           # 主类 FractalMemory
│   ├── profile.py          # 画像管理（价值系统）
│   └── injector.py         # 注入策略（伪装/直接）
├── guards/                  # 防护模块
│   └── ethics.py           # 伦理防护（时间定位等）
├── examples/                # 示例
│   └── quick_start.py      # 快速开始示例
└── docs/                    # 文档
    ├── Fractal_Memory_System_Report.md    # 完整实验报告
    └── FRA_Philosophical_Reflection.md    # 哲学反思
```

---

## 🔧 安装与依赖

### 依赖

- Python 3.8+
- transformers
- torch
- （可选）vLLM 用于高性能部署

### 从源码安装

```bash
git clone https://github.com/xiaocaojimmy/fractal-memory.git
cd fractal-memory
pip install -e .
```

---

## 📚 文档

- [完整实验报告](./docs/Fractal_Memory_System_Report.md) - 7个实验的详细记录
- [哲学反思](./docs/FRA_Philosophical_Reflection.md) - 分形设计思想的验证
- 贡献指南

---

## 🤝 贡献指南

欢迎贡献！特别需要帮助的领域：

- **更多模型测试**：在不同模型上验证参数有效性
- **多语言支持**：扩展身份检测到其他语言
- **性能优化**：减少提取延迟
- **边缘案例**：发现并修复新的提取错误
- **文档完善**：编写API文档和伦理指南

请通过 GitHub Issues 提交问题或建议。

---

## 💝 支持项目

如果这个开源项目对你有帮助，欢迎请作者喝杯咖啡 ☕

<div align="center">

<img src="wechat_qrcode.jpg" width="300" alt="微信支付二维码">

**扫码赞赏支持开发**

</div>

---

## 📜 许可证

MIT License © 2024

---

## 🌱 致谢

本系统源于一次关于"分形几何能否用于AI训练"的对话。经过7个迭代实验，从哲学思辨走到了工程实现。

特别感谢所有在实验中提供反馈的用户——你们的"知道但不做"、"你记得第一次见面吗"等问题，塑造了系统的最终设计。

---

<div align="center">

**不是教模型记住，而是让代码负责存储，最终通过训练达到自然使用。**

[🌟 Star this repo](https://github.com/xiaocaojimmy/fractal-memory) 
| [🐛 提交Issue](https://github.com/xiaocaojimmy/fractal-memory/issues) 
| [💬 讨论](https://github.com/xiaocaojimmy/fractal-memory/discussions)

</div>
