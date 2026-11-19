# AGENTS.md（commander）

Node.js 命令行框架（`program.option('-d, --debug')`），package.json 原文是 "the complete solution for node.js command-line programs"，零运行时依赖。

## 0. 不要做什么（最高优先级）
- 不要给包加运行时依赖：package.json 没有 dependencies 字段，只有 devDependencies；零依赖是发布物的一部分（files 只含 index.js、lib/*.js、typings/index.d.ts、package-support.json）。
- 不要改 CHANGELOG.md 或 package.json 的 version：发版时由维护者统一改（CONTRIBUTING.md 原文）。
- 不要直接提 PR：无 issue 先开 issue；未受维护者邀请不提 PR；不要提交基本由 AI 生成的 PR（CONTRIBUTING.md＋AI_POLICY.md）。
- 不要动公共 API 的导出形态：index.js（21 行）是唯一入口，导出 program、createCommand/createOption/createArgument 与 Command/Option/Argument/Help/错误类；lib/ 内部类只通过它对外。
- 不要把破坏性改动放进小版本：遵循 SemVer，破坏性改动只进大版本（约每半年一次，见 docs/release-policy.md）；不要擅自提高 engines 的 Node 最低版本（现 >=22.12.0，大版本才随 LTS 到期上调）。
- 不要只跑 `npm test` 就交工：它只含 node:test＋ts 类型检查，格式与 lint 在 `npm run check` 里，漏了会卡 CI。

## 1. 常用命令
- 测试（全套）：`npm test`（node --test 全部用例＋tsd/tsc 类型检查）
- 全面自查：`npm run test-all`（测试＋check：类型＋eslint＋prettier）
- 分项：类型 `npm run check:type`；lint `npm run check:lint`；格式 `npm run check:format`（prettier --check）
- 修复格式/lint：`npm run fix`
- 自查：`git diff` 看改动面；本仓没有 build 命令，不要臆造

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先看 tests/ 里对应用例覆盖哪条语义，再改 lib/，最后跑 `npm test`。
- 完工证据：`npm run test-all` 全绿输出；交工前自查 diff，确认只动了该动的文件；PR 目标分支是 develop，不是 main。

## 3. 项目指纹
- 技术栈：JavaScript（ESM，package.json 声明 `"type": "module"`）＋手写 TypeScript 类型声明 typings/index.d.ts（1116 行）；Node >=22.12.0；零运行时依赖。
- 结构：index.js（入口，21 行）、lib/command.js（核心，2803 行）、lib/help.js（735 行）、lib/option.js（377 行）、lib/argument.js（147 行）、lib/error.js（36 行）、lib/suggestSimilar.js（99 行）；tests/（node:test，104 个 *.test.js，另有 .cjs/.mjs 专项）；examples/（可运行示例）；docs/（术语/选项/帮助/解析与钩子/发版策略）。
- 写法约定：2 空格缩进、LF、文件末尾空行（见 .editorconfig）；prettier 单引号（.prettierrc.js）；ESLint flat config（eslint.config.js，含 typescript-eslint 与 eslint-node-test）。
- 测试命名：`<主题>.test.js`，按命令/选项/参数等主题分组（如 command.action.test.js、argument.choices.test.js、help.boxWrap.test.js）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改命令解析/执行逻辑 | lib/command.js ＋ tests/command.*.test.js 补用例 |
| 改选项定义/解析 | lib/option.js ＋ tests/option.*.test.js |
| 改参数定义/校验 | lib/argument.js ＋ tests/argument.*.test.js |
| 改帮助输出 | lib/help.js ＋ tests/command.*help*.test.js / help.*.test.js |
| 改错误类型/退出行为 | lib/error.js ＋ tests/command.error.test.js |
| 改类型声明 | typings/index.d.ts（与 Readme.md 的 API 一节对齐，tsd 会卡住） |
| 改文档 | Readme.md（＋ Readme_zh-CN.md 同步）与 docs/ 对应专题 |

## 5. 测试
- 行为改动先在 tests/ 加用例：node:test 的 describe/test＋assert/strict（见 tests/command.action.test.js）；共享辅助在 tests/testHelpers.js。
- 可执行子命令有专用的 .cjs mock/search 测试（tests/command.executableSubcommand.*.test.cjs），不要当普通 .js 改。
- 类型改动同步改 typings/index.d.ts，`npm test` 里的 tsd＋tsc 段会卡住。

## 6. 边界
- ✅ 总是：改完跑 `npm run test-all`；保持零运行时依赖
- ⚠️ 先问：新增导出、改公共 API 语义、提高 Node 最低版本、改 lib/ 分层
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- examples/ 的示例是否随功能改动同步更新：仓内无成文规定说明示例与功能的同步节奏。
- Readme_zh-CN.md 的同步节奏：仓内无成文规定说明中文版何时跟随英文版更新。
