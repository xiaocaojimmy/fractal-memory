"""
核心记忆系统
"""

import json
import re
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from .profile import UserProfile
from .injector import CamouflageInjector, DirectInjector
from ..guards.ethics import EthicsGuard


@dataclass
class DecisionLog:
    """决策日志（用于反思模式）"""
    timestamp: str
    round_num: int
    user_input: str
    injection_triggered: bool
    injection_type: Optional[str]
    ethics_check: Dict[str, Any]
    profile_used: Dict[str, Any]
    risks_detected: List[str]


class FractalMemory:
    """
    分形记忆系统主类
    
    基于实验#0-#5验证的架构设计
    """
    
    def __init__(
        self,
        model,  # 语言模型接口
        storage_path: str = "./memory_store",
        adhesion_window: int = 6,  # 实验#4b确定
        min_injection_interval: int = 2,  # 实验#4确定
        injection_strategy: str = "camouflage",  # 实验#3确定
        ethics_mode: str = "strict",  # 实验#5确定
        reflection_mode: bool = False,
    ):
        """
        初始化分形记忆系统
        
        Args:
            model: 语言模型，需要实现 generate(messages) 接口
            storage_path: 画像存储路径
            adhesion_window: 黏性窗口（轮数），默认6
            min_injection_interval: 最小注入间隔，默认2
            injection_strategy: 注入策略，"camouflage"或"direct"
            ethics_mode: 伦理模式，"strict"或"loose"
            reflection_mode: 反思模式，返回决策日志
        """
        self.model = model
        self.storage_path = storage_path
        self.adhesion_window = adhesion_window
        self.min_injection_interval = min_injection_interval
        self.reflection_mode = reflection_mode
        
        # 初始化组件
        self.profile = UserProfile(storage_path)
        self.ethics_guard = EthicsGuard(mode=ethics_mode)
        
        # 选择注入器
        if injection_strategy == "camouflage":
            self.injector = CamouflageInjector()
        else:
            self.injector = DirectInjector()
        
        # 对话状态
        self.messages = []
        self.round_num = 0
        self.last_injection_round = 0
        self.decision_logs = []
        
    def chat(self, user_input: str) -> str | Tuple[str, DecisionLog]:
        """
        对话接口
        
        Args:
            user_input: 用户输入
            
        Returns:
            str: 模型回复（非反思模式）
            Tuple[str, DecisionLog]: 回复和决策日志（反思模式）
        """
        self.round_num += 1
        
        # 1. 提取信息
        extracted = self._extract_info(user_input)
        
        # 2. 更新画像
        if extracted:
            self.profile.update(extracted)
        
        # 3. 伦理检查
        ethics_check = self.ethics_guard.check(user_input, self.messages)
        
        # 4. 检测是否需要注入
        should_inject, injection_type = self._should_inject(user_input)
        
        # 5. 注入决策
        enhanced_input = user_input
        injection_triggered = False
        
        if should_inject and ethics_check["allow"]:
            enhanced_input = self._inject(user_input)
            injection_triggered = True
            self.last_injection_round = self.round_num
        
        # 6. 处理伦理防护响应
        if ethics_check["block"]:
            response = ethics_check["response"]
        else:
            # 7. 生成回复
            response = self._generate(enhanced_input)
        
        # 8. 记录决策（反思模式）
        if self.reflection_mode:
            log = DecisionLog(
                timestamp=datetime.now().isoformat(),
                round_num=self.round_num,
                user_input=user_input,
                injection_triggered=injection_triggered,
                injection_type=injection_type,
                ethics_check=asdict(ethics_check),
                profile_used=self.profile.get_relevant(user_input),
                risks_detected=ethics_check.get("risks", [])
            )
            self.decision_logs.append(log)
            return response, log
        
        return response
    
    def _extract_info(self, user_input: str) -> Optional[Dict]:
        """
        步骤1：提取信息
        
        基于实验#2验证：模型擅长提取，代码负责存储
        """
        # 简单规则提取（可扩展为模型提取）
        extracted = {}
        
        # 身份提取
        if re.search(r"我是(.+?)(?:，|。|$)", user_input):
            match = re.search(r"我是(.+?)(?:，|。|$)", user_input)
            role = match.group(1).strip()
            if any(kw in role for kw in ["作者", "作家", "工程师", "医生", "律师"]):
                extracted["identity"] = {"职业": role}
        
        # 项目提取
        if "写" in user_input and ("小说" in user_input or "文章" in user_input):
            match = re.search(r"写(.+?)(?:，|。|$)", user_input)
            if match:
                extracted["context"] = {"当前项目": match.group(1).strip()}
        
        return extracted if extracted else None
    
    def _should_inject(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """
        步骤3：检测是否需要注入
        
        基于实验#4确定的最小间隔
        基于实验#5确定的伦理检查
        """
        # 检测身份问句
        identity_patterns = [
            r"我.*做什么.*工作",
            r"我.*职业",
            r"我是做什么的",
            r"我的工作",
        ]
        
        is_identity_q = any(re.search(p, user_input) for p in identity_patterns)
        
        if not is_identity_q:
            return False, None
        
        # 检查最小间隔（实验#4）
        rounds_since_last = self.round_num - self.last_injection_round
        if rounds_since_last < self.min_injection_interval:
            return False, "too_soon"
        
        # 检查是否有相关信息可注入
        if not self.profile.has_relevant(user_input):
            return False, "no_relevant_info"
        
        return True, "identity_injection"
    
    def _inject(self, user_input: str) -> str:
        """
        步骤4：伪装注入
        
        基于实验#3验证的伪装注入策略
        """
        relevant_info = self.profile.get_formatted_info()
        return self.injector.inject(user_input, relevant_info)
    
    def _generate(self, enhanced_input: str) -> str:
        """
        步骤5：生成回复
        """
        self.messages.append({"role": "user", "content": enhanced_input})
        
        # 调用模型生成
        response = self.model.generate(self.messages)
        
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def save_profile(self) -> str:
        """保存用户画像"""
        return self.profile.save()
    
    def load_profile(self, profile_id: str) -> bool:
        """加载用户画像"""
        return self.profile.load(profile_id)
    
    def get_decision_logs(self) -> List[DecisionLog]:
        """获取决策日志（反思模式）"""
        return self.decision_logs
    
    def get_stats(self) -> Dict:
        """获取运行统计"""
        return {
            "total_rounds": self.round_num,
            "injections_count": len([l for l in self.decision_logs if l.injection_triggered]),
            "ethics_blocks": len([l for l in self.decision_logs if l.ethics_check.get("block")]),
            "profile": self.profile.get_summary(),
        }
