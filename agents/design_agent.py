"""
系统设计 Agent
接收结构化需求，输出技术设计方案（模块划分、接口定义、数据结构）
"""

from .base_agent import BaseAgent
from workflow.state import WorkflowState


class DesignAgent(BaseAgent):
    """
    系统设计 Agent
    输入：state.get("requirement_spec") - 结构化需求
    输出：state.set("design_doc", {...}) - 技术设计文档
    """

    def __init__(self):
        super().__init__("DesignAgent")

    def run(self, state: WorkflowState) -> None:
        spec = state.get("requirement_spec")
        if not spec:
            raise ValueError("requirement_spec not found in state")

        self.log(state, f"Designing for project: {spec['project_name']}")

        design = self._create_design(spec)

        state.set("design_doc", design)
        self.log(state, f"Design doc generated: {len(design['modules'])} modules, {len(design['interfaces'])} interfaces")

    def _create_design(self, spec: dict) -> dict:
        """根据需求生成技术设计"""
        project_name = spec["project_name"]
        features = spec["features"]

        # 根据项目类型生成不同的设计
        if "计算器" in project_name:
            modules = [
                {"name": "Calculator", "responsibility": "核心计算逻辑"},
                {"name": "Parser", "responsibility": "输入解析与校验"},
                {"name": "UI", "responsibility": "命令行交互与结果展示"}
            ]
            interfaces = [
                {"method": "add(a, b)", "input": "两个数字", "output": "和"},
                {"method": "subtract(a, b)", "input": "两个数字", "output": "差"},
                {"method": "multiply(a, b)", "input": "两个数字", "output": "积"},
                {"method": "divide(a, b)", "input": "两个数字", "output": "商（除数为0时报错）"}
            ]
            data_structures = [
                {"name": "OperationResult", "fields": ["success: bool", "value: float", "error: str"]}
            ]
        elif "待办" in project_name:
            modules = [
                {"name": "TodoManager", "responsibility": "待办事项管理核心逻辑"},
                {"name": "Storage", "responsibility": "数据持久化（JSON文件）"},
                {"name": "CLI", "responsibility": "命令行界面交互"}
            ]
            interfaces = [
                {"method": "add_todo(title)", "input": "事项标题", "output": "Todo对象"},
                {"method": "complete_todo(todo_id)", "input": "事项ID", "output": "是否成功"},
                {"method": "list_todos()", "input": "无", "output": "Todo列表"},
                {"method": "delete_todo(todo_id)", "input": "事项ID", "output": "是否成功"}
            ]
            data_structures = [
                {"name": "Todo", "fields": ["id: int", "title: str", "completed: bool", "created_at: str"]}
            ]
        else:
            modules = [
                {"name": "Core", "responsibility": "核心业务逻辑"},
                {"name": "IO", "responsibility": "输入输出处理"}
            ]
            interfaces = [
                {"method": "run()", "input": "用户输入", "output": "处理结果"}
            ]
            data_structures = [
                {"name": "Result", "fields": ["success: bool", "data: any"]}
            ]

        return {
            "project_name": project_name,
            "architecture": "分层架构（UI层 / 业务逻辑层 / 数据层）",
            "modules": modules,
            "interfaces": interfaces,
            "data_structures": data_structures,
            "tech_stack": ["Python 3.8+", "标准库 only"],
            "file_layout": [
                "main.py - 程序入口",
                "core.py - 核心业务逻辑",
                "utils.py - 工具函数"
            ]
        }
