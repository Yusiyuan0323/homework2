"""
Workflow 引擎模块
负责任务编排、顺序执行、状态流转和错误处理
"""

from typing import List, Callable, Optional
from .state import WorkflowState


class WorkflowEngine:
    """
    简单的顺序执行 Workflow 引擎
    支持：顺序执行、错误中断、状态追踪
    扩展方向：条件分支、循环、并行执行
    """

    def __init__(self, name: str = "default_workflow"):
        self.name = name
        self._nodes: List[dict] = []  # 节点列表：{name, agent, condition}
        self._on_step_end: Optional[Callable] = None

    def add_node(self, name: str, agent, condition: Optional[Callable] = None) -> "WorkflowEngine":
        """
        添加一个节点到流程末尾
        :param name: 节点名称
        :param agent: Agent 实例（必须实现 run(state) 方法）
        :param condition: 可选条件函数，返回 True 才执行该节点
        """
        self._nodes.append({
            "name": name,
            "agent": agent,
            "condition": condition
        })
        return self  # 支持链式调用

    def set_step_callback(self, callback: Callable) -> "WorkflowEngine":
        """设置每步执行后的回调（用于可视化/日志）"""
        self._on_step_end = callback
        return self

    def run(self, initial_state: WorkflowState) -> WorkflowState:
        """
        执行整个 Workflow
        :param initial_state: 初始状态
        :return: 最终状态
        """
        initial_state.log("Engine", f"Workflow '{self.name}' started with {len(self._nodes)} nodes")

        for i, node in enumerate(self._nodes):
            node_name = node["name"]
            agent = node["agent"]
            condition = node["condition"]

            # 检查条件
            if condition is not None and not condition(initial_state):
                initial_state.log("Engine", f"Node '{node_name}' skipped (condition not met)")
                continue

            # 设置当前节点
            initial_state.current_node = node_name
            initial_state.log("Engine", f"[{i+1}/{len(self._nodes)}] Entering node: {node_name}")

            try:
                # 执行 Agent
                agent.run(initial_state)

                # 步骤回调
                if self._on_step_end:
                    self._on_step_end(node_name, initial_state)

            except Exception as e:
                initial_state.set_error(f"Node '{node_name}' failed: {str(e)}")
                initial_state.log("Engine", f"Workflow aborted at node '{node_name}'", level="ERROR")
                return initial_state

            initial_state.log("Engine", f"[{i+1}/{len(self._nodes)}] Node '{node_name}' completed")

        initial_state.mark_completed()
        initial_state.log("Engine", f"Workflow '{self.name}' completed successfully")
        return initial_state

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    def describe(self) -> str:
        """返回流程描述"""
        lines = [f"Workflow: {self.name} ({len(self._nodes)} nodes)"]
        for i, node in enumerate(self._nodes):
            lines.append(f"  {i+1}. {node['name']}")
        return "\n".join(lines)
