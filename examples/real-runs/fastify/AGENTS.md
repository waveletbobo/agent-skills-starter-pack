# AGENTS.md（fastify）

快速低开销的 Node.js Web 框架（package.json 原文："Fast and low overhead web framework, for Node.js"），MIT，6.0.0-alpha.6，CommonJS，入口 fastify.js＋fastify.d.ts；运行时依赖 15 项（avvio、find-my-way、pino、fast-json-stringify、@fastify/* 编译器等），源码无构建步骤，build/ 只生成 lib/ 内两份派生文件。

## 0. 不要做什么（最高优先级）
- 不要手改 lib/config-validator.js 与 lib/error-serializer.js：两者由 build/build-validation.js 生成，`npm run test:validator:integrity` 用 git diff 强制同步，手改会被该检查打回。
- 不要跳过 lint 就交工：`npm run lint`（eslint 9＋neostandard，ts:true）是唯一 JS lint 入口，另有 `npm run lint:markdown`（markdownlint-cli2）管文档。
- 不要只跑部分测试就交工：`npm test` 默认跑 lint＋unit＋test:types 三段，漏任一段等于没跑全。
- 不要在 PR 里升版本号：CONTRIBUTING.md 原文——发版是 lead maintainer 的 prerogative，PR 内不 bump version。
- 不要 --force 推 main 或改已合并 PR 的历史：CONTRIBUTING.md 明文禁止；非 main 分支做持续开发。
- 不要用纯 AI、无人参与的方式提 PR：CONTRIBUTING.md 原文——PR 必须由人类打开，非组织管理的 bot 开的 PR 会导致该 bot 被组织封禁。
- 不要把安全漏洞公开提 issue：SECURITY.md 已备，安全问题走该文件口径。
- 不要不读贡献指南就提 PR：正式规则在 CONTRIBUTING.md（OPEN 开源项目、双人审批、CI 全绿等），非正式操作细节在 docs/Guides/Contributing.md，文档风格在 docs/Guides/Style-Guide.md。

## 1. 常用命令
- 安装：`npm install`（源码无构建步骤，装完即用）
- 全量测试：`npm test`（lint＋unit＋test:types）
- 单元测试：`npm run unit`（borp，基于 Node 原生 test runner）
- 类型测试：`npm run test:types`（tstyche，测 types/）
- 覆盖率：`npm run coverage`（c8＋borp，html 报告）
- CI 口径覆盖率：`npm run coverage:ci-check-coverage`（borp --coverage --check-coverage --lines 100，即 100% 行覆盖硬门）
- Lint：`npm run lint`（eslint；口径见 eslint.config.js）
- Lint 自动修：`npm run lint:fix`（eslint --fix）
- 文档 lint：`npm run lint:markdown`（markdownlint-cli2）
- 生成文件校验：`npm run test:validator:integrity`（先 build:validation 再 git diff 比对两份派生文件）
- 版本号同步：`npm run build:sync-version`（prepublishOnly 链路内调用）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先复现（test/ 里加用例），再改 lib/ 或 fastify.js，最后 `npm test` 全绿。
- 加功能：先读 docs/Guides/Contributing.md；重大改动先开 issue 讨论再动手（该指南原文：minor 直接提 PR，major 先开 issue）。
- 外部 API 改动与重大修改须走内部 PR 征求其他贡献者反馈（CONTRIBUTING.md 原文）。
- 完工证据：`npm test` 全绿＋覆盖率 100% 行覆盖不掉；改文档同步改 docs/ 对应章节并过 markdownlint。
- 审批门：至少两位贡献者或一位核心成员批准方可合并，全部 CI 必须全绿；SemVer 大版本改动由 lead maintainer 合并。
- 版本分支：每个大版本有独立分支（1.x–4.x），改动须基于对应版本分支；LTS 政策见 docs/Reference/LTS.md。

## 3. 项目指纹
- 技术栈：Node、纯 JavaScript（CommonJS，'use strict'）＋TypeScript 类型定义（fastify.d.ts、types/），borp＋Node test runner 测试、tstyche 类型测试、eslint 9＋neostandard、markdownlint-cli2、c8 覆盖率。
- 结构：fastify.js（入口，34,867 字节）＋fastify.d.ts；lib/（框架本体，含 content-type-parser.js、content-type.js、config-validator.js、error-serializer.js 等）；test/（*.test.js，含 404s/500s 等按行为分子文件）；types/（tstyche 类型测试）；docs/（Reference/＋Guides/）；examples/（示例与 benchmark）；build/（生成脚本）；integration/；.github/workflows/（含 backport.yml 等）。
- 核心源码：fastify.js（装配与导出）；lib/content-type-parser.js（请求体解析）；lib/content-type.js；lib/config-validator.js 与 lib/error-serializer.js（生成文件，勿手改）。
- 写法约定：JavaScript；测试按被测行为分子文件（test/404s.test.js、test/500s.test.js 等）；文档在 docs/（非根目录 Readme）；代码风格 StandardJS 系（neostandard），行宽上限 120（eslint.config.js max-len，URL/字符串/模板/正则/注释除外，逗号结尾禁用）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改框架装配/导出/核心行为 | fastify.js ＋ test/ 对应用例 |
| 改请求体解析（content-type、parser） | lib/content-type-parser.js、lib/content-type.js ＋ test/ 对应用例 |
| 改配置校验/错误序列化逻辑 | build/build-validation.js（生成器）＋ test/ 对应用例，勿手改 lib/ 生成产物 |
| 改类型定义 | fastify.d.ts、types/（tstyche 用例同步改） |
| 改文档 | docs/ 对应章节（改后过 markdownlint，风格见 docs/Guides/Style-Guide.md） |
| 改 lint 口径 | eslint.config.js（neostandard 配置＋忽略列表） |
| 改测试/覆盖率口径 | package.json scripts（unit/coverage:ci-check-coverage） |
| 改 CI/发布 | .github/workflows/、package.json prepublishOnly 链路 |

## 5. 测试
- 行为改动先加用例：测试在 test/ 内按被测行为分子文件（*.test.js），跑 `npm run unit` 只验相关文件可加 borp 文件参数。
- 覆盖率硬门：CI 用 coverage:ci-check-coverage 校验 100% 行覆盖，改 lib/ 后须确认覆盖率不掉。
- 类型即测试：types/ 由 tstyche 校验，改 fastify.d.ts 必同步改类型用例并跑 `npm run test:types`。
- 生成文件同步：改 build/build-validation.js 或相关逻辑后跑 `npm run test:validator:integrity` 确认派生文件一致。
- 格式即测试：eslint 任一不过视为未完工；提交前 lint＋test 双绿；文档改动过 markdownlint。

## 6. 边界
- ✅ 总是：改 lib/ 必带测试；完工跑 `npm test`（lint＋unit＋types 三段）；覆盖率守住 100% 行覆盖；安全问题走 SECURITY.md；提 PR 前读 CONTRIBUTING.md
- ⚠️ 先问：新增运行时依赖（package.json dependencies 已有 15 项，动它先确认）、改 eslint 口径（eslint.config.js）、改公开 API（fastify.js 与 lib/ 的公开导出）、改 Node 最低版本（package.json 无 engines 字段，见待确认）
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- Node 最低版本（engines 字段与版本矩阵）：本稿只确认 package.json 无 engines 字段、无 .nvmrc，@types/node ^26 仅为开发依赖口径；动手前以 CI 矩阵为准。
- CI 工作流完整清单与各 Node 版本矩阵：本稿只实读到 .github/workflows/backport.yml 存在，未逐项核对全部工作流与矩阵。
- 发版流程细节（prepublishOnly 全链路、build:sync-version 的触发方与版本号来源）：本稿只确认 package.json 内 prepublishOnly 命令串，未核实发布触发条件与负责人。
- docs 风格指南细节：本稿只确认 docs/Guides/Style-Guide.md 存在，未逐字核对全文；改文档前以该指南为准。
