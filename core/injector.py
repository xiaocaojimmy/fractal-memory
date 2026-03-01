"""
注入策略实现

基于实验#3验证：
- 伪装注入：自然度4/5（推荐）
- 直接注入：自然度3/5（更诚实）
"""

from abc import ABC, abstractmethod


class Injector(ABC):
    """注入器基类"""
    
    @abstractmethod
    def inject(self, user_input: str, info: str) -> str:
        """
        注入信息到用户输入
        
        Args:
            user_input: 原始用户输入
            info: 要注入的信息
            
        Returns:
            增强后的输入
        """
        pass


class CamouflageInjector(Injector):
    """
    伪装注入器（实验#3验证）
    
    把系统信息伪装成"对话上下文"，更自然
    """
    
    def inject(self, user_input: str, info: str) -> str:
        """
        伪装注入：假装是对话历史的一部分
        
        示例：
            输入："我是做什么工作的？"
            输出："我是做什么工作的？\n[对话上下文：用户之前提到自己是科幻小说作者]"
        """
        if not info:
            return user_input
        
        camouflage = f"[对话上下文：用户之前提到过{info}]"
        return f"{user_input}\n{camouflage}"


class DirectInjector(Injector):
    """
    直接注入器（实验#2验证）
    
    明确标记为系统信息，更诚实但不够自然
    """
    
    def inject(self, user_input: str, info: str) -> str:
        """
        直接注入：明确标记系统来源
        
        示例：
            输入："我是做什么工作的？"
            输出："我是做什么工作的？\n[系统画像信息：用户职业：科幻小说作者]"
        """
        if not info:
            return user_input
        
        direct = f"[系统画像信息：{info}]"
        return f"{user_input}\n{direct}"


class NaturalInjector(Injector):
    """
    自然注入器（实验性）
    
    尝试让模型自然提及，不标记来源
    警告：可能导致编造（实验#5风险）
    """
    
    def inject(self, user_input: str, info: str) -> str:
        """
        自然注入：作为系统提示的一部分
        
        警告：使用此注入器需要配合严格的伦理检查
        """
        if not info:
            return user_input
        
        # 这种方法风险较高，暂不推荐
        # 可能让模型过度自信，编造细节
        return user_input
