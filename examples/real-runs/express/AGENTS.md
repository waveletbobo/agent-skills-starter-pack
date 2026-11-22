# AGENTS.md（express）

极简、非强制观点的 Web 框架（package.json 原文："Fast, unopinionated, minimalist web framework"），MIT，Node ≥18；5.3.0，无构建步骤，入口 index.js 只转出 ./lib/express；运行时依赖 27 项，路由与 body 解析均为外部包（router ^2.2.0、body-parser ^2.4.0）。

## 0. 不要做什么（最高优先级）
- 不要改 lib/ 不同步改测试：仓内无构建产物可兜底，行为改动缺测试等于没改完（测试入口见第 1 节）。
- 不要跳过 lint 就交工：`eslint .` 是唯一 lint 入口，口径在根目录 .eslintrc.yml（eslint 8.47.0）。
- 不要只跑部分测试就交工：`npm test` 默认跑 test/ 与 test/acceptance/ 两个目录，漏 acceptance 等于没跑全。
- 不要臆断路由行为：路由实现在外部依赖 router 包（node_modules/router），不在本仓 lib/ 里，改路由语义先确认依赖版本与上游行为。
- 不要把安全漏洞公开提 issue：Readme §Security Issues 原文——发现安全漏洞走 Security Policies and Procedures（github.com/expressjs/express/security/policy）。
- 不要不读组织级贡献指南就提 PR：技术细节在 expressjs/.github 的 CONTRIBUTING.md（Readme §Contributing 链接），行为守则见 Code of Conduct。

## 1. 常用命令
- 安装：`npm install`（无构建步骤，装完即用）
- 测试：`npm test`（mocha --require test/support/env --reporter spec --check-leaks test/ test/acceptance/）
- TAP 输出测试：`npm run test-tap`（同上，reporter 改 tap）
- 覆盖率：`npm run test-cov`（nyc，排除 examples/test/benchmarks，html＋text 双报告）
- CI 口径覆盖率：`npm run test-ci`（nyc，lcovonly＋text）
- Lint：`npm run lint`（eslint .；口径见 .eslintrc.yml）
- Lint 自动修：`npm run lint:fix`（eslint . --fix）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先复现（test/ 里加用例或 acceptance 用例），再改 lib/，最后 `npm test`＋`npm run lint` 全绿。
- 加功能：先读组织级 Contributing Guide（expressjs/.github/CONTRIBUTING.md），确认讨论/issue 前置要求再动手。
- 完工证据：`npm test` 全绿＋`eslint .` 全绿；改文档同步改 Readme.md 对应章节。
- 行为守则：参与即须遵守 Code of Conduct（Readme §Contributing 原文）。

## 3. 项目指纹
- 技术栈：Node ≥18、纯 JavaScript（CommonJS，'use strict'）、mocha＋supertest 测试、eslint 8 检查、nyc 覆盖率。
- 结构：index.js（唯一入口，转出 lib/express）；lib/（框架本体 6 文件）；test/（74 项，含 acceptance/ 子目录）；examples/（示例应用）；.github/workflows/（ci、codeql、legacy、npm-publish、scorecard）；History.md（变更记录）。
- 核心源码：lib/express.js（导出与装配）；lib/application.js（app 方法与 settings）；lib/request.js（req 扩展）；lib/response.js（res 扩展）；lib/utils.js（工具函数）；lib/view.js（视图渲染）。
- 写法约定：JavaScript；测试按被测对象分子文件（test/app.*.js、test/req.*.js、test/res.*.js、test/Router.js 等）；文档在 Readme.md（非 docs/ 目录）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改 app 行为（settings、engine、路由挂载） | lib/application.js ＋ test/app.*.js |
| 改请求对象（req 属性/方法） | lib/request.js ＋ test/req.*.js |
| 改响应对象（res 方法、send/json/redirect） | lib/response.js ＋ test/res.*.js |
| 改导出/装配/中间件拼装 | lib/express.js ＋ test/express.*.js（json/raw/static/text/urlencoded 五个内置中间件测试） |
| 改视图渲染 | lib/view.js ＋ test/app.render.js |
| 改工具函数 | lib/utils.js ＋对应测试 |
| 改路由语义 | 先确认 router 依赖版本与上游行为，本仓只含挂载层（lib/application.js） |
| 改文档 | Readme.md（改后核对目录锚点） |
| 改 CI/发布 | .github/workflows/（ci.yml、npm-publish.yml 等） |

## 5. 测试
- 行为改动先加用例：测试在 test/ 内按被测对象分子文件，acceptance/ 放端到端用例；跑 `npm test` 只验相关文件可加 mocha 文件参数。
- 防泄漏：测试命令带 --check-leaks，全局变量泄漏会直接失败，新测试不许引入全局泄漏。
- 格式即测试：eslint 任一不过视为未完工；提交前 lint＋test 双绿。
- 覆盖率回归：改 lib/ 后跑 `npm run test-cov` 确认覆盖率不掉（CI 用 test-ci 的 lcovonly 报告）。

## 6. 边界
- ✅ 总是：改 lib/ 必带测试；完工跑 `npm test`＋`npm run lint`；安全问题走 security policy；提 PR 前读组织级 Contributing Guide
- ⚠️ 先问：新增运行时依赖（package.json dependencies 已有 27 项，动它先确认）、改 eslint 口径（.eslintrc.yml）、改公开 API（lib/ 各文件的公开导出）、改 Node 最低版本（engines 为 >= 18）
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- PR 前置流程（是否须先建 issue 讨论、标签与 reviewer 指派方式）：本稿只实读到 Readme §Contributing 指向组织级 CONTRIBUTING.md，未逐字核对该指南全文，动手前以该指南为准。
- test/support/env 的具体作用（环境变量/全局挂载）：本稿只确认测试命令 --require 该文件，未核实其内容。
- 发版流程（版本号提升、History.md 更新责任、npm 发布触发方式）：本稿只确认 .github/workflows/npm-publish.yml 存在，未核实触发条件与发布口径。
- examples/ 的维护口径（示例是否参与测试与 lint）：本稿只确认 test-cov 排除 examples，未核实 examples 是否被 eslint 覆盖。
