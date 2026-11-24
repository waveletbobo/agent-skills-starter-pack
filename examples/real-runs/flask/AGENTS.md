# AGENTS.md（Flask）

A simple framework for building complex web applications（pyproject 原文），Pallets 出品，3.2.0.dev，Python >=3.11。

## 0. 不要做什么（最高优先级）
- 不要只跑 `pytest` 就交工：filterwarnings=error（警告即失败），格式与类型在 tox style/typing 里，漏了会卡 CI。
- 不要改 CHANGES.rst 的发版格式：每版条目带 `:pr:`/`:issue:` 编号引用；3.2.0 仍为 Unreleased（见 CHANGES.rst 顶部，Python 3.9/3.10 支持已去掉、RequestContext 已并入 AppContext）。
- 不要把类型检查当可选：mypy 是 strict（`src/` 与 `tests/type_check/` 都在检查范围内），`py.typed` 在位，改公共 API 必须同步类型。
- 不要在 src/ 外放包代码：flit 打包 src 布局，ruff `src = ["src"]`；包代码只进 src/flask/。
- 不要绕过 pre-commit：ruff-check、ruff-format、uv-lock、codespell 都在钩子里，提交前跑过。
- 不要随便加运行时依赖：六个运行时依赖（blinker/click/itsdangerous/jinja2/markupsafe/werkzeug）是 pyproject 定死的集合，新增先问。

## 1. 常用命令
- 测试（全套）：`pytest`（testpaths=tests，filterwarnings=error）
- 全环境：`tox`（py3.11–py3.15、pypy3.11、tests-min、tests-dev、style、typing、docs；uv 驱动）
- 最低依赖版测试：`tox r -e tests-min`；风格：`tox r -e style`；类型：`tox r -e typing`（mypy strict）
- 钩子：`pre-commit run --all-files`（ruff-check、ruff-format、uv-lock、codespell、常规钩子）
- 文档：`tox r -e docs`（Sphinx，docs/*.rst）
- 本地跑：`flask run`（console script：flask.cli:main）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先看 tests/ 里对应用例覆盖哪条语义，再改 src/flask/，最后跑 `pytest`。
- 完工证据：`pytest` 全绿＋`tox r -e style`＋`tox r -e typing` 全绿；交工前自查 diff，确认只动了该动的文件。
- 通用贡献流程（环境搭建、PR 流程）不在仓内，见 Pallets 官方贡献指南（docs/contributing.rst 顶部链接）。

## 3. 项目指纹
- 技术栈：Python >=3.11；flit_core 打包，src 布局；ruff（B/E/F/I/UP/W，import 强制单行）；pytest＋coverage（branch=true）；mypy strict。
- 结构：src/flask/（app.py、blueprints.py、cli.py、config.py、ctx.py、globals.py、helpers.py、sessions.py、signals.py、templating.py、testing.py、views.py、wrappers.py、json/、sansio/）；tests/（27 项，conftest.py，test_appctx/test_basic/test_blueprints/test_cli/test_config…）；docs/（Sphinx *.rst，含 contributing.rst）；examples/（flit sdist 收录）。
- 写法约定：ruff-format；import 单行；类型标注全覆盖（mypy strict）；CHANGES.rst 条目带 :pr:/:issue: 引用。
- 测试命名：`test_<主题>.py`，按应用上下文/蓝图/CLI/配置/请求上下文等主题分组。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改应用创建/请求分发 | src/flask/app.py ＋ tests/test_basic.py、test_reqctx.py 补用例 |
| 改蓝图 | src/flask/blueprints.py ＋ tests/test_blueprints.py |
| 改 CLI | src/flask/cli.py ＋ tests/test_cli.py |
| 改配置加载 | src/flask/config.py ＋ tests/test_config.py、test_instance_config.py |
| 改上下文/全局代理 | src/flask/ctx.py、globals.py ＋ tests/test_appctx.py |
| 改会话 | src/flask/sessions.py ＋ tests/test_session_interface.py |
| 改模板渲染 | src/flask/templating.py ＋ tests/test_templating.py |
| 改测试客户端 | src/flask/testing.py ＋ tests/test_testing.py |
| 改文档 | docs/ 对应 *.rst ＋ CHANGES.rst 记条目 |

## 5. 测试
- 行为改动先在 tests/ 加用例：pytest 风格，共享夹具在 tests/conftest.py。
- 警告即失败：filterwarnings=error，新增代码不得引入 DeprecationWarning。
- 类型改动同步检查：`tox r -e typing`（mypy strict 会卡住未标注的新增公共 API）。
- 最低依赖版：改依赖下限时跑 `tox r -e tests-min` 验证。

## 6. 边界
- ✅ 总是：改完跑 `pytest`＋style＋typing；CHANGES.rst 记条目
- ⚠️ 先问：新增公共导出、改公共 API 语义、提高 Python 最低版本、新增运行时依赖、改 src/flask/ 分层
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- PR 是否必须先开 issue、CHANGES.rst 条目由谁写：仓内 contributing.rst 只链向 Pallets 官方指南，未写明，以官方指南为准，本稿不臆断。
- 3.2.0 的 RequestContext 合并与 Flask 方法签名改动（CHANGES.rst 顶部）：改请求分发相关代码时须按新签名（AppContext 为第一参数），旧签名仅在弃用期内兼容。
