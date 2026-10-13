"""
Agent 基类
所有具体 Agent 必须继承此类并实现 run() 方法
"""

from abc import ABC, abstractmethod
from workflow.state import WorkflowState


class BaseAgent(ABC):
    """
    Agent 抽象基类
    定义了 Agent 的统一接口：接收状态 -> 处理 -> 写回状态
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state: WorkflowState) -> None:
        """
        执行 Agent 的核心逻辑
        :param state: Workflow 共享状态，Agent 通过读写 state 与其他节点通信
        """
        pass

    def log(self, state: WorkflowState, message: str, level: str = "INFO") -> None:
        """记录日志到状态对象"""
        state.log(self.name, message, level)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.name}'>"
