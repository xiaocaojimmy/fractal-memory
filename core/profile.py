"""
用户画像管理
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class UserProfile:
    """
    用户画像管理
    
    实现"结构痕迹"概念：
    - 不保存权重，保存知识拓扑
    - JSON格式，可跨会话、可携带
    """
    
    def __init__(self, storage_path: str = "./memory_store"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 画像结构
        self.data = {
            "identity": {},
            "context": {},
            "preferences": {},
            "facts": [],
            "_meta": {
                "version": "1.0",
                "created_at": None,
                "updated_at": None,
                "session_count": 0,
            }
        }
        
        self.profile_id = None
    
    def update(self, extracted: Dict) -> None:
        """
        更新画像
        
        基于价值系统优先级：
        identity (1.5) > context (1.2) > preferences (1.0) > facts (0.3)
        """
        if "identity" in extracted:
            self.data["identity"].update(extracted["identity"])
        
        if "context" in extracted:
            self.data["context"].update(extracted["context"])
        
        if "preferences" in extracted:
            self.data["preferences"].update(extracted["preferences"])
        
        # 更新时间戳
        self.data["_meta"]["updated_at"] = datetime.now().isoformat()
        if not self.data["_meta"]["created_at"]:
            self.data["_meta"]["created_at"] = datetime.now().isoformat()
    
    def has_relevant(self, query: str) -> bool:
        """检查是否有相关信息"""
        # 检查身份
        if self.data["identity"].get("职业"):
            return True
        
        # 检查上下文
        if self.data["context"].get("当前项目"):
            return True
        
        return False
    
    def get_relevant(self, query: str) -> Dict:
        """获取相关信息"""
        relevant = {}
        
        # 身份信息（最高优先级）
        if self.data["identity"]:
            relevant["identity"] = self.data["identity"]
        
        # 上下文信息
        if self.data["context"]:
            relevant["context"] = self.data["context"]
        
        return relevant
    
    def get_formatted_info(self) -> str:
        """获取格式化信息（用于注入）"""
        parts = []
        
        if self.data["identity"].get("职业"):
            parts.append(f"自己是{self.data['identity']['职业']}")
        
        if self.data["context"].get("当前项目"):
            parts.append(f"正在{self.data['context']['当前项目']}")
        
        return "，".join(parts) if parts else ""
    
    def get_summary(self) -> Dict:
        """获取画像摘要"""
        return {
            "identity_keys": list(self.data["identity"].keys()),
            "context_keys": list(self.data["context"].keys()),
            "facts_count": len(self.data["facts"]),
            "updated_at": self.data["_meta"]["updated_at"],
        }
    
    def save(self, profile_id: Optional[str] = None) -> str:
        """
        保存画像到文件
        
        这就是"结构痕迹"的持久化
        """
        if profile_id:
            self.profile_id = profile_id
        elif not self.profile_id:
            self.profile_id = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.storage_path, f"{self.profile_id}.json")
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load(self, profile_id: str) -> bool:
        """从文件加载画像"""
        filepath = os.path.join(self.storage_path, f"{profile_id}.json")
        
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        self.profile_id = profile_id
        self.data["_meta"]["session_count"] = self.data["_meta"].get("session_count", 0) + 1
        
        return True
