"""
编码生成 Agent
接收设计文档，生成可运行的 Python 源代码文件
"""

import os
from .base_agent import BaseAgent
from workflow.state import WorkflowState


class CodingAgent(BaseAgent):
    """
    编码生成 Agent
    输入：state.get("design_doc") - 技术设计文档
    输出：state.set("generated_files", [...]) - 生成的文件列表
          实际写入文件到 output/ 目录
    """

    def __init__(self, output_dir: str = "output"):
        super().__init__("CodingAgent")
        self.output_dir = output_dir

    def run(self, state: WorkflowState) -> None:
        design = state.get("design_doc")
        if not design:
            raise ValueError("design_doc not found in state")

        self.log(state, f"Generating code for: {design['project_name']}")

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

        # 根据项目类型生成代码
        project_name = design["project_name"]
        files = self._generate_code(project_name, design)

        # 写入文件
        written_files = []
        for filename, content in files.items():
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            written_files.append(filepath)
            self.log(state, f"Generated: {filepath}")

        state.set("generated_files", written_files)
        state.set("output_dir", os.path.abspath(self.output_dir))
        self.log(state, f"Total {len(written_files)} files generated")

    def _generate_code(self, project_name: str, design: dict) -> dict:
        """根据项目类型生成对应的代码文件"""
        if "计算器" in project_name:
            return self._generate_calculator()
        elif "待办" in project_name:
            return self._generate_todo()
        else:
            return self._generate_generic(design)

    def _generate_calculator(self) -> dict:
        """生成计算器项目代码"""
        main_py = '''#!/usr/bin/env python3
"""
命令行计算器 - 由 Workflow 自动生成
"""


class Calculator:
    """核心计算逻辑"""

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


def main():
    print("=" * 30)
    print("      命令行计算器")
    print("=" * 30)
    print("支持操作: +  -  *  /")
    print("输入 q 退出")
    print("-" * 30)

    calc = Calculator()

    while True:
        try:
            expr = input("请输入表达式 (如 1+2): ").strip()
            if expr.lower() == "q":
                print("再见!")
                break

            # 简单解析
            op = None
            for o in ["+", "-", "*", "/"]:
                if o in expr:
                    op = o
                    break

            if not op:
                print("错误: 无法识别操作符")
                continue

            a_str, b_str = expr.split(op, 1)
            a = float(a_str.strip())
            b = float(b_str.strip())

            if op == "+":
                result = calc.add(a, b)
            elif op == "-":
                result = calc.subtract(a, b)
            elif op == "*":
                result = calc.multiply(a, b)
            elif op == "/":
                result = calc.divide(a, b)

            print(f"结果: {result}")
            print("-" * 30)

        except ValueError as e:
            print(f"错误: {e}")
            print("-" * 30)
        except KeyboardInterrupt:
            print("\\n再见!")
            break


if __name__ == "__main__":
    main()
'''
        return {"calculator.py": main_py}

    def _generate_todo(self) -> dict:
        """生成待办事项管理器代码"""
        main_py = '''#!/usr/bin/env python3
"""
待办事项管理器 - 由 Workflow 自动生成
"""

import json
import os
from datetime import datetime


class Todo:
    """待办事项数据结构"""

    def __init__(self, todo_id: int, title: str):
        self.id = todo_id
        self.title = title
        self.completed = False
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        todo = cls(data["id"], data["title"])
        todo.completed = data.get("completed", False)
        todo.created_at = data.get("created_at", "")
        return todo


class TodoManager:
    """待办事项管理核心逻辑"""

    def __init__(self, filepath: str = "todos.json"):
        self.filepath = filepath
        self.todos: list[Todo] = []
        self._load()

    def add_todo(self, title: str) -> Todo:
        todo_id = max((t.id for t in self.todos), default=0) + 1
        todo = Todo(todo_id, title)
        self.todos.append(todo)
        self._save()
        return todo

    def complete_todo(self, todo_id: int) -> bool:
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = True
                self._save()
                return True
        return False

    def list_todos(self) -> list[Todo]:
        return self.todos

    def delete_todo(self, todo_id: int) -> bool:
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                self._save()
                return True
        return False

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.todos], f, ensure_ascii=False, indent=2)

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.todos = [Todo.from_dict(d) for d in data]


def main():
    manager = TodoManager()

    while True:
        print("\\n" + "=" * 30)
        print("      待办事项管理器")
        print("=" * 30)
        print("1. 查看所有待办")
        print("2. 添加待办")
        print("3. 完成待办")
        print("4. 删除待办")
        print("5. 退出")
        print("-" * 30)

        choice = input("请选择操作 (1-5): ").strip()

        if choice == "1":
            todos = manager.list_todos()
            if not todos:
                print("暂无待办事项")
            for t in todos:
                status = "✓" if t.completed else " "
                print(f"  [{status}] #{t.id} {t.title}")

        elif choice == "2":
            title = input("请输入待办内容: ").strip()
            if title:
                todo = manager.add_todo(title)
                print(f"已添加: #{todo.id} {todo.title}")

        elif choice == "3":
            todo_id = input("请输入完成的待办ID: ").strip()
            try:
                if manager.complete_todo(int(todo_id)):
                    print("已标记完成")
                else:
                    print("未找到该待办")
            except ValueError:
                print("请输入数字ID")

        elif choice == "4":
            todo_id = input("请输入要删除的待办ID: ").strip()
            try:
                if manager.delete_todo(int(todo_id)):
                    print("已删除")
                else:
                    print("未找到该待办")
            except ValueError:
                print("请输入数字ID")

        elif choice == "5":
            print("再见!")
            break

        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()
'''
        return {"todo_app.py": main_py}

    def _generate_generic(self, design: dict) -> dict:
        """生成通用模板代码"""
        project_name = design["project_name"]
        main_py = f'''#!/usr/bin/env python3
"""
{project_name} - 由 Workflow 自动生成
"""


def main():
    print("欢迎使用 {project_name}")
    # TODO: 实现核心功能


if __name__ == "__main__":
    main()
'''
        return {"main.py": main_py}
