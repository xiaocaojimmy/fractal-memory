"""
Fractal Memory System - 分形记忆系统

基于分形递归架构思想实现的AI长期记忆系统。

核心设计：
- 外部存储 + 伪装注入 = 自然可靠的长期记忆
- 三重时间尺度：快速(生成) / 中速(上下文) / 慢速(画像)
- 诚实优先：不编造，承认限制
- 黏性管理：6轮窗口，适时重新注入

实验验证：#0-#5完整测试
"""

from .core.memory import FractalMemory
from .core.profile import UserProfile
from .core.injector import CamouflageInjector, DirectInjector
from .guards.ethics import EthicsGuard

__version__ = "0.1.0"
__all__ = [
    "FractalMemory",
    "UserProfile",
    "CamouflageInjector",
    "DirectInjector",
    "EthicsGuard",
]

# 实验验证的核心参数
ADHESION_WINDOW = 6  # 实验#4b: 7轮阈值，6轮保守设置
MIN_INJECTION_INTERVAL = 2  # 实验#4: 避免连续注入

# 注入策略效果（实验#3）
INJECTION_STRATEGIES = {
    "camouflage": {"naturalness": 4, "description": "伪装注入，最自然"},
    "direct": {"naturalness": 3, "description": "直接注入，更诚实"},
}
