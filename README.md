# Homework 2: Simple Workflow MVP

## 项目简介

本项目实现了一个 **Mini SE（软件工程）流程** 的多 Agent 协作 Workflow，包含三个 Agent 节点：

```
需求Agent → 设计Agent → 编码Agent
```

用户输入一段自然语言需求，Workflow 自动完成需求分析、系统设计、代码生成三个阶段，最终输出可运行的 Python 项目代码。

---

## 快速开始

### 环境要求

- Python 3.8+
- 无第三方依赖（仅使用标准库）

### 运行方式

```bash
# 使用默认需求（命令行计算器）
python main.py

# 指定自定义需求
python main.py --requirement "做一个待办事项管理器"

# 指定输出目录
python main.py -r "做一个待办事项管理器" -o my_output
```

### 运行示例

```
============================================================
  Simple Workflow MVP - Mini SE Pipeline
  Requirement -> Design -> Coding
============================================================

  用户需求: 做一个命令行计算器，支持加减乘除
  输出目录: output

  Workflow: MiniSE-Pipeline (3 nodes)
  1. RequirementAnalysis
  2. SystemDesign
  3. CodeGeneration

  ------------------------------------------------------------
  开始执行 Workflow...
  ------------------------------------------------------------

  ✓ 节点 [RequirementAnalysis] 执行完成
    当前状态键: ['raw_requirement', 'requirement_spec']

  ✓ 节点 [SystemDesign] 执行完成
    当前状态键: ['raw_requirement', 'requirement_spec', 'design_doc']

  ✓ 节点 [CodeGeneration] 执行完成
    当前状态键: ['raw_requirement', 'requirement_spec', 'design_doc', 'generated_files', 'output_dir']
  ...
```

---

## 项目结构

```
homework2/
├── main.py                  # 程序入口，组装并运行 Workflow
├── requirements.txt         # 依赖说明（无第三方依赖）
├── README.md                # 本文件
├── Design.md                # 设计文档
├── workflow/                # Workflow 核心框架
│   ├── __init__.py
│   ├── state.py             # 状态管理（Agent 间通信）
│   └── engine.py            # Workflow 引擎（流程编排）
├── agents/                  # 具体 Agent 实现
│   ├── __init__.py
│   ├── base_agent.py        # Agent 抽象基类
│   ├── requirement_agent.py # 需求分析 Agent
│   ├── design_agent.py      # 系统设计 Agent
│   └── coding_agent.py      # 编码生成 Agent
└── output/                  # 运行时生成的代码和状态文件
    ├── calculator.py        # 生成的计算器代码
    ├── todo_app.py          # 生成的待办应用代码
    └── workflow_state.json  # 完整执行状态快照
```

---

## 核心概念

### 1. Agent 间通信：共享状态模式

所有 Agent 共享同一个 `WorkflowState` 对象：
- **读**：Agent 从 state 中获取上游节点的输出
- **写**：Agent 将自己的结果写入 state，供下游节点读取

这是一种 **黑板模式（Blackboard Pattern）** 的简化实现，解耦了 Agent 之间的直接依赖。

### 2. Workflow 引擎

`WorkflowEngine` 负责：
- 按顺序执行节点
- 节点间状态传递
- 错误捕获与中断
- 执行日志记录
- 可扩展的回调机制

### 3. 可扩展性

新增 Agent 只需两步：
1. 继承 `BaseAgent`，实现 `run(state)` 方法
2. 通过 `engine.add_node()` 加入流程

---

## 支持的需求类型

| 关键词 | 生成项目 |
|--------|----------|
| 计算器 / calculator | 命令行四则运算计算器 |
| 待办 / todo | 待办事项管理器（JSON 持久化） |
| 其他 | 通用模板代码 |

---

## 评审标准对应

| 维度 | 实现说明 |
|------|----------|
| 流程完整性 (40%) | 端到端跑通：需求输入 → 设计 → 代码生成 → 输出文件 |
| Agent 协作 (30%) | 共享状态对象实现 Agent 间数据传递，每个 Agent 职责单一 |
| 可扩展性 (20%) | Agent 基类 + 引擎 add_node 接口，新增 Agent/节点零修改核心框架 |
| 文档 (10%) | README.md + Design.md，含架构图、流程图、使用说明 |

---

## License

This is a homework assignment.
