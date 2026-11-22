# AGENTS.md（jquery）

jQuery 4.1.0，DOM 操作 JavaScript 库（package.json 原文："JavaScript library for DOM operations"），OpenJS Foundation and other contributors，MIT，"type": "module"，main dist/jquery.js。零运行时依赖（package.json 无 dependencies 字段，只有 devDependencies）。

## 0. 不要做什么（最高优先级）
- 不要直接改 dist/ 或 dist-module/：两者是构建产物，且 2026-11-17 提交 "Release: remove dist files from main branch" 已把 dist 文件移出 main 分支；改 src/ 后走 `npm run build` 重建。
- 不要跳过 pretest 直接跑测试：`pretest` = qunit-fixture＋babel:tests＋npmcopy，缺了夹具/转译产物测试会失真；全量 `npm test` 链路是 build:all＋lint＋browserless＋browser＋esm＋slim＋no-deprecated＋selector-native，单跑一种不算完工。
- 不要绕过 lint：`npm run lint` = eslint（eslint.config.js）＋ package.json 的 jsonlint 两段，漏一段会卡 CI。
- 不要给核心包加运行时依赖：package.json 没有 dependencies 字段，新增依赖先问（devDependencies 另说）。
- 不要用错提交信息格式：commitplease 组件名只许用 Core/Ajax/Attributes/Callbacks/CSS/Data/Deferred/Deprecated/Dimensions/Effects/Event/Manipulation/Offset/Queue/Selector/Serialize/Traversing/Wrap/Docs/Tests/Build/Support/Release；修 bug 用 Closes/Fixes ＋票号格式。
- 不要在这里提插件或 API 文档的 issue：本仓只做 jQuery Core；插件问题找插件作者，API 文档问题去 api.jquery.com 仓（CONTRIBUTING.md 开头原文）。
- 不要不签 CLA 就交 PR：PR 须签署 OpenJS 贡献者许可协议（Corporate/Individual，可在 openjs-foundation/easycla 预览）。

## 1. 常用命令
- 安装：`npm install`（prepare 钩子装 husky）
- 构建：`npm run build`（node ./build/command.js）；全量构建 `npm run build:all`；监听开发 `npm start`
- 单元测试：`npm run test:unit`（jtr，带 test/middleware-mockserver.cjs）
- 无浏览器测试：`npm run test:browserless`（build:all＋jsdom 冒烟＋node 冒烟＋Promises/A+＋jsdom 单测）
- 浏览器测试：`npm run test:browser`（Chrome＋Firefox headless）；单浏览器：`npm run test:chrome`／`test:firefox`／`test:edge`／`test:safari`
- 变体测试：`npm run test:slim`、`test:no-deprecated`、`test:selector-native`、`test:esm`
- Node 冒烟：`npm run test:node_smoke_tests`；Promises/A+：`npm run test:promises_aplus`
- 风格：`npm run lint`（eslint＋jsonlint）；发版：`npm run release`（release-it，配置见 .release-it.cjs）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 报 bug 先自查三件（CONTRIBUTING.md 原文）：关浏览器扩展复现、用最新构建复测、把用例缩到最小可复现；无最小复现的 bug 单平均耗时高得多。
- 修 bug：先在 test/unit 找到对应模块的覆盖语义，再改 src/ 对应模块，最后跑 `npm run test:unit`＋相关变体测试。
- 新功能极少被接受：先读 wiki 的 API 设计原则与 Adding-new-features 页，通过指南的才考虑。
- 完工证据：`npm run build:all`＋`npm run lint`＋相关测试全绿；交工前自查 diff，只动该动的文件。
- 贡献前先读 CONTRIBUTING.md 与 contribute.jquery.org 的 commit & PR 指南；每周例会周一美东中午 #jquery/meeting，会议纪要在 meetings.jquery.org。

## 3. 项目指纹
- 技术栈：ESM 全仓（"type": "module"）；构建用自定义 build/ 任务（Rollup 4.68.4 在 devDependencies 内）；测试用 QUnit 3.0.0＋jquery-test-runner（jtr）＋jsdom 29.1.1＋sinon 9.2.4；提交信息用 commitplease；发版用 release-it 21.1.2。
- 结构：src/（按模块拆文件＋子目录：ajax、attributes、core、css、data、deferred、effects、event、manipulation、queue、selector、traversing 等，另有 var/ 与 exports/）；src/jquery.js 与 wrapper*.js（wrapper.js／wrapper-factory.js／wrapper-esm.js／wrapper-factory-esm.js）构成入口与包装层；build/（command.js、tasks/build.js、tasks/qunit-fixture.js、tasks/node_smoke_tests.js、tasks/promises_aplus_tests.js、release/）；test/（unit/、integration/、node_smoke_tests/、bundler_smoke_tests/、promises_aplus_adapters/、index.html、middleware-mockserver.cjs）；dist/ 与 dist-module/ 为构建产物目录。
- 写法约定：模块文件一一对应功能域（如 ajax.js＋ajax/、css.js＋css/）；ESM 源码，构建产物分 UMD/ESM/factory/slim 四种 exports（package.json exports 原文：.／./slim／./factory／./factory-slim／./src/*.js）。
- 测试分层：QUnit 单元测试（test/unit/）＋集成测试（test/integration/）＋Node 冒烟＋bundler 冒烟（jsdom）＋Promises/A+ 适配测试。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改核心工具/入口行为 | src/core.js＋src/core/、src/jquery.js ＋ test/unit/core.js |
| 改 Ajax | src/ajax.js＋src/ajax/ ＋ test/unit/ajax.js |
| 改属性/样式/尺寸 | src/attributes.js＋src/attributes/、src/css.js＋src/css/、src/dimensions.js ＋对应单测 |
| 改事件/队列/回调 | src/event.js＋src/event/、src/queue.js＋src/queue/、src/callbacks.js ＋对应单测 |
| 改动画效果 | src/effects.js＋src/effects/ ＋ test/unit/effects.js |
| 改 DOM 操作/遍历 | src/manipulation.js＋src/manipulation/、src/traversing.js＋src/traversing/ ＋对应单测 |
| 改选择器 | src/selector.js＋src/selector/、src/selector-native.js ＋ test:selector-native 变体验证 |
| 改构建/发版流程 | build/tasks/build.js、build/command.js、.release-it.cjs ＋ build/ 任务 |
| 改测试脚手架 | build/tasks/qunit-fixture.js、test/middleware-mockserver.cjs、test/index.html |
| 改文档/贡献指南 | README.md、CONTRIBUTING.md（API 文档本身不在本仓） |

## 5. 测试
- 行为改动先加用例：QUnit 单测放 test/unit/ 对应模块文件。
- 构建产物改动：`npm run build:all` 必须全过，只改源码不重建不算完工。
- 变体改动同步检查：slim 版（`npm run test:slim`）、去 deprecated（`test:no-deprecated`）、原生选择器（`test:selector-native`）、ESM（`test:esm`）各跑对应变体。
- 浏览器改动：`npm run test:browser`（Chrome＋Firefox headless）跑通再交；失败先看 test/middleware-mockserver.cjs 是否在跑（`npm run test:server` 可单独起）。

## 6. 边界
- ✅ 总是：改完跑 build:all＋lint＋相关单测；保持零运行时依赖；提交信息用 commitplease 组件名
- ⚠️ 先问：新增 devDependencies、改构建任务、改公开 exports、改发版配置
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- 最低 Node 版本：package.json 无 engines 字段，本稿未读 .github/workflows 的 CI 矩阵，不写版本断言，改动前以 CI 配置为准。
- build/command.js 的命令行选项（-e/--slim 等）完整语义：本稿只从 test 脚本确认了 -e deprecated、-e selector、--slim 三种用法，未读 command.js 全文。
- 发版触发方式：`npm run release`（release-it）为手动命令还是 CI 触发，本稿未核实，不写流程断言。
- dist-module/ 与 dist/ 各包装文件的具体差异：本稿只确认 exports 映射存在，未逐文件核对，不写差异断言。
