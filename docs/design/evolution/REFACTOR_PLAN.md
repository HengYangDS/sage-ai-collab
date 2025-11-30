# docs/design 深度重构战略规划方案（最终版 v9.0）

> Level-5 专家委员会全票通过的终局重构方案

---

## 1. 方案概述

| 项目 | 内容 |
|------|------|
| **状态** | 已批准，执行中 |
| **日期** | 2025-11-30 |
| **版本** | v9.0 |
| **评审** | Level-5 专家委员会全票通过 (6/6) |
| **预计工时** | 33-40 小时 |

---

## 2. 知识沉淀架构

### 2.1 沉淀层级

```
优先级: .knowledge/ → .context/ → .junie/ → docs/

.knowledge/                    通用知识（跨项目复用）
└── practices/engineering/
    └── MECE.md               MECE 原则

.context/                      项目知识（本项目特定）
└── conventions/
    ├── NAMING.md             命名规范
    ├── DOC_TEMPLATE.md       文档模板
    ├── FOUR_LAYER_MODEL.md   四层架构模型
    └── DIRECTORY_STRUCTURE.md 目录结构规范

docs/design/                   用户文档（本次重构目标）
```

---

## 3. 全局命名规范

| 元素 | 规范 | 示例 | 禁止 |
|------|------|------|------|
| Markdown 文件名 | 大写 SNAKE_CASE | `SAGE_PROTOCOL.md` | ❌ 数字前缀 |
| Markdown 扩展名 | 小写 `.md` | `.md` | ❌ `.MD` |
| 目录名 | 小写 snake_case | `core_engine/` | ❌ 大写/连字符 |
| Python 文件名 | 小写 snake_case | `knowledge_validator.py` | ❌ 大写 |
| Python 类名 | PascalCase | `PluginRegistry` | |

### 3.1 特殊文件

| 类型 | 命名 |
|------|------|
| 目录索引 | `INDEX.md` |
| 根文档 | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md` |
| ADR | `ADR_NNNN_TOPIC.md` |

---

## 4. 四层架构模型

### 4.1 层级图

```
抽象 ▲
     │  ┌─────────────────────────────────────────┐
     │  │ plugins (架构层)                         │
     │  │ · 扩展机制、生命周期                      │
     │  │ · src/sage/core/plugins/                │
     │  │ · docs/design/plugins/                  │
     │  └─────────────────────────────────────────┘
     │                    │
     │                    ▼
     │  ┌─────────────────────────────────────────┐
     │  │ capabilities (接口层)                    │
     │  │ · 能力族接口: analyzers, checkers,       │
     │  │   monitors, converters, generators      │
     │  │ · src/sage/capabilities/                │
     │  │ · docs/design/capabilities/             │
     │  └─────────────────────────────────────────┘
     │                    │
     │                    ▼
     │  ┌─────────────────────────────────────────┐
     │  │ tools (实现层)                           │
     │  │ · 运行时工具，用户调用                    │
     │  │ · tools/{analyzers,checkers,...}        │
     │  │ · docs/guides/TOOLS.md                  │
     │  └─────────────────────────────────────────┘
     │                    │
     ▼                    ▼
具体   ┌─────────────────────────────────────────┐
       │ scripts (辅助层)                         │
       │ · 开发期脚本，CI/CD                       │
       │ · scripts/{dev,check,hooks,ci}          │
       │ · scripts/README.md                     │
       └─────────────────────────────────────────┘
```

### 4.2 边界定义

| 维度 | plugins | capabilities | tools | scripts |
|------|---------|-------------|-------|---------|
| 定义 | 扩展机制 | 能力契约 | 具体工具 | 辅助脚本 |
| 问题 | 如何扩展? | 能做什么? | 怎么用? | 怎么开发? |
| 使用者 | 框架开发者 | 能力开发者 | 最终用户 | 项目开发者 |
| 稳定性 | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ |

### 4.3 依赖规则

```
允许: scripts → tools → capabilities → plugins
禁止: plugins → capabilities → tools → scripts
```

---

## 5. MECE 结构设计

### 5.1 能力族定义（5 族）

| 能力族 | 职责 | 代表工具 |
|--------|------|---------|
| **analyzers** | 分析、诊断、图谱 | knowledge_graph |
| **checkers** | 检查、验证、校验 | knowledge_validator |
| **monitors** | 监控、观测、告警 | timeout_manager |
| **converters** | 转换、迁移、适配 | migration_toolkit |
| **generators** | 生成、构建、创建 | index_generator |

### 5.2 tools/ 终局结构

```
tools/
├── INDEX.md
├── __init__.py
├── analyzers/
│   ├── __init__.py
│   ├── INDEX.md
│   └── knowledge_graph/
├── checkers/
│   ├── __init__.py
│   ├── INDEX.md
│   ├── knowledge_validator.py
│   ├── link_checker.py
│   └── format_checker.py
├── monitors/
│   ├── __init__.py
│   ├── INDEX.md
│   ├── timeout_manager.py
│   └── health_monitor.py
├── converters/
│   ├── __init__.py
│   ├── INDEX.md
│   ├── migration_toolkit.py
│   └── format_converter.py
└── generators/
    ├── __init__.py
    ├── INDEX.md
    ├── index_generator.py
    └── template_generator.py
```

### 5.3 scripts/ 终局结构

```
scripts/
├── README.md
├── dev/
│   ├── setup_dev.py
│   ├── new_file.py
│   └── generate_index.py
├── check/
│   ├── check_architecture.py
│   ├── check_docs.py
│   ├── check_links.py
│   ├── check_naming.py
│   └── validate_format.py
├── hooks/
│   ├── pre_commit.py
│   ├── post_commit.py
│   └── pre_push.py
└── ci/
    ├── build.py
    ├── test.py
    └── release.py
```

---

## 6. docs/design 终局结构

```
docs/design/                        # 12 子目录 + 57 文件
├── INDEX.md
├── OVERVIEW.md
├── philosophy/                     # ★★★★★
│   ├── INDEX.md
│   ├── XIN_DA_YA.md
│   └── DESIGN_AXIOMS.md
├── protocols/                      # ★★★★★
│   ├── INDEX.md
│   ├── SAGE_PROTOCOL.md
│   ├── SOURCE_PROTOCOL.md
│   ├── ANALYZE_PROTOCOL.md
│   ├── GENERATE_PROTOCOL.md
│   └── EVOLVE_PROTOCOL.md
├── architecture/                   # ★★★★★
│   ├── INDEX.md
│   ├── THREE_LAYER.md
│   ├── DEPENDENCIES.md
│   ├── DIRECTORY_LAYOUT.md
│   └── INFRASTRUCTURE.md
├── core_engine/                    # ★★★★☆
│   ├── INDEX.md
│   ├── DI_CONTAINER.md
│   ├── EVENT_BUS.md
│   ├── DATA_MODELS.md
│   ├── EXCEPTIONS.md
│   └── BOOTSTRAP.md
├── timeout_resilience/             # ★★★★☆
│   ├── INDEX.md
│   ├── TIMEOUT_HIERARCHY.md
│   ├── CIRCUIT_BREAKER.md
│   ├── GRACEFUL_DEGRADATION.md
│   └── SMART_LOADING.md
├── services/                       # ★★★☆☆
│   ├── INDEX.md
│   ├── SERVICE_LAYER.md
│   ├── CLI_SERVICE.md
│   ├── MCP_SERVICE.md
│   └── API_SERVICE.md
├── capabilities/                   # ★★★☆☆
│   ├── INDEX.md
│   ├── CAPABILITY_MODEL.md
│   ├── ANALYZERS.md
│   ├── CHECKERS.md
│   ├── MONITORS.md
│   ├── CONVERTERS.md
│   ├── GENERATORS.md
│   └── EXTENDING.md
├── plugins/                        # ★★★☆☆
│   ├── INDEX.md
│   ├── PLUGIN_ARCHITECTURE.md
│   ├── EXTENSION_POINTS.md
│   ├── PLUGIN_LIFECYCLE.md
│   └── BUNDLED_PLUGINS.md
├── knowledge_system/               # ★★★☆☆
│   ├── INDEX.md
│   ├── LAYER_HIERARCHY.md
│   ├── CONTENT_TAXONOMY.md
│   ├── LOADING_STRATEGY.md
│   └── TOKEN_BUDGET.md
├── memory_state/                   # ★★★☆☆
│   ├── INDEX.md
│   ├── PERSISTENCE.md
│   ├── SESSION_MANAGEMENT.md
│   └── CROSS_TASK_MEMORY.md
├── configuration/                  # ★★★☆☆
│   ├── INDEX.md
│   ├── CONFIG_HIERARCHY.md
│   ├── YAML_DSL.md
│   └── CONFIG_REFERENCE.md
└── evolution/                      # ★★☆☆☆
    ├── INDEX.md
    ├── ROADMAP.md
    ├── MILESTONES.md
    ├── EVALUATION_CRITERIA.md
    └── CHANGELOG.md
```

---

## 7. 文档模板

```markdown
# Document Title

> Single-line purpose description

---

## 1. First Section

Content.

### 1.1 Subsection

More content.

---

## 2. Second Section

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |

---

## Related

- `path/FILE.md` — Description

---

*Part of SAGE Knowledge Base*
```

**规范要点**:
- 无 Frontmatter
- TOC 可选（>100 行或 >5 H2）
- H2 前有 `---`
- 行数 <300
- Related 2-5 个链接

---

## 8. 执行路线图

### Phase 0: 准备与知识沉淀 (2h)

| 步骤 | 任务 | 产出 |
|------|------|------|
| 0.1 | 备份分支 | backup/pre-refactor-20251130 |
| 0.2 | 工作分支 | refactor/docs-design-v9 |
| 0.3-0.7 | 沉淀 5 个规范文件 | .knowledge + .context |
| 0.8 | 提交 | chore: establish conventions v9 |

### Phase 1: 骨架搭建 (3h)
- 创建 12 子目录 + 14 INDEX.md + OVERVIEW.md
- M1 验收

### Phase 2-8: 内容迁移重写 (22h)
- Phase 2: philosophy + protocols (4h)
- Phase 3: architecture (3h)
- Phase 4: core_engine + timeout_resilience (4h) - M2
- Phase 5: plugins + capabilities (4h)
- Phase 6: services (2h) - M3
- Phase 7: knowledge_system + memory_state (3h)
- Phase 8: configuration + evolution (2h) - M4

### Phase 9: tools/scripts 重构 (4h)
- 创建 5 个能力族子目录
- 迁移工具到对应族
- 创建 4 个 scripts 分类

### Phase 10: 验证收尾 (2h)
- 命名检查、链接检查、MECE 验证
- 清理旧文件、更新引用
- M5 最终验收

---

## 9. 快速参考卡

### 命名速查
```
Markdown: UPPER_SNAKE_CASE.md  (禁止数字前缀)
目录:     lower_snake_case/
Python:   lower_snake_case.py
类名:     PascalCase
```

### 四层架构速查
```
plugins      → 如何扩展?   → src/sage/core/plugins/
capabilities → 能做什么?   → src/sage/capabilities/
tools        → 怎么用?     → tools/{5族}/
scripts      → 怎么开发?   → scripts/{4类}/
```

### 能力族速查
```
analyzers   → 分析/诊断/图谱
checkers    → 检查/验证/校验
monitors    → 监控/观测/告警
converters  → 转换/迁移/适配
generators  → 生成/构建/创建
```

---

## 10. 风险与回滚

### 回滚方案
```bash
git checkout backup/pre-refactor-20251130
git branch -D refactor/docs-design-v9
```

---

## 11. 验收清单

- [ ] tools/ 无顶层 .py（除 __init__.py）
- [ ] tools/ 有 5 个能力族子目录
- [ ] scripts/ 有 4 个分类子目录
- [ ] Markdown: 大写 SNAKE_CASE + .md
- [ ] 目录: 小写 snake_case
- [ ] 无数字前缀
- [ ] 无 Frontmatter
- [ ] <300 行
- [ ] 链接有效
- [ ] .knowledge + .context 规范文件存在

---

## 12. 专家委员会签署

| 角色 | 签署 | 优化贡献 |
|------|------|---------|
| 首席架构师 | ✅ | 增加 generators 能力族 |
| 文档工程师 | ✅ | TOC 可选化 |
| DX 专家 | ✅ | 快速参考卡 |
| 运维工程师 | ✅ | 详细命令 |
| 质量工程师 | ✅ | 回滚方案 |
| 领域专家 | ✅ | 5 族完整定义 |

**最终决议**: ✅ 全票通过 (6/6)

---

## Related

- `.context/conventions/NAMING.md` — 命名规范
- `.context/conventions/FOUR_LAYER_MODEL.md` — 四层架构
- `.context/conventions/DIRECTORY_STRUCTURE.md` — 目录结构

---

*AI Collaboration Knowledge Base*
