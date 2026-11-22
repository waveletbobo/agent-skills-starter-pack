# AGENTS.md（django）

高层 Python Web 框架（pyproject.toml 原文：\"A high-level Python web framework that encourages rapid development and clean, pragmatic design\"），BSD-3-Clause，Python ≥3.12，setuptools 打包；依赖仅 asgiref ≥3.13、sqlparse ≥0.5.0，tzdata 仅 Windows。版本号取自 django.__version__（setuptools dynamic）。

## 0. 不要做什么（最高优先级）
- 不要不带 Trac 票号就开非琐碎 PR：CONTRIBUTING.rst 原文——非琐碎改动（超过修 typo）无 Trac 票会被直接关掉；先在 code.djangoproject.com 建票再提 PR。
- 不要跳过测试跑改动：tox 默认命令就是 `cd tests && python runtests.py`，修 bug 的 PR 须附测试（贡献指南行为契约，见第 2 节）。
- 不要只跑部分检查就交工：格式黑盒 black、isort、flake8 三项各有独立 tox 环境，缺一项等于没过。
- 不要改 docs/*.txt 里的代码块不跑 blacken-docs：docs 有独立 `make black` 环境，文档内 Python 示例同样要合 black 口径。
- 不要在 JS 改动后跳过 `npm test`：仓内有 package.json、Gruntfile.js 与 js_tests/，JS 侧有独立 tox javascript 环境。
- 不要臆断数据库后端：默认跑 SQLite，PostgreSQL/MySQL/Oracle 各有 tests/requirements/ 下独立依赖文件，改动涉数据库行为先确认后端。

## 1. 常用命令
- 安装（可编辑）：`pip install -e .`（tox 用 usedevelop=true，默认可编辑安装）
- 测试：`cd tests && python runtests.py`（tox py3 环境同此命令；可加测试标签只跑指定模块）
- 指定后端测试：先装对应依赖（如 `pip install -r tests/requirements/postgres.txt`），再进 tests 跑 runtests.py
- 格式检查：`black --check --diff .`（tox black 环境；target-version py312）
- 导入排序：`isort --check-only --diff django tests scripts`（tox isort 环境；black profile，django 为 first-party）
- 静态检查：`flake8 .`（tox flake8 环境，flake8 ≥7.3.0；口径见根目录 .flake8）
- 文档代码块：`cd docs && make black`（blacken-docs；tox blacken-docs 环境）
- 文档拼写：`cd docs && make spelling`（Sphinx＋pyenchant＋sphinxcontrib-spelling；tox docs 环境）
- 文档 lint：`cd docs && make lint`（sphinx-lint；tox lint-docs 环境）
- JS 测试：`npm install && npm test`（tox javascript 环境）
- 工作流安全检查：`zizmor .`（tox zizmor 环境，zizmor ≥1.25.2）
- 一键 pre-commit：`pre-commit run --all-files`（black 26.5.1、isort 8.0.1、flake8 7.3.0、biome-check 2.4.15、zizmor 1.25.2，见 .pre-commit-config.yaml）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先在 Trac 建票（code.djangoproject.com/newticket），PR 附问题描述＋改动说明＋测试，缺测试不交工。
- 加功能：先建票讨论，贡献指南全文在 docs/internals/contributing/（线上版 docs.djangoproject.com/en/dev/internals/contributing/）。
- 完工证据：`runtests.py` 全绿＋black＋isort＋flake8 三项全绿；改文档加跑 `make spelling` 与 `make lint`；改 JS 加跑 `npm test`。
- 行为守则：贡献前先读 CONTRIBUTING.rst 与 Code of Conduct（djangoproject.com/conduct/）。

## 3. 项目指纹
- 技术栈：Python 3.12–3.15（3.15 含自由线程 free-threading beta）；打包 setuptools；格式化 black＋isort；检查 flake8；JS 侧 biome；文档 Sphinx。
- 结构：django/（框架本体）；tests/（测试套件，runtests.py 入口）；docs/（Sphinx 文档）；scripts/（开发脚本）；extras/；js_tests/（JS 测试）；.github/（CI 配置）。
- 核心源码：django/core/（管理命令与核心运行逻辑）；django/db/（ORM）；django/conf/（配置）；django/http/（请求/响应）；django/views/（通用视图）；django/forms/（表单）；django/template/（模板引擎）；django/contrib/（自带应用：admin、auth、sessions 等）；django/utils/（工具函数）；django/urls/（URL 分发）；django/test/（测试工具）。
- 写法约定：Python；测试集中在 tests/，按应用分子目录；文档为 .txt（reStructuredText，Sphinx 源）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改 ORM/查询/迁移 | django/db/ ＋ tests/ 对应模型测试 |
| 改请求处理/中间件/视图 | django/http/、django/middleware/、django/views/ ＋ tests/ 对应测试 |
| 改表单/模板 | django/forms/、django/template/、django/templatetags/ ＋ tests/ 对应测试 |
| 改 admin/auth 等自带应用 | django/contrib/<应用>/ ＋ tests/ 对应测试 |
| 改配置/启动/管理命令 | django/conf/、django/core/ ＋ tests/ 对应测试 |
| 改文档 | docs/（.txt 源文件，改后跑 make spelling＋make lint＋make black） |
| 改 JS（admin 等前端） | js_tests/ 与相关静态文件，改后跑 `npm test` |
| 改 CI/安全检查 | .github/、tox.ini、.pre-commit-config.yaml、zizmor.yml |

## 5. 测试
- 行为改动先加用例：测试在 tests/ 内按应用分子目录，跑 `python tests/runtests.py <标签>` 只验相关模块，全量跑不带标签。
- 后端回归：改动涉数据库时，默认 SQLite 之外至少确认 PostgreSQL/MySQL 侧依赖文件与行为（tests/requirements/ 下各后端文件）。
- 格式即测试：black、isort、flake8 任一不过视为未完工；提交前三项全绿。
- 文档回归：改 docs/*.txt 后跑 `make spelling`＋`make lint`＋`make black`，三项全绿。
- JS 回归：改 JS 相关文件后跑 `npm test`。

## 6. 边界
- ✅ 总是：非琐碎改动先建 Trac 票；改完跑 runtests.py＋black＋isort＋flake8；修 bug 必带测试
- ⚠️ 先问：新增运行时依赖（pyproject.toml dependencies 只有三项，动它先确认）、改 black/isort/flake8 口径（pyproject.toml 与 .flake8）、改公开 API（django/ 各包的公开导出）、改 docs 结构
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- runtests.py 单测标签写法与常用过滤参数：本稿只实读到 tox 命令 `runtests.py {posargs}`，未逐字核对标签语法，改动前以 tests/runtests.py --help 为准。
- 各数据库后端的切换方式（环境变量/命令行参数）：本稿只确认 tests/requirements/ 下有 postgres/mysql/oracle 三个依赖文件，未核实切换口径，不写断言。
- docs 构建主命令（make html 等）：本稿只实读到 make spelling / make lint / make black 三个目标，未核实完整构建命令。
- 发版流程（版本号提升与 Release notes 落点）：本稿只确认版本取自 django.__version__、Release notes 在 docs.djangoproject.com/en/stable/releases/，未核实发版触发方式。
