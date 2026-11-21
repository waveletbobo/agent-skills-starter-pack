# AGENTS.md（vite）

前端开发构建工具（packages/vite/package.json 原文："Native-ESM powered web dev build tool"），Vite 团队出品，vite 8.4.0-beta.1，ESM（"type": "module"），MIT，作者 Evan You。pnpm workspaces 单仓。

## 0. 不要做什么（最高优先级）
- 不要用 npm/yarn 装依赖：根 package.json 有 `preinstall: npx only-allow pnpm`，包管理器只认 pnpm（packageManager 字段 pnpm@12.21.0）。
- 不要跳过构建直接改 `packages/vite/dist`：dist 是构建产物，改源码后走 `pnpm run build` 重建；开发时用 `packages/vite` 的 `pnpm run dev` 监听重建。
- 不要只跑 `pnpm test-unit` 就交工：`pnpm test` = test-unit ＋ test-e2e 两段，e2e 在 vitest.config.e2e.ts 下分 serve/build 等 project；格式与 lint 在 pre-commit 钩子里，漏了会卡提交。
- 不要改 Node 版本下限：engines 要求 Node ^20.19.0 || >=22.12.0，降版本会断 CI。
- 不要给 vite 核心包乱加运行时依赖：packages/vite 运行时依赖只有 5 个（lightningcss、picomatch、postcss、rolldown、tinyglobby），新增依赖先问。
- 不要绕过 lint-staged：pre-commit 钩子对全部文件跑 oxfmt，对 packages/*/src 与 types 下的 .ts 跑 oxlint --fix。

## 1. 常用命令
- 安装：`pnpm i`（仓根；多版本 pnpm 并存时建议先 `corepack enable`，CONTRIBUTING.md 原文）
- 构建全部包：`pnpm run build`（pnpm -r --filter='./packages/*' run build）
- 核心包开发监听：`cd packages/vite && pnpm run dev`（先清 dist，再 rolldown --config rolldown.config.ts -w）
- 核心包构建：`cd packages/vite && pnpm run build`（build-bundle＋build-types 两段；类型构建另有 rolldown.dts.config.ts）
- 单元测试：`pnpm test-unit`（根目录 vitest run）
- e2e 测试：`pnpm test-e2e`（vitest run -c vitest.config.e2e.ts；单测 serve：`pnpm test-serve`，单测 build：`pnpm test-build`）
- 风格：根目录 `pnpm run format`（oxfmt）；核心包 `pnpm run format` 同为 oxfmt
- lint：根目录 `pnpm run lint`（oxlint .）；核心包 `pnpm run lint`（oxlint src）
- 类型检查：根目录 `pnpm run typecheck`（tsc -p scripts＋各包并行 typecheck）；核心包 `pnpm run typecheck`（6 个 tsc 工程：根、src/node、src/client、src/module-runner、src/shared、两个 __tests_dts__）
- 文档构建：`pnpm run docs-build`（即 test-docs 的目标）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 开发核心包：仓根 `pnpm i` → `pnpm run build` → 进 packages/vite 跑 `pnpm run dev` 监听（CONTRIBUTING.md 原文三步）。
- 修 bug：先看对应测试覆盖哪条语义（单元在包内、e2e 在 playground/__tests__），再改源码，最后跑 `pnpm test-unit`＋相关 e2e project。
- 完工证据：`pnpm test-unit` 全绿＋`pnpm run lint`＋`pnpm run typecheck` 全绿；交工前自查 diff，确认只动了该动的文件。
- 贡献前先读 CONTRIBUTING.md 与文档站的 Project Philosophy 页（CONTRIBUTING.md 开头原文要求）。

## 3. 项目指纹
- 技术栈：TypeScript ~7.0.2；构建用 rolldown（~1.3.2，含 dts 构建）；测试用 vitest ^5.1.0＋playwright-chromium（e2e）；格式化 oxfmt、lint 用 oxlint（＋oxlint-tsgolint）；脚本运行 tsx。
- 结构：packages/vite（核心包，src 下分 node、client、module-runner、shared；bin/vite.js 为入口；exports 主入口为 ./dist/node/index.js，另有 ./client、./module-runner、./internal）；packages/create-vite（脚手架）；packages/plugin-legacy（旧浏览器插件）；playground/（e2e 夹具与用例）；scripts/（发布与 changelog 脚本，如 publishCI.ts、mergeChangelog.ts）；docs/（文档站）。
- 写法约定：ESM 全仓；oxfmt 格式化；oxlint 管 lint；TS 严格多工程检查（核心包 6 个 tsc 工程）。
- 测试分层：单元测试 vitest run；e2e 测试 vitest -c vitest.config.e2e.ts，分 serve/build 等 project；调试 serve 可用 `VITE_DEBUG_SERVE=1`，保留构建产物可用 `VITE_PRESERVE_BUILD_ARTIFACTS=1`。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改开发服务器/HMR 行为 | packages/vite/src/node/ ＋对应单元测试与 playground e2e 用例 |
| 改构建/打包逻辑 | packages/vite/src/node/（rolldown 配置在 rolldown.config.ts）＋ e2e build project |
| 改客户端运行时 | packages/vite/src/client/ ＋对应测试 |
| 改模块运行器 | packages/vite/src/module-runner/ ＋对应测试 |
| 改共享工具 | packages/vite/src/shared/ ＋引用它的三处复核 |
| 改脚手架 | packages/create-vite/ |
| 改旧浏览器插件 | packages/plugin-legacy/ |
| 改公开类型 | packages/vite/types/ 与 client.d.ts，构建后跑 build-types-check |
| 改文档 | docs/ 对应页，跑 `pnpm run docs-build` 验证 |

## 5. 测试
- 行为改动先加用例：单元用 vitest，e2e 用例放 playground/__tests__。
- 改核心构建/类型时：`pnpm run build` 必须全过（bundle＋dts 两段），只改源码不重建不算完工。
- 类型改动同步检查：核心包 `pnpm run typecheck` 覆盖 6 个工程，漏一个工程会卡 CI。
- 调试 e2e：serve 失败先加 `VITE_DEBUG_SERVE=1`；build 产物问题先加 `VITE_PRESERVE_BUILD_ARTIFACTS=1` 再看产物。

## 6. 边界
- ✅ 总是：改完跑 test-unit＋lint＋typecheck；保持 pnpm 唯一包管理器
- ⚠️ 先问：新增运行时依赖、改 Node 最低版本、改 packages/vite/src 四区划分、改公开 exports
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- PR 是否必须先开 issue、changelog 条目由谁写：CONTRIBUTING.md 本稿实读部分未写明，以仓内贡献指南全文为准，本稿不臆断。
- src/node 下各子目录分工与 playground 夹具命名约定：本稿未逐目录实读，改动前以对应目录内 README/测试为准。
- 发版流程（scripts/publishCI.ts 与 mergeChangelog.ts 的触发条件）：本稿只确认脚本存在，未核实触发方式，不写流程断言。
