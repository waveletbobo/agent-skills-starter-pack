# AGENTS.md（Jinja）

A very fast and expressive template engine（pyproject 原文），Pallets 出品，3.2.0.dev，Python >=3.10。

## 0. 不要做什么（最高优先级）
- 不要只跑 `pytest` 就交工：filterwarnings=error（警告即失败），格式与类型在 tox style/typing 里，漏了会卡 CI。
- 不要改 CHANGES.rst 的发版格式：每版条目带 `:pr:`/`:issue:`/`:ghsa:` 编号引用；3.2.0 仍为 Unreleased（见 CHANGES.rst 顶部，Python 3.7/3.8/3.9 支持已去掉、`__version__` 已弃用、改用 `importlib.metadata.version("jinja2")`）。
- 不要把类型检查当可选：mypy 是 strict（`src/` 在检查范围内），`py.typed` 在位，改公共 API 必须同步类型；pyright 为 standard 模式。
- 不要在 src/ 外放包代码：flit 打包 src 布局，ruff `src = ["src"]`；包代码只进 src/jinja2/。
- 不要绕过 pre-commit：ruff、ruff-format、uv-lock、check-merge-conflict、debug-statements、常规钩子都在里面，提交前跑过。
- 不要随便加运行时依赖：唯一运行时依赖是 MarkupSafe>=3.0（pyproject 定死），i18n 可选依赖 Babel>=2.17，新增先问。

## 1. 常用命令
- 测试（全套）：`pytest`（testpaths=tests，filterwarnings=error）
- 全环境：`tox`（py3.10–py3.13、pypy3.11、style、typing、docs；uv 驱动）
- 风格：`tox r -e style`（pre-commit 全钩子）；类型：`tox r -e typing`（mypy strict）
- 钩子：`pre-commit run --all-files`（ruff、ruff-format、uv-lock、常规钩子）
- 文档：`tox r -e docs`（Sphinx，`-E -W -b dirhtml`，docs/*.rst）
- 本地跑：模板渲染走 `jinja2.Environment`，无 CLI 入口（console script 未定义）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先看 tests/ 里对应用例覆盖哪条语义，再改 src/jinja2/，最后跑 `pytest`。
- 开 PR 前先开 ticket（PR 模板原文，文档错别字等简单非代码改动除外）；PR 描述写清改动如何解决所链 ticket。
- 完工证据：`pytest` 全绿＋`tox r -e style`＋`tox r -e typing` 全绿；交工前自查 diff，确认只动了该动的文件。
- 通用贡献流程（环境搭建、PR 流程）不在仓内，见 Pallets 官方贡献指南（PR 模板引用的 CONTRIBUTING.rst 即该指南）。

## 3. 项目指纹
- 技术栈：Python >=3.10；flit_core 打包，src 布局；ruff（B/E/F/I/UP/W，UP038 除外，import 强制单行）；pytest＋coverage（branch=true）；mypy strict＋pyright standard。
- 结构：src/jinja2/（environment.py、compiler.py、parser.py、lexer.py、nodes.py、runtime.py、filters.py、loaders.py、sandbox.py、bccache.py、optimizer.py、idtracking.py、meta.py、nativetypes.py、ext.py、async_utils.py、debug.py、defaults.py、constants.py、exceptions.py、tests.py、utils.py、visitor.py）；tests/（22 项，conftest.py，test_lexnparse/test_compile/test_api/test_runtime/test_security/test_async…）；docs/（Sphinx *.rst，api/sandbox/nativetypes/templates/extensions）；scripts/（generate_identifier_pattern.py）。
- 写法约定：ruff-format；import 单行；类型标注全覆盖（mypy strict）；CHANGES.rst 条目带 :pr:/:issue: 引用；文档改动配 `.. versionchanged::` 条目。
- 测试命名：`test_<主题>.py`，按词法解析/编译/API/运行时/安全/异步/扩展等主题分组。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改模板语法/解析 | src/jinja2/lexer.py、parser.py、nodes.py ＋ tests/test_lexnparse.py、test_nodes.py 补用例 |
| 改代码生成 | src/jinja2/compiler.py、optimizer.py ＋ tests/test_compile.py |
| 改环境/API | src/jinja2/environment.py、defaults.py ＋ tests/test_api.py |
| 改运行时/渲染 | src/jinja2/runtime.py ＋ tests/test_runtime.py |
| 改过滤器/测试函数 | src/jinja2/filters.py、tests.py ＋ tests/test_filters.py、test_tests.py |
| 改沙箱安全 | src/jinja2/sandbox.py ＋ tests/test_security.py |
| 改加载器 | src/jinja2/loaders.py ＋ tests/test_loader.py |
| 改字节码缓存 | src/jinja2/bccache.py ＋ tests/test_bytecode_cache.py |
| 改异步渲染 | src/jinja2/async_utils.py ＋ tests/test_async.py、test_async_filters.py |
| 改文档 | docs/ 对应 *.rst ＋ CHANGES.rst 记条目 |

## 5. 测试
- 行为改动先在 tests/ 加用例：pytest 风格，共享夹具在 tests/conftest.py；用例须在改动前失败、改动后通过（PR 模板原文）。
- 警告即失败：filterwarnings=error，新增代码不得引入 DeprecationWarning。
- 类型改动同步检查：`tox r -e typing`（mypy strict 会卡住未标注的新增公共 API）。
- 安全改动必跑 `tests/test_security.py`；沙箱相关改动另看 CHANGES.rst 的 :ghsa: 安全条目写法。

## 6. 边界
- ✅ 总是：改完跑 `pytest`＋style＋typing；CHANGES.rst 记条目；PR 先开 ticket
- ⚠️ 先问：新增公共导出、改公共 API 语义、提高 Python 最低版本、新增运行时依赖、改 lexer/parser/nodes 分层
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- CONTRIBUTING.rst 不在仓内（PR 模板引用它，docs/ 无此文件）：以 Pallets 官方贡献指南为准，本稿不臆断其具体步骤。
