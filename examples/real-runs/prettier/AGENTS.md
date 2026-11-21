# AGENTS.md（prettier）

代码格式化工具（package.json 原文："Prettier is an opinionated code formatter"），prettier 3.11.0-dev，ESM（"type": "module"），MIT，作者 James Long。单包仓，包管理器为 yarn。

## 0. 不要做什么（最高优先级）
- 不要从源码目录发布：package.json 有 `prepublishOnly: echo "Error: must publish from dist/" && exit 1`，发布只走 `dist/`，改源码后走 `node ./scripts/build/build.js` 重建。
- 不要降 Node 版本下限：engines 要求 Node >=22，降版本会断 CI。
- 不要只改代码不更新快照：测试用 Jest 快照，CONTRIBUTING.md 原文要求开 PR 前务必跑 `jest -u` 更新快照并 `git diff` 检查改动。
- 不要绕过自格式化：`lint:prettier` 对全仓跑 `prettier . --check --cache`，本仓用自己格式化自己，提交前先过 `yarn fix`。
- 不要给核心乱加运行时依赖：`lint:deps`（scripts/check-deps.js）会核查依赖，新增依赖先问。
- 不要跳过类型检查就交工：`yarn lint` 是 run-p 并行跑 lint:*，含 tsc 与 eslint，漏一项会卡 CI。

## 1. 常用命令
- 安装：`yarn`（仓根；CONTRIBUTING.md 原文两步：`yarn` → `yarn test`）
- 测试：`yarn test`（即 `jest`）
- 构建：`node ./scripts/build/build.js`（脚本在 scripts/build/build.js）
- 风格：`yarn lint:prettier`（`prettier . --check --cache`）；一键修复：`yarn fix`（fix:eslint＋fix:prettier）
- lint：`yarn lint`（run-p 并行 lint:*）；单项：`yarn lint:typecheck`（tsc）、`yarn lint:eslint`（eslint .）、`yarn lint:changelog`、`yarn lint:spellcheck`（cspell）、`yarn lint:deps`（check-deps.js）、`yarn lint:knip`
- 调试格式化：`node bin/prettier.js --ignore-path=.prettierignore`（另有 `debug:watch`、`debug:inspect`）
- 性能：`yarn perf`（yarn && yarn build && node dist/prettier/bin/prettier.cjs）；基准对比：`yarn perf:benchmark`、`yarn perf:compare`
- 生产态测试：`yarn test:production`（NODE_ENV=production）；独立包：`yarn test:production-standalone`；浏览器态：`yarn test:production:browser`（chrome/firefox 变体）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug / 改格式化行为：先看 `tests/format` 里对应目录的用例，再改 `src/language-*` 源码，最后跑 `jest -u` 更新快照并 `git diff` 复核。
- 完工证据：`yarn test` 全绿＋`yarn lint` 全绿；交工前自查 diff，确认只动了该动的文件。
- 贡献前先读 CONTRIBUTING.md：测试一节是行为契约（快照＋runFormatTest 签名），不是参考。

## 3. 项目指纹
- 技术栈：JavaScript ESM 全仓；测试 Jest（快照）；lint 用 eslint＋tsc＋cspell＋knip；构建脚本在 scripts/build/；发布产物在 dist/。
- 结构：src/cli（命令行入口）、src/main（核心流程）、src/common、src/config、src/document（打印中间层）、src/universal、src/utilities；语言插件按语言分目录 src/language-{css,graphql,handlebars,html,js,json,markdown,yaml}；src/plugins（插件加载）；src/experimental-cli（实验性 CLI）；入口 src/index.js／index.cjs／index.d.ts，独立包 src/standalone.js。
- 写法约定：ESM；本仓代码风格由自身格式化（.prettierignore 排除项见仓内）；拼写检查 cspell 覆盖全部文件。
- 测试分层：`tests/format/<语言>/<用例>/format.test.js` 调 `runFormatTest(import.meta, [解析器], 选项)`，同一输入多解析器输出必须一致；typescript 隐含 babel-ts/oxc-ts/yuku-ts，babel 在 js/jsx 下隐含 acorn/espree/meriyah/oxc/yuku。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改 JS/TS 格式化行为 | src/language-js/ ＋ tests/format/js（或 jsx/typescript）对应用例 |
| 改 CSS/HTML/Markdown 等语言行为 | src/language-{css,html,markdown,yaml,graphql,handlebars,json}/ ＋ tests/format 对应用例 |
| 改 CLI 行为/选项 | src/cli/ ＋ src/config/ |
| 改核心打印流程 | src/main/ ＋ src/document/ |
| 改插件加载/第三方插件支持 | src/plugins/ |
| 改构建/发布 | scripts/build/（发布只认 dist/，勿改 prepublishOnly 口径） |
| 改文档 | docs/（网站构建：`yarn build:website`） |

## 5. 测试
- 行为改动先加用例：每个 `tests/format` 子目录的 format.test.js 必须含至少一次 `runFormatTest` 调用；新用例文件放对应目录，跑 `jest -u` 生成快照。
- 快照是契约：`jest -u` 后必须 `git diff` 逐项看快照变化，意料外的 diff 说明改动面超预期，先收敛再提交。
- 多解析器一致性：同一输入在列表内各解析器输出必须相同，某解析器特判先问。
- 生产态回归：涉及打包/standalone 的改动加跑 `yarn test:production-standalone`；浏览器态改动加跑 `yarn test:production:browser`。

## 6. 边界
- ✅ 总是：改完跑 `yarn test`＋`yarn lint`；改格式化行为必更新快照并 diff 复核
- ⚠️ 先问：新增运行时依赖、改 Node 最低版本、改 src/language-* 目录划分、改公开 exports（index.js／standalone.js）
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- PR 是否必须先开 issue、changelog 条目由谁写：CONTRIBUTING.md 本稿实读部分未写明，以仓内贡献指南全文为准，本稿不臆断。
- src/main 与 src/document 的具体分工、src/plugins 内置插件清单：本稿只确认目录存在，未逐目录实读，改动前以对应目录内代码与测试为准。
- 发版流程（scripts/generate-changelog.js 与 publishCI 相关脚本的触发条件）：本稿只确认脚本存在，未核实触发方式，不写流程断言。
