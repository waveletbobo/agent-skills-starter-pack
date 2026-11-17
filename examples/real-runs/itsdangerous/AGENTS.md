# AGENTS.md（itsdangerous）

把数据安全地交给不受信任的环境、再取回验签的 Python 库（Pallets 维护），核心资产是签名/序列化格式的长期兼容。

## 0. 不要做什么（最高优先级）
- 不要随手改签名与编码格式：signer.py、encoding.py、timed.py 的输出就是已发出的令牌格式，改字节布局等于让存量令牌全部验签失败；确需改，先按仓内 PR 模板要求开 issue 讨论。
- 不要放宽 pytest 的警告策略：pyproject.toml 里 filterwarnings = ["error"]，新警告即测试失败，不许靠加 ignore 糊弄过去。
- 不要把 isinstance 元组写法改成联合类型语法：ruff 配置明确 ignore UP038，是刻意保留的兼容写法。
- 不要跳过 CHANGES.rst：PR 模板写死——行为变更要在 CHANGES.rst 加条目并链接 issue，代码文档加 `.. versionchanged::` 标注。
- 不要引入运行时依赖：pyproject.toml 的 [project] 段无 dependencies，零依赖是当前事实。

## 1. 常用命令
- 测试：`uv run pytest`（pyproject 已配 testpaths=tests）；全矩阵 `uv run --locked tox`（py3.10–3.13＋PyPy 3.11）
- 风格：`uv run pre-commit run --all-files`（ruff＋ruff-format，钩子版本在 .pre-commit-config.yaml 中冻结）
- 类型：`uv run --locked tox run -e typing`（mypy strict＋pyright，含 --verifytypes 核查）
- 构建：`uv build`（flit_core 后端）

## 2. 工作流
- 3 步以上先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先在 tests/test_itsdangerous/ 写一个没有修复就会失败的用例（PR 模板的硬性要求），再改 src/itsdangerous/。
- 完工证据三选一：pytest 通过输出 / tox 对应 env 全绿 / 类型检查输出；交工前自查 diff。

## 3. 项目指纹
- 技术栈：Python >=3.10，src 布局（src/itsdangerous/），flit_core 打包，uv 管理（uv.lock 锁定），tox 编排多环境。
- 模块：signer.py（Signer、HMACAlgorithm）、serializer.py（Serializer）、timed.py（时间戳变体）、url_safe.py（URL 安全变体）、encoding.py（base64 与字节转换）、exc.py（异常族）、_json.py（紧凑 JSON）。
- 写法约定：模块顶部 `from __future__ import annotations`；ruff 强制单行 import（isort force-single-line）；公共名在 __init__.py 以 `from .x import Y as Y` 显式再导出，新增公共 API 必须同步登记。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改签名行为 | src/itsdangerous/signer.py ＋ tests/test_itsdangerous/test_signer.py |
| 改序列化/编码 | serializer.py / encoding.py ＋ 对应的 test_*.py |
| 加异常类型 | exc.py ＋ __init__.py 再导出 ＋ docs 相应页 |
| 改文档 | docs/ ＋ CHANGES.rst 条目 |

## 5. 测试
- 每个行为变更都要有先失败、后通过的测试（PR 模板要求），测试文件与模块同名对应（test_signer.py 对 signer.py）。
- 改签名/编码逻辑跑全套 pytest，不许只跑单个文件就交工。

## 6. 边界
- ✅ 总是：改完跑 pytest 与 pre-commit；新增公共名同步 __init__.py
- ⚠️ 先问：改令牌格式、加依赖、动 requires-python 下限
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- main 与 stable 分支的发布分工：workflow 只见标签触发发布，两分支何时互相合入，仓内无成文说明。
- 发版节奏与版本号规则：pyproject 只记当前版本 2.3.0.dev，无发版日历可读。
