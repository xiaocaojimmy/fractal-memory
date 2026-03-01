# Fractal Memory System

## GitHub 发布指南

由于环境限制，GitHub推送需要手动完成。

### 快速发布步骤

1. **在GitHub创建仓库**
   - 访问：https://github.com/new
   - 仓库名：`fractal-memory`
   - 选择 Public
   - 点击 Create repository

2. **本地推送**
```bash
cd C:\Users\Administrator\.openclaw\workspace\experiments\fra\fractal_memory
git remote add origin https://github.com/YOUR_USERNAME/fractal-memory.git
git push -u origin master
```

3. **验证**
   - 访问 `https://github.com/YOUR_USERNAME/fractal-memory`
   - 确认代码已推送

### 可选：创建Release

1. 在GitHub页面点击 "Create a new release"
2. Tag: `v0.1.0`
3. Title: "Initial Release: Verified by Experiments #0-#5"
4. Description:
```
## Fractal Memory System v0.1.0

Based on complete experimental validation (#0-#5).

### Core Features
- External storage + camouflage injection
- 6-round adhesion window
- Ethics guard against hallucination
- Honesty-first principle

### Experimental Verification
- ✅ 7 adhesion threshold (exp #4b)
- ✅ 4/5 naturalness with camouflage (exp #3)
- ✅ Strict ethics mode (exp #5)

### Documentation
- [Full Report](./docs/Fractal_Memory_System_Report.md)
- [Philosophical Reflection](./docs/FRA_Philosophical_Reflection.md)
```

---

## 本地使用

仓库已初始化，可以直接使用：

```python
from core.memory import FractalMemory

memory = FractalMemory(model, adhesion_window=6)
```
