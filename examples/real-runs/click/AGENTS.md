# AGENTS.md（click）

Python 可组合命令行工具包（pyproject 原文："Composable command line interface toolkit"），Pallets 出品，8.6.0.dev，零运行时依赖（标准库以外无依赖）。

## 0. 不要做什么（最高优先级）
- 不要给包加运行时依赖：pyproject 没有 dependencies 字段；能用标准库实现的功能不许拉外部包（docs/contributing.md 原文）。
- 不要用三元表达式：coverage 测不到两个分支，改写成显式 `if`/`else` 块（docs/contributing.md 原文）。
- 不要只跑 `pytest` 就交工：它默认排除 stress 测试（addopts `-m 'not stress'`），格式与 lint 在 pre-commit/tox style 里，漏了会卡 CI。
- 不要改 CHANGES.md 的发版格式：每版条目带 `{pr}` 编号引用；8.6.0 仍为 Unreleased，正在去掉 Python 3.10 支持、并为 Click 9.0 做多处弃用（见 CHANGES.md 顶部）。
- 不要把类型检查当可选：mypy 是 strict，pyright 是 basic，`src/` 与 `tests/typing/` 都在检查范围内；`py.typed` 在位，改公共 API 必须同步类型。
- 不要在 Markdown 里写超长行：文档行宽 80 字符（docs/contributing.md 原文）。

## 1. 常用命令
- 测试（全套，默认不含 stress）：`pytest`（filterwarnings=error，警告即失败）
- 压力测试：`tox r -e stress`（竞态专项）；随机并行测污染：`tox r -e random`
- 全环境：`tox`（py3.11–py3.15、pypy3.11、style、typing、docs；uv 驱动）
- 风格：`tox r -e style`；类型：`tox r -e typing`（mypy strict＋pyright basic）
- 钩子：`pre-commit run --all-files`（ruff-check、ruff-format、uv-lock、codespell、常规钩子）
- 文档：`tox r -e docs`（Sphinx＋MyST，docs/*.md）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先看 tests/ 里对应用例覆盖哪条语义，再改 src/click/，最后跑 `pytest`。
- 完工证据：`pytest` 全绿＋`tox r -e style`＋`tox r -e typing` 全绿；交工前自查 diff，确认只动了该动的文件。
- 通用贡献流程（环境搭建、PR 流程）不在仓内，见 Pallets 官方贡献指南（docs/contributing.md 顶部链接）。

## 3. 项目指纹
- 技术栈：Python >=3.11（3.10 已在 8.6.0 去掉）；flit_core 打包，src 布局；ruff（B/E/F/I/UP/W/ICN，import 强制单行、typing 别名 `t`）；pytest＋coverage（branch=true）。
- 结构：src/click/（17 个 .py，core.py 4018 行、testing.py 840 行、decorators.py 621 行、parser.py、types.py、termui.py、shell_completion.py、formatting.py、exceptions.py）；tests/（22 个顶层 .py＋test_exceptions/test_types/test_utils/typing 子目录，conftest.py）；examples/（可运行示例，ruff 排除）；docs/（Sphinx＋MyST 的 *.md，含 contributing.md）。
- 写法约定：ruff-format；import 单行；`typing` 一律别名 `t`；Markdown 80 列；避免三元表达式。
- 测试命名：`test_<主题>.py`，按命令/参数/选项/解析等主题分组（如 test_commands.py、test_options.py、test_parser.py、test_shell_completion.py）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改命令/组执行逻辑 | src/click/core.py ＋ tests/test_commands.py、test_chain.py 补用例 |
| 改装饰器 API | src/click/decorators.py ＋ tests/test_command_decorators.py |
| 改参数解析 | src/click/parser.py ＋ tests/test_parser.py、test_arguments.py、test_options.py |
| 改帮助/格式化输出 | src/click/formatting.py ＋ tests/test_formatting.py |
| 改错误类型/退出行为 | src/click/exceptions.py ＋ tests/test_exceptions/ |
| 改类型系统 | src/click/types.py ＋ tests/test_types/ |
| 改测试工具 CliRunner | src/click/testing.py ＋ tests/test_testing.py |
| 改文档 | docs/ 对应 *.md（80 列）＋ CHANGES.md 记条目 |

## 5. 测试
- 行为改动先在 tests/ 加用例：pytest 风格，共享夹具在 tests/conftest.py。
- 警告即失败：filterwarnings=error，新增代码不得引入 DeprecationWarning。
- stress 测试默认不跑：改测试运行器（testing.py）或涉及竞态时，单独跑 `tox r -e stress`。
- 类型改动同步检查：`tox r -e typing`（mypy strict 会卡住未标注的新增公共 API）。

## 6. 边界
- ✅ 总是：改完跑 `pytest`＋style＋typing；保持零运行时依赖
- ⚠️ 先问：新增公共导出、改公共 API 语义、提高 Python 最低版本、改 src/click/ 分层
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- PR 是否必须先开 issue、CHANGES.md 条目由谁写：仓内 contributing.md 未写明，以 Pallets 官方贡献指南为准，本稿不臆断。
- nightly 工作流跑 Flask 下游套件：改动是否影响下游需跑 Flask 套件验证，仓内无成文触发条件，改核心解析/执行逻辑时建议人工确认。
