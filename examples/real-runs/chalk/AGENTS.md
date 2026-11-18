# AGENTS.md（chalk）

终端字符串着色库（`chalk.blue('Hello world!')`），ESM only，零运行时依赖，约 11.5 万个包依赖它。

## 0. 不要做什么（最高优先级）
- 不要给包加运行时依赖：ansi-styles 与 supports-color 是 vendored 进 source/vendor/ 的副本（package.json 的 imports 映射 `#ansi-styles` / `#supports-color`），不是 dependencies；零依赖是这个包的立身之本。
- 不要把 source/vendor 当成本仓源码改：xo 与 c8 的配置都排除该目录（第三方代码口径）；要升级先确认上游，再整体替换副本。
- 不要动 level 的取值范围：`level` 只能是 0–3 的整数（index.js 的 assertValidLevel 会抛错），level 本体存在 Symbol 下、对外是带校验的 accessor。
- 不要给 index.js 的热路径加开销：性能是卖点（根目录有 benchmark.js 对照），改动前后跑 `npm run bench` 对比。
- 不要引入构建步骤：没有打包器，source/ 直接发布（package.json 的 files 只含 source）。

## 1. 常用命令
- 测试（全套）：`npm test`（依次跑 xo 风格检查、c8 覆盖率下的 node:test、tsc 类型检查）
- 分项：风格 `npx xo`；单元测试 `node --test 'test/[!_]*.js'`；类型 `npx tsc --noEmit --types node source/index.d.ts`
- 性能：`npm run bench`（node --experimental-bench 跑 benchmark.js）
- 自查：`git diff` 看改动面；本仓没有 build 命令，不要臆造

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先看 test/ 里对应用例覆盖哪条语义，再改 source/index.js，最后跑 `npm test`。
- 完工证据：`npm test` 全绿输出；交工前自查 diff，确认只动了该动的文件。

## 3. 项目指纹
- 技术栈：JavaScript（ESM，package.json 声明 `"type": "module"`）＋手写 TypeScript 类型声明 source/index.d.ts；Node >=22（engines），CI 实测 Node 22/26。
- 结构：source/index.js（核心，259 行）、source/utilities.js（33 行）、source/index.d.ts（437 行）、source/vendor/（ansi-styles 与 supports-color 副本各含 index.js＋index.d.ts；supports-color 另有 browser.js/browser.d.ts）；test/（node:test，6 个用例文件＋2 个 `_` 前缀夹具）；benchmark.js 在根目录。
- 颜色级别：level 0–3＝全关/16 色/256 色/真彩色（readme 的 chalk.level 一节），自动检测、可由 `new Chalk({level: n})` 或 `FORCE_COLOR=n` 覆盖；stdout 与 stderr 各用一套检测（chalkStderr）。
- 写法约定：Tab 缩进、LF、UTF-8、去行尾空格、文件末尾空行（见 .editorconfig）；*.yml 用 2 空格。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改着色逻辑 | source/index.js ＋ test/chalk.js 补用例 |
| 改颜色级别检测 | source/index.js（level accessor）＋ test/level.js |
| 改类型或文档注释 | source/index.d.ts（与 readme.md 的 API 一节对齐） |
| 改工具函数 | source/utilities.js |
| 改发布内容或引擎范围 | package.json 的 files / engines 字段 |

## 5. 测试
- 行为改动先在 test/ 加用例：test/chalk.js 为主用例集（242 行）；夹具文件以下划线开头（_fixture.js、_force-color-fixture.js），`npm test` 的 glob `test/[!_]*.js` 会排除它们，不要直接跑夹具。
- 强制颜色用例走 test/force-color.js；无颜色支持走 test/no-color-support.js。
- 类型改动同步改 source/index.d.ts，`npm test` 里的 tsc 段会卡住。

## 6. 边界
- ✅ 总是：改完跑 `npm test`；保持零运行时依赖
- ⚠️ 先问：新增导出、改 level 语义、提高 Node 最低版本、改 vendor 副本
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- vendor 副本的同步节奏：仓内无成文规定说明何时跟随上游 ansi-styles / supports-color 发版。
- 发布节奏与版本号规则：仓内无 CHANGELOG 文件，无从读出。
