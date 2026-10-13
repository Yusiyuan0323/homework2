"""
Workflow 状态管理模块
负责在 Agent 之间共享和传递状态数据
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json


class WorkflowState:
    """
    Workflow 全局状态对象
    所有 Agent 共享同一个状态实例，通过读写状态实现通信
    """

    def __init__(self, initial_input: Optional[Dict[str, Any]] = None):
        # 核心数据存储
        self._data: Dict[str, Any] = initial_input or {}
        # 执行日志
        self._logs: List[Dict[str, Any]] = []
        # 当前执行到的节点
        self._current_node: Optional[str] = None
        # 流程是否完成
        self._completed: bool = False
        # 错误信息
        self._error: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        """读取状态数据"""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """写入状态数据"""
        self._data[key] = value

    def update(self, values: Dict[str, Any]) -> None:
        """批量更新状态"""
        self._data.update(values)

    @property
    def data(self) -> Dict[str, Any]:
        """获取全部数据（只读视图）"""
        return self._data.copy()

    def log(self, agent_name: str, message: str, level: str = "INFO") -> None:
        """记录执行日志"""
        self._logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "level": level,
            "message": message
        })

    @property
    def logs(self) -> List[Dict[str, Any]]:
        """获取执行日志"""
        return self._logs.copy()

    @property
    def current_node(self) -> Optional[str]:
        return self._current_node

    @current_node.setter
    def current_node(self, node: str) -> None:
        self._current_node = node

    @property
    def is_completed(self) -> bool:
        return self._completed

    def mark_completed(self) -> None:
        self._completed = True

    @property
    def error(self) -> Optional[str]:
        return self._error

    def set_error(self, error: str) -> None:
        self._error = error
        self.log("System", f"Error: {error}", level="ERROR")

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "data": self._data,
            "logs": self._logs,
            "current_node": self._current_node,
            "completed": self._completed,
            "error": self._error
        }

    def save_to_file(self, filepath: str) -> None:
        """将状态保存到 JSON 文件"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def __repr__(self) -> str:
        return f"WorkflowState(keys={list(self._data.keys())}, node={self._current_node})"
