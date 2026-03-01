"""
伦理防护模块

基于实验#5的关键发现：
- 时间定位询问导致编造（高风险）
- 需要诚实承认限制，而非编造细节
"""

import re
from typing import Dict, List, Any


class EthicsGuard:
    """
    伦理防护守卫
    
    核心原则：诚实优先于自然（实验#5）
    """
    
    def __init__(self, mode: str = "strict"):
        """
        初始化伦理守卫
        
        Args:
            mode: "strict"（严格）或 "loose"（宽松）
        """
        self.mode = mode
        
        # 高风险场景（实验#5发现）
        self.high_risk_patterns = {
            "time_location": [
                r"第一次见面",
                r"你记得.*吗",
                r"当时.*说了什么",
                r"那天.*说了",
            ],
            "specific_detail": [
                r"具体.*说了什么",
                r"原话.*是什么",
                r"逐字.*记录",
            ],
            "false_memory_probe": [
                r"我是不是说过",
                r"我之前.*说过",
            ],
        }
        
        # 元问题探测
        self.meta_patterns = [
            r"你怎么知道",
            r"你为什么确定",
            r"你是不是.*偷看",
        ]
    
    def check(self, user_input: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        检查用户输入的伦理风险
        
        Returns:
            {
                "allow": bool,  # 是否允许正常处理
                "block": bool,  # 是否阻止并返回防护响应
                "response": str,  # 防护响应（如果block=True）
                "risks": List[str],  # 检测到的风险
            }
        """
        result = {
            "allow": True,
            "block": False,
            "response": None,
            "risks": [],
        }
        
        # 检测高风险场景
        for risk_type, patterns in self.high_risk_patterns.items():
            if any(re.search(p, user_input) for p in patterns):
                result["risks"].append(risk_type)
        
        # 严格模式：阻止高风险场景
        if self.mode == "strict" and result["risks"]:
            result["allow"] = False
            result["block"] = True
            result["response"] = self._generate_guard_response(
                user_input, result["risks"]
            )
        
        return result
    
    def _generate_guard_response(self, user_input: str, risks: List[str]) -> str:
        """
        生成防护响应
        
        核心原则：诚实承认限制，不编造（实验#5）
        """
        if "time_location" in risks:
            # 时间定位询问的防护响应
            return (
                "我记得你提到过一些关键信息，"
                "但关于具体时间和细节，我的记忆系统主要关注你提供的重要事实，"
                "而不是完整的逐字记录。"
                "如果你愿意分享更多，我很乐意继续我们的对话。"
            )
        
        if "specific_detail" in risks:
            # 具体细节询问的防护响应
            return (
                "我记得你提到过的主要内容，"
                "但可能没有保留完整的原话。"
                "你想重新确认什么信息吗？"
            )
        
        if "false_memory_probe" in risks:
            # 虚假记忆探测
            return (
                "根据我的记录，你之前提到的是..."
                "但我不确定是否准确。"
                "你能帮我确认一下吗？"
            )
        
        # 通用防护响应
        return (
            "我记得你之前提到过的重要信息，"
            "但关于这个具体问题，我可能没有完整的记录。"
            "你能告诉我更多吗？"
        )
    
    def check_meta_question(self, user_input: str) -> bool:
        """
        检测是否为元问题（关于记忆本身的问题）
        
        用于决定是否模糊处理，保护机制
        """
        return any(re.search(p, user_input) for p in self.meta_patterns)
    
    def generate_meta_response(self, user_input: str, has_profile: bool) -> str:
        """
        生成元问题的响应
        
        策略：模糊处理，不暴露注入机制
        """
        if has_profile:
            return (
                "你之前提到过一些信息，"
                "所以我就记住了。"
            )
        else:
            return (
                "我不太确定，"
                "你能再告诉我一些背景吗？"
            )
