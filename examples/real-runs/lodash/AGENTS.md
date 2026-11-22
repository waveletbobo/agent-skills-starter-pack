# AGENTS.md（lodash）

JavaScript 实用工具库（单文件本体 lodash.js），MIT，Node ≥4.0.0；4.18.1，主入口 lodash.js；已进入功能完备（Feature-Complete）阶段（README 重要提示：获 Sovereign Tech Agency 支持后转入该阶段），新功能门槛高。

## 0. 不要做什么（最高优先级）
- 不要只改 lodash.js 不跑构建：dist/ 须同步提交，CI 的 ci-dist-sync 工作流会校验（改完跑 `npm run build`，把 dist/ 一并提交，否则 CI 报错）。
- 不要跳过 style 就交工：`npm run validate` 是 style＋test，风格口径在根目录 .jscsrc（jscs，行宽 180、花括号必写）。
- 不要只跑部分测试就交工：`npm test` 默认先跑 build（pretest），再跑 test:main＋test:fp，漏 FP 等于没跑全。
- 不要不读贡献指南就提 PR：先查 issue tracker（可能已讨论或已修），fork 后再提 PR；功能请求先走 issue，须社区投票（votes needed）攒够兴趣才会被考虑。
- 不要把安全问题公开提 issue：根目录有 SECURITY.md、threat-model.md 与 incident_response_plan.md，安全问题走 SECURITY.md 的渠道。
- 不要把新功能当默认改动：Feature-Complete 阶段以修 bug 与维护为主，加功能先走 issue 讨论。

## 1. 常用命令
- 安装：`npm install`
- 构建：`npm run build`（build:main＋build:fp；把根目录 lodash.js 复制到 dist/ 并压缩）
- 测试：`npm test`（pretest 先 build；test:main＋test:fp）
- 主测试：`npm run test:main`（node test/test）
- FP 测试：`npm run test:fp`（node test/test-fp）
- 风格：`npm run style`（jscs；口径见 .jscsrc）
- 全量校验：`npm run validate`（style＋test）
- 文档示例测试：`npm run test:doc`（markdown-doctest doc/*.md）
- 文档构建：`npm run doc`（node lib/main/build-doc github）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先复现（test/test.js 里加用例），再改 lodash.js，最后 `npm run validate` 全绿＋`npm run build` 同步 dist/。
- 加功能：先读 .github/CONTRIBUTING.md，确认 issue 前置要求（先查 tracker、功能请求须投票）再动手。
- 改 FP 版：同步看 fp/ 与 test/test-fp.js，不要只改主版。
- 完工证据：`npm run validate` 全绿＋dist/ 与源码同步（git diff dist/ 为空）；改文档同步改 doc/*.md 对应章节。
- 行为守则：参与即须遵守 OpenJS 基金会 Code of Conduct（CONTRIBUTING.md 原文）。

## 3. 项目指纹
- 技术栈：Node ≥4.0.0、纯 JavaScript（单文件，无构建器打包源码）、jscs 风格检查、QUnit 风格测试。
- 结构：lodash.js（唯一本体，根目录）；lib/（仅构建脚本：main、fp、common 三组）；test/（主套件 test.js 27,246 行、FP 套件 test-fp.js、浏览器 runner html、playwright 配置）；doc/（文档源，示例受 markdown-doctest 校验）；fp/（函数式编程版）；dist/（构建产物，须与源码同步提交）；.github/workflows/（ci-node、ci-bun、ci-docs、ci-dist-sync、browser-testing、codeql、renovate、scorecards）。
- 核心源码：lodash.js（全部方法实现都在这一个文件里，无源码分文件）；lib/main/build-dist.js（复制 lodash.js 到 dist/ 并压缩）；lib/fp/build-dist.js（FP 版构建）；lib/common/（构建公共函数：file、mapping、minify、util）。
- 写法约定：JavaScript；测试按方法分子文件在 test/test.js 内（单文件大套件）；文档在 doc/*.md（非 docs/ 目录）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改工具函数行为 | lodash.js ＋ test/test.js |
| 改 FP 版行为 | fp/ ＋ test/test-fp.js |
| 改构建产物 | 只改 lodash.js 后跑 `npm run build`，不要手改 dist/ |
| 改构建脚本 | lib/main/build-dist.js（主版）／lib/fp/build-dist.js（FP 版）／lib/common/（公共函数） |
| 改文档 | doc/*.md（改后跑 `npm run test:doc`） |
| 改风格口径 | .jscsrc |
| 改 CI | .github/workflows/（ci-node、ci-bun、ci-docs、ci-dist-sync 等 8 个） |
| 改贡献流程 | .github/CONTRIBUTING.md |

## 5. 测试
- 行为改动先加用例：测试在 test/test.js（主套件）与 test/test-fp.js（FP 套件）内，跑 `npm test` 只验相关方法可加文件参数。
- 先构建后测试：`npm test` 的 pretest 会跑 build，跳过 build 直接跑 node test/test 可能测到旧构建。
- 浏览器测试：test/ 下有 html runner（backbone.html、fp.html、index.html 等）与 playwright.config.js，走浏览器跑测试。
- 文档即测试：doc/*.md 的示例受 markdown-doctest 校验，改文档示例须跑 `npm run test:doc`。
- 风格即测试：jscs 任一不过视为未完工；提交前 style＋test 双绿（即 `npm run validate`）。

## 6. 边界
- ✅ 总是：改 lodash.js 必带测试；完工跑 `npm run validate`；改完跑 `npm run build` 同步 dist/；安全问题走 SECURITY.md；提 PR 前读 .github/CONTRIBUTING.md
- ⚠️ 先问：新增运行时依赖（package.json 依赖极少，动它先确认）、改 jscs 口径（.jscsrc）、改公开 API（lodash.js 的公开导出）、改 Node 最低版本（engines 为 >= 4.0.0）、加新功能（Feature-Complete 阶段，先走 issue）
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- fp/ 目录是构建产物还是手写源码（build:fp 的输入输出关系）：本稿只确认 build:fp 入口为 lib/fp/build-dist.js，未核实 fp/ 是否随构建重写。
- test/test.js 的单跑方式（如何只跑一个方法的用例、QUnit 过滤参数）：本稿只确认文件 27,246 行与入口命令 `node test/test`，未核实单测过滤方式。
- 发版流程（版本号提升、dist/ 提交责任、npm 发布触发方式）：本稿只确认 build-dist.js 复制＋压缩、ci-dist-sync 校验 dist/ 同步，未核实发布触发条件与发布口径。
- 新功能在 Feature-Complete 阶段的实际准入标准（issue 投票数阈值）：本稿只确认 CONTRIBUTING.md 要求先走 issue 投票，未核实具体票数门槛。
