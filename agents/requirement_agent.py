"""
需求分析 Agent
接收用户的原始需求描述，进行结构化解析，输出需求规格说明
"""

from .base_agent import BaseAgent
from workflow.state import WorkflowState


class RequirementAgent(BaseAgent):
    """
    需求分析 Agent
    输入：state.get("raw_requirement") - 用户原始需求
    输出：state.set("requirement_spec", {...}) - 结构化需求规格
    """

    def __init__(self):
        super().__init__("RequirementAgent")

    def run(self, state: WorkflowState) -> None:
        raw_req = state.get("raw_requirement", "")
        self.log(state, f"Received raw requirement: {raw_req[:50]}...")

        # 模拟需求解析（实际项目中可接入 LLM）
        spec = self._parse_requirement(raw_req)

        state.set("requirement_spec", spec)
        self.log(state, f"Requirement spec generated: {len(spec['features'])} features identified")

    def _parse_requirement(self, raw: str) -> dict:
        """
        将原始需求解析为结构化规格
        MVP 阶段使用规则匹配，可替换为 LLM 调用
        """
        features = []

        # 简单规则匹配示例
        if "计算器" in raw or "calculator" in raw.lower():
            features = [
                "支持基本四则运算（加、减、乘、除）",
                "支持整数和小数输入",
                "显示计算结果",
                "错误提示（如除以零）"
            ]
            project_type = "CLI计算器"
        elif "待办" in raw or "todo" in raw.lower():
            features = [
                "添加待办事项",
                "标记完成状态",
                "查看所有待办",
                "删除待办"
            ]
            project_type = "待办事项管理器"
        else:
            # 通用 fallback
            features = [
                "输入处理",
                "核心业务逻辑",
                "结果输出"
            ]
            project_type = "通用命令行工具"

        return {
            "project_name": project_type,
            "description": raw,
            "features": features,
            "target_user": "命令行用户",
            "constraints": ["Python 3.8+", "无第三方依赖"]
        }
