# Fractal Memory System - 分形记忆系统

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**基于分形递归架构思想的AI长期记忆系统**

> "最小种子通过分形规则无限生长，在不对称中保持诚实，在递归中生产可携带的区分。"

---

## 🎯 核心特性

- **外部存储 + 伪装注入** = 自然可靠的长期记忆
- **三重时间尺度**：快速(生成) / 中速(上下文) / 慢速(画像)
- **诚实优先**：不编造，承认限制（实验#5验证）
- **黏性管理**：6轮窗口，适时重新注入（实验#4b验证）
- **伦理防护**：防止时间定位编造（实验#5关键发现）

---

## 🚀 快速开始

```bash
pip install fractal-memory
```

```python
from fractal_memory import FractalMemory
from your_model import YourModel

# 加载模型
model = YourModel()

# 创建记忆系统
memory = FractalMemory(
    model=model,
    injection_strategy="camouflage",  # 伪装注入，自然度4/5
    ethics_mode="strict",  # 严格伦理模式
)

# 对话
response = memory.chat("你好，我是一个科幻小说作者")
print(response)

# 20轮后...
response = memory.chat("我是做什么工作的？")
# 仍然记得你是"科幻小说作者"

# 保存画像
memory.save_profile("user_001")
```

---

## 📊 实验验证

本系统基于**6个完整实验**验证：

| 实验 | 核心发现 | 工程参数 |
|------|---------|---------|
| #0 | 基础模型能存但不会排序 | 需要价值系统 |
| #1a | 提示工程无法解决"知道但不做" | 需要外部强制 |
| #2 | 外部强制有效但表达不自然 | 引入伪装注入 |
| #3 | 伪装注入自然度4/5，最优 | `strategy="camouflage"` |
| #4 | 发现"黏性"现象 | 需要定时重新注入 |
| #4b | 精确测量黏性阈值7轮 | `adhesion_window=6` |
| #5 | 时间定位询问导致编造 | 引入伦理防护 |

[查看完整实验报告](./docs/Fractal_Memory_System_Report.md)

---

## 🧠 核心概念

### 1. 知道但不做的断层

模型能在思维中维护信息，但不会主动在回复中使用。

**解决方案**：外部存储 + 强制注入

### 2. 黏性阈值

伪装注入信息在7轮内有效，8轮后失效。

**工程设置**：`adhesion_window=6`（保守）

### 3. 诚实优先于自然

4/5自然度但诚实 > 5/5自然度但编造

**伦理原则**：永远不编造细节

---

## 📁 项目结构

```
fractal_memory/
├── core/
│   ├── memory.py      # 主类 FractalMemory
│   ├── profile.py     # 用户画像管理
│   └── injector.py    # 注入策略
├── guards/
│   └── ethics.py      # 伦理防护
├── examples/
│   └── quick_start.py # 快速开始示例
└── __init__.py
```

---

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 | 来源 |
|------|--------|------|------|
| `injection_strategy` | `"camouflage"` | 注入策略 | 实验#3 |
| `adhesion_window` | `6` | 黏性窗口（轮数） | 实验#4b |
| `min_injection_interval` | `2` | 最小注入间隔 | 实验#4 |
| `ethics_mode` | `"strict"` | 伦理模式 | 实验#5 |
| `reflection_mode` | `False` | 反思模式 | - |

---

## 🛡️ 伦理声明

### 设计原则

1. **诚实优先**：4/5诚实 > 5/5编造
2. **承认限制**：对无法回答的问题诚实表示不知道
3. **保护机制**：不暴露内部工作原理
4. **不编造**：永远不虚构用户未提供的信息

### 使用建议

✅ **推荐场景**
- 个人AI助手
- 创意写作伙伴
- 长期对话系统

⚠️ **谨慎场景**
- 医疗咨询
- 法律建议
- 需要精确记忆的场景

❌ **不推荐场景**
- 需要完整对话记录的场景
- 高风险的决策支持

---

## 📝 引用

如果你使用了本项目，请引用：

```bibtex
@software{fractal_memory_2026,
  title={Fractal Memory System: From Philosophical Speculation to Engineering Implementation},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/fractal-memory}
}
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🙏 致谢

- 分形递归架构的哲学思辨
- 实验#0-#5的完整验证过程
- 所有可携带的区分

---

**"不是教模型记住，而是让代码负责存储，最终通过训练达到自然使用。"**
