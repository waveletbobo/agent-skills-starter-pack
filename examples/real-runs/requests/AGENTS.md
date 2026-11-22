# AGENTS.md（requests）

Requests 2.34.2，Python HTTP 库（pyproject.toml 原文：description "Python HTTP for Humans."），Python Software Foundation，Apache-2.0，requires-python >=3.10，源码在 src/requests/（src layout，setuptools packages.find where=["src"]），版本唯一来源 src/requests/__version__.py（__version__ = "2.34.2"）。运行时依赖仅 4 个：charset_normalizer>=2,<4、idna>=2.5,<4、urllib3>=1.26,<3、certifi>=2023.5.7。

## 0. 不要做什么（最高优先级）
- 不要直接改版本号以外的发布元数据：版本只改 src/requests/__version__.py（pyproject.toml 的 version 是 dynamic attr 引用），不要在 pyproject 里写死版本号。
- 不要绕过 pre-commit 直接交：.pre-commit-config.yaml 含 ruff-check（--fix）与 ruff-format（排除 tests/test_lowlevel.py），另有 check-case-conflict、check-merge-conflict、check-toml、check-yaml、end-of-file-fixer、mixed-line-ending、trailing-whitespace；未跑 pre-commit 的改动会在 CI 被拦。
- 不要只跑部分测试就声称完工：pyproject 的 pytest addopts 是 --doctest-modules，src/requests 内的 doctest 也算测试；完工须跑全量 `python -m pytest tests`。
- 不要给核心库加新运行时依赖：4 个依赖是刻意收敛的，新增依赖先问（可选依赖走 [project.optional-dependencies]：security 为空、socks 用 PySocks、use_chardet_on_py3 用 chardet）。
- 不要改 tests/test_lowlevel.py 的格式：ruff-format 明确排除该文件，格式化它会产生无关 diff。
- 不要跳过「先写失败测试」：贡献指南（docs/dev/contributing.rst）要求先写能复现 bug/功能的测试并确认失败，再改代码，最后全量测试全绿才发 PR 到 main 分支。
- 不要把新功能直接做成 PR：贡献指南要求不确定的贡献先尽早反馈（Get Early Feedback），维护者对是否适合本项目有最终决定权；行为守则遵循 PSF Code of Conduct。

## 1. 常用命令
- 安装开发依赖：`python -m pip install -r requirements-dev.txt`（Makefile init 目标；或 `make init`）
- 测试：`python -m pytest tests`（Makefile test 目标）；CI 形态：`python -m pytest tests --junitxml=report.xml`
- 覆盖率：`python -m pytest --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=src/requests tests`
- 类型检查：pyright，strict 模式，include 仅 src/requests（[tool.pyright]，依赖组 typecheck 含 pyright、typing_extensions、chardet、cryptography、PyOpenSSL）
- 风格：ruff（target-version py310，src 为 src/requests 与 tests，排除 docs/ 与 ext/；lint 选 E/W/F/I/UP/T10，忽略 E203/E501/UP031；format 为 black 兼容、双引号、空格缩进）
- 多版本矩阵：tox envlist 为 py{310,311,312,313,314}-{default,use_chardet_on_py3}，`tox` 跑矩阵；use_chardet_on_py3 环境额外装 security、socks、use_chardet_on_py3
- 文档：`make docs`（cd docs && make html，产物在 docs/_build/html/index.html）
- 发版：`make publish`（建 .publishenv 虚拟环境装 twine 与 build，`python -m build` 后 `twine upload --skip-existing dist/*`，随后删 build/dist/.egg/requests.egg-info）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 报 bug/提功能先读 docs/dev/contributing.rst：fork 仓→先跑全量测试确认基线全绿→写失败测试→改代码→全量测试全绿→PR 到 main 分支。
- 尽早反馈：未完成版也可以先发出来征求意见，不会因此降低被接受的概率；不合适的贡献会被拒，拒了也不影响下一次。
- 完工证据：`python -m pytest tests` 全绿（含 --doctest-modules 的模块内 doctest）＋ruff-check 与 ruff-format 全过＋pyright strict 全过；交工前自查 diff，只动该动的文件。
- 文档改动在 docs/ 下（Sphinx，.rst），API 文档入口 docs/api.rst，开发指南在 docs/dev/contributing.rst。

## 3. 项目指纹
- 技术栈：Python >=3.10（pyproject classifiers 覆盖 3.10–3.15，含 CPython 与 PyPy、自由线程 2 - Beta）；构建 setuptools>=61.0；测试 pytest>=3＋pytest-httpbin 2.1.0、httpbin~=0.10.0、pytest-cov、pytest-mock、pytest-xdist、trustme；类型 pyright strict；风格 ruff。
- 结构：src/requests/（api.py、sessions.py、models.py、adapters.py、auth.py、cookies.py、exceptions.py、structures.py、status_codes.py、compat.py、certs.py、hooks.py、help.py、_internal_utils.py、_types.py、packages.py、py.typed）；tests/（test_requests.py、test_adapters.py、test_lowlevel.py、test_hooks.py、test_help.py、test_packages.py、test_structures.py、test_utils.py、test_testserver.py、conftest.py、testserver/、certs/）；docs/（user/、dev/、community/、api.rst）；ext/（被 ruff 排除）；HISTORY.md、AUTHORS.rst、NOTICE、MANIFEST.in。
- 写法约定：公开 API 薄层在 api.py（get/post/put/patch/delete/head/options 等）之上，Session 在 sessions.py，请求/响应模型在 models.py，传输适配器在 adapters.py（urllib3 之上）；异常体系集中在 exceptions.py；兼容层集中在 compat.py（__init__.py 与 compat.py 允许 E402/F401）。
- 测试分层：pytest 单元/集成测试（tests/）＋模块内 doctest（addopts --doctest-modules）＋testserver 本地 HTTP 服务器夹具（tests/testserver/）＋pytest-httpbin 外部夹具；tox 矩阵覆盖 5 个 Python 版本 × 是否用 chardet。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改公开请求 API（get/post 等） | src/requests/api.py ＋ tests/test_requests.py |
| 改 Session 行为/重定向/合并设置 | src/requests/sessions.py ＋ tests/test_requests.py |
| 改请求/响应模型 | src/requests/models.py ＋ tests/test_requests.py |
| 改传输/连接/重试 | src/requests/adapters.py ＋ tests/test_adapters.py、tests/test_lowlevel.py |
| 改认证 | src/requests/auth.py ＋ tests/test_requests.py |
| 改 Cookie 处理 | src/requests/cookies.py ＋ tests/test_requests.py |
| 改异常类型 | src/requests/exceptions.py ＋对应测试 |
| 改工具结构/CaseInsensitiveDict | src/requests/structures.py、src/requests/utils.py ＋ tests/test_structures.py、tests/test_utils.py |
| 改状态码表 | src/requests/status_codes.py |
| 改版本/发布元数据 | src/requests/__version__.py、pyproject.toml、HISTORY.md |
| 改文档/贡献指南 | docs/（.rst）、README.md |

## 5. 测试
- 行为改动先加用例：失败测试先行（贡献指南 checklist 第 3 步），用例放 tests/ 对应模块文件；模块内 doctest 也要同步更新。
- 全量验证：`python -m pytest tests`（含 doctest）＋ruff-check/format＋pyright strict；多版本改动跑 `tox` 矩阵（py310–py314 × default/use_chardet_on_py3）。
- 网络相关改动：优先用 tests/testserver/ 本地夹具与 pytest-httpbin，不要依赖外网真实服务；证书相关用 tests/certs/ 与 trustme。
- 覆盖率：改动核心路径后跑 Makefile coverage 目标，确认覆盖未掉。

## 6. 边界
- ✅ 总是：先写失败测试再改代码；全量测试＋ruff＋pyright 全绿才交；版本只改 __version__.py
- ⚠️ 先问：新增运行时依赖、改公开 API、改 tox/pytest 配置、改发版流程
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- 最低 Python 版本的实际 CI 矩阵：pyproject classifiers 列 3.10–3.15，tox envlist 列 py310–py314，两者上限不一致（3.15 是否进 CI），本稿未读 .github/workflows 全文，不写断言。
- use_chardet_on_py3 的触发条件：可选依赖 chardet>=3.0.2,<8 与默认 charset_normalizer 的切换逻辑，本稿未读 _internal_utils.py 与 compat.py 全文，不写切换断言。
- 发版触发方式：`make publish` 为手动命令还是 CI 触发，本稿未核实，不写流程断言。
- ext/ 目录的用途与内容：本稿只确认 ruff 与 pre-commit 均排除 ext/，未读其内容，不写用途断言。
