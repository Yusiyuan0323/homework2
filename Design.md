# Design.md - 系统设计文档

## 1. 设计目标

构建一个最小可行的多 Agent 协作 Workflow 框架，验证以下核心概念：
- Agent 编排（Orchestration）
- Agent 间通信（Communication）
- 状态管理（State Management）
- 流程控制（Flow Control）

---

## 2. 整体架构

### 2.1 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    WorkflowEngine                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  Node 1  │───▶│  Node 2  │───▶│  Node 3  │          │
│  │ Requirement│  │ Design   │  │ Coding   │          │
│  │  Agent   │    │  Agent   │    │  Agent   │          │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘          │
│       │               │               │                │
│       └───────────────┼───────────────┘                │
│                       ▼                                │
│              ┌─────────────────┐                       │
│              │  WorkflowState  │  ← 共享状态黑板        │
│              │  (Blackboard)   │                       │
│              └─────────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

### 2.2 分层设计

| 层级 | 组件 | 职责 |
|------|------|------|
| 编排层 | WorkflowEngine | 节点调度、顺序执行、错误处理 |
| 状态层 | WorkflowState | 数据存储、日志记录、状态追踪 |
| Agent层 | RequirementAgent / DesignAgent / CodingAgent | 具体业务逻辑 |
| 抽象层 | BaseAgent | Agent 统一接口定义 |

---

## 3. 核心组件设计

### 3.1 WorkflowState（状态管理）

**设计模式**：黑板模式（Blackboard Pattern）

**数据结构**：

```python
class WorkflowState:
    _data: Dict[str, Any]       # 共享业务数据
    _logs: List[Dict]           # 执行日志
    _current_node: str          # 当前执行节点
    _completed: bool            # 流程完成标志
    _error: str                 # 错误信息
```

**接口**：

| 方法 | 说明 |
|------|------|
| `get(key, default)` | 读取状态数据 |
| `set(key, value)` | 写入状态数据 |
| `update(dict)` | 批量更新 |
| `log(agent, msg, level)` | 记录日志 |
| `save_to_file(path)` | 序列化保存为 JSON |

**设计决策**：
- 所有 Agent 通过同一个 state 对象通信，避免直接调用耦合
- state 同时承担数据传递和日志记录两个职责
- 支持序列化，便于调试和执行追踪

### 3.2 WorkflowEngine（流程引擎）

**核心职责**：
1. 维护节点列表
2. 按顺序执行节点
3. 捕获异常并中断流程
4. 触发步骤回调

**节点结构**：

```python
{
    "name": str,           # 节点名称
    "agent": BaseAgent,    # Agent 实例
    "condition": callable  # 可选执行条件
}
```

**执行流程**：

```
开始
  ↓
for node in nodes:
  ├─ 检查 condition（如有）
  ├─ 设置 current_node
  ├─ 调用 agent.run(state)
  │   ├─ 成功 → 触发 step_callback
  │   └─ 异常 → 记录 error，中断
  ↓
标记 completed
结束
```

**可扩展方向**：
- 条件分支：根据 state 中的值选择下一个节点
- 循环：节点执行失败时重试
- 并行：多个节点同时执行，合并结果
- DAG：有向无环图调度

### 3.3 BaseAgent（Agent 基类）

**设计模式**：模板方法模式

```python
class BaseAgent(ABC):
    name: str

    @abstractmethod
    def run(self, state: WorkflowState) -> None:
        """子类必须实现的核心逻辑"""
        pass

    def log(self, state, message, level):
        """公共日志方法"""
        state.log(self.name, message, level)
```

**设计决策**：
- 所有 Agent 统一接收 state、不返回值（通过 state 传递结果）
- 单一职责：每个 Agent 只做一件事
- 可测试性：Agent 可独立单元测试

---

## 4. Agent 协作流程

### 4.1 Mini SE Pipeline

```
用户输入需求
     │
     ▼
┌─────────────────┐
│ RequirementAgent│  输入: raw_requirement (str)
│                 │  输出: requirement_spec (dict)
└────────┬────────┘         - project_name
         │                  - features[]
         ▼                  - constraints[]
┌─────────────────┐
│  DesignAgent    │  输入: requirement_spec (dict)
│                 │  输出: design_doc (dict)
└────────┬────────┘         - modules[]
         │                  - interfaces[]
         ▼                  - data_structures[]
┌─────────────────┐
│  CodingAgent    │  输入: design_doc (dict)
│                 │  输出: generated_files[] (list[str])
└─────────────────┘         - 写入 output/ 目录
```

### 4.2 数据流

| 阶段 | 写入的 State Key | 数据类型 |
|------|------------------|----------|
| 初始 | `raw_requirement` | str |
| 需求分析后 | `requirement_spec` | dict |
| 系统设计后 | `design_doc` | dict |
| 代码生成后 | `generated_files` | list[str] |
| 代码生成后 | `output_dir` | str |

---

## 5. 扩展设计

### 5.1 如何新增一个 Agent

1. 在 `agents/` 下新建文件，继承 `BaseAgent`
2. 实现 `run(state)` 方法
3. 在 `main.py` 中通过 `engine.add_node()` 添加

```python
# 示例：新增一个测试生成 Agent
class TestAgent(BaseAgent):
    def run(self, state):
        code = state.get("generated_code")
        # ... 生成测试代码 ...
        state.set("test_code", test_code)

# 加入流程
engine.add_node("TestGeneration", TestAgent())
```

### 5.2 如何支持条件分支

```python
# 只有需求中包含"Web"才执行 WebDesignAgent
def needs_web(state):
    return "web" in state.get("requirement_spec", {}).get("description", "").lower()

engine.add_node("WebDesign", WebDesignAgent(), condition=needs_web)
```

---

## 6. 技术选型

| 选择 | 理由 |
|------|------|
| Python 3.8+ | 教学友好，生态丰富，标准库足够实现 MVP |
| 无第三方依赖 | 降低运行门槛，便于评审环境复现 |
| 共享状态模式 | 简单直观，适合 2-3 个 Agent 的小规模协作 |
| 顺序执行引擎 | MVP 阶段足够，后续可扩展为 DAG 调度 |

---

## 7. 已知限制与改进方向

### 当前限制
1. Agent 内部逻辑是规则匹配，未接入 LLM
2. 仅支持顺序执行，无并行/分支/循环
3. 状态存储在内存中，崩溃后丢失
4. 无任务队列和持久化调度

### 改进方向
- 接入 LLM API，让 Agent 具备真正的智能
- 引入有向无环图（DAG）调度，支持并行和条件分支
- 状态持久化到数据库，支持断点续跑
- 添加可视化编排界面（Web UI）
- 支持错误重试和补偿机制
