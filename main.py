#!/usr/bin/env python3
"""
Homework 2: Simple Workflow MVP
Mini SE 流程：需求Agent -> 设计Agent -> 编码Agent

运行方式:
    python main.py
    python main.py --requirement "做一个待办事项管理器"
"""

import sys
import argparse
from workflow import WorkflowState, WorkflowEngine
from agents import RequirementAgent, DesignAgent, CodingAgent


def print_step(node_name: str, state: WorkflowState):
    """每步执行完后的回调：打印进度"""
    print(f"\n  ✓ 节点 [{node_name}] 执行完成")
    print(f"    当前状态键: {list(state.data.keys())}")


def main():
    parser = argparse.ArgumentParser(description="Simple Workflow MVP - Mini SE 流程")
    parser.add_argument(
        "--requirement", "-r",
        type=str,
        default="做一个命令行计算器，支持加减乘除",
        help="用户原始需求描述"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output",
        help="代码生成输出目录"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Simple Workflow MVP - Mini SE Pipeline")
    print("  Requirement -> Design -> Coding")
    print("=" * 60)
    print(f"\n  用户需求: {args.requirement}")
    print(f"  输出目录: {args.output}")

    # 1. 初始化状态
    initial_state = WorkflowState({
        "raw_requirement": args.requirement
    })

    # 2. 组装 Workflow
    engine = WorkflowEngine(name="MiniSE-Pipeline")
    engine \
        .add_node("RequirementAnalysis", RequirementAgent()) \
        .add_node("SystemDesign", DesignAgent()) \
        .add_node("CodeGeneration", CodingAgent(output_dir=args.output)) \
        .set_step_callback(print_step)

    # 打印流程描述
    print(f"\n  {engine.describe()}")
    print("\n" + "-" * 60)
    print("  开始执行 Workflow...")
    print("-" * 60)

    # 3. 执行
    final_state = engine.run(initial_state)

    # 4. 输出结果
    print("\n" + "=" * 60)
    print("  Workflow 执行结果")
    print("=" * 60)

    if final_state.error:
        print(f"\n  ✗ 执行失败: {final_state.error}")
        sys.exit(1)

    print(f"\n  ✓ 状态: {'完成' if final_state.is_completed else '未完成'}")

    # 打印需求规格
    spec = final_state.get("requirement_spec")
    if spec:
        print(f"\n  [需求规格]")
        print(f"    项目: {spec['project_name']}")
        print(f"    功能点: {len(spec['features'])} 个")
        for f in spec["features"]:
            print(f"      - {f}")

    # 打印设计文档
    design = final_state.get("design_doc")
    if design:
        print(f"\n  [设计文档]")
        print(f"    架构: {design['architecture']}")
        print(f"    模块: {len(design['modules'])} 个")
        for m in design["modules"]:
            print(f"      - {m['name']}: {m['responsibility']}")

    # 打印生成的文件
    files = final_state.get("generated_files", [])
    if files:
        print(f"\n  [生成文件]")
        for f in files:
            print(f"    - {f}")

    # 保存完整状态
    state_file = "output/workflow_state.json"
    final_state.save_to_file(state_file)
    print(f"\n  完整状态已保存到: {state_file}")

    # 打印执行日志摘要
    logs = final_state.logs
    print(f"\n  [执行日志] 共 {len(logs)} 条")
    for log in logs:
        level_tag = "⚠" if log["level"] == "ERROR" else " "
        print(f"    {level_tag} [{log['agent']}] {log['message']}")

    print("\n" + "=" * 60)
    print("  完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
