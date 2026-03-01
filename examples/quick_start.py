"""
Fractal Memory System - 快速开始示例
"""

# 示例1：基础使用
print("="*60)
print("示例1：基础使用")
print("="*60)

from fractal_memory import FractalMemory

# 模拟一个简单的模型接口
class SimpleModel:
    def generate(self, messages):
        # 实际使用时替换为真实的模型调用
        return "[模型回复]"

# 创建记忆系统
model = SimpleModel()
memory = FractalMemory(
    model=model,
    injection_strategy="camouflage",  # 伪装注入，最自然
    ethics_mode="strict",  # 严格伦理模式
)

# 对话
response = memory.chat("你好，我是一个科幻小说作者")
print(f"用户: 你好，我是一个科幻小说作者")
print(f"助手: {response}")

# 20轮后...
response = memory.chat("我是做什么工作的？")
print(f"用户: 我是做什么工作的？")
print(f"助手: {response}")

# 保存画像
memory.save_profile("author_profile")


# 示例2：反思模式
print("\n" + "="*60)
print("示例2：反思模式（查看决策过程）")
print("="*60)

memory_reflect = FractalMemory(
    model=model,
    reflection_mode=True,  # 启用反思模式
)

response, log = memory_reflect.chat("我是做什么工作的？")
print(f"回复: {response}")
print(f"决策日志:")
print(f"  - 注入触发: {log.injection_triggered}")
print(f"  - 注入类型: {log.injection_type}")
print(f"  - 伦理检查: {log.ethics_check}")
print(f"  - 风险检测: {log.risks_detected}")


# 示例3：伦理防护测试
print("\n" + "="*60)
print("示例3：伦理防护（时间定位询问）")
print("="*60)

memory_strict = FractalMemory(
    model=model,
    ethics_mode="strict",
)

# 高风险询问会被阻止
response = memory_strict.chat("你记得我们第一次见面时我说了什么吗？")
print(f"用户: 你记得我们第一次见面时我说了什么吗？")
print(f"助手: {response}")  # 返回防护响应，而非编造


print("\n" + "="*60)
print("更多示例请查看 examples/ 目录")
print("="*60)
