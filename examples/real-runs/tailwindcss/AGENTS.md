# AGENTS.md（tailwindcss）

Utility-first CSS 框架（packages/tailwindcss/package.json 原文："A utility-first CSS framework for rapidly building custom user interfaces"），tailwindcss 4.3.5，MIT，作者 Tailwind Labs。pnpm 11.9.0＋turbo 单仓多包，TypeScript＋Rust 双语言（Rust 侧在 crates/）。

## 0. 不要做什么（最高优先级）
- 不要不构建就跑集成/UI 测试：CONTRIBUTING.md 原文要求集成测试与浏览器测试前先 `pnpm build`，直接跑会测到旧构建。
- 不要没先讨论就开新功能 PR：CONTRIBUTING.md 原文——新功能先在 Discussions 的 Ideas 分类提出来，不常接受新功能 PR，没排上优先级的 PR 会被关掉（不是功能不好，是没空跟进）。
- 不要改根 package.json 里的 prettier 口径：格式化规则就写在根 package.json 的 `"prettier"` 一节（semi false、singleQuote、printWidth 100），`pnpm run lint` 第一项就是 `prettier --check .`。
- 不要只跑 JS 测试就交工：根 `test` 脚本是 `cargo test && vitest run`，改 crates/ 必须过 Rust 侧测试。
- 不要跳过包内类型检查：packages/tailwindcss 的 `lint` 是 `tsc --noEmit`，类型不过不交工。
- 不要只改代码不加测试：CONTRIBUTING.md 原文——修 bug 的 PR 要附测试，新功能务必带测试，提交前全部测试通过。

## 1. 常用命令
- 安装：`pnpm install`（仓根；CONTRIBUTING.md 原文另需 Node.js＋Rustup＋pnpm 三件套）
- Rust 工具链：`rustup default stable`＋`rustup target add wasm32-wasip1-threads`
- 构建：`pnpm build`（即 `turbo build`，跳过 playgrounds；随后 `node ./scripts/pack-packages.mjs`）
- 开发监听：`pnpm tdd`（即 `vitest --hideSkippedTests` 监听模式）
- 测试：`pnpm test`（即 `cargo test && vitest run --hideSkippedTests`）
- 集成测试：`pnpm build && pnpm test:integrations`（vitest，根目录 integrations/）
- 浏览器测试：`pnpm build && pnpm test:ui`（playwright；单包：`pnpm run --filter=tailwindcss test:ui`）
- 风格：`pnpm run lint`（`prettier --check . && turbo lint`）；一键修复：`pnpm run format`（`prettier --write .`）
- 单包 lint：`pnpm run --filter=tailwindcss lint`（`tsc --noEmit`）；单包构建：`pnpm run --filter=tailwindcss build`（tsup-node，生产环境变量）
- 试跑场：`pnpm build && pnpm vite`（Vite playground）／`pnpm build && pnpm nextjs`（Next.js playground）

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：按 CONTRIBUTING.md 原文——PR 附问题描述＋改动说明＋测试，缺测试不交工。
- 加功能：先在 Discussions 发 Ideas 帖等排期，不要直接开 PR 写实现。
- 完工证据：`pnpm test` 全绿＋`pnpm run lint` 全绿；涉及构建产物或浏览器行为的改动加跑 `pnpm test:integrations`／`pnpm test:ui`。
- 贡献前先读 .github/CONTRIBUTING.md：测试一节是行为契约（构建先行、集成与 UI 分开跑），不是参考。

## 3. 项目指纹
- 技术栈：TypeScript（vitest 测试、tsup 打包）＋Rust（cargo test；crates/ 为 Rust 侧）；包管理 pnpm workspaces＋turbo；格式化 prettier（无分号、单引号、行宽 100）。
- 结构：packages/tailwindcss（核心包，src/index.ts 入口）；packages/@tailwindcss-{browser,cli,node,postcss,standalone,turbopack,upgrade,vite,webpack}（各集成端）；crates/（Rust 侧，实读见 node、ignore、classification-macros 等目录）；integrations/（集成测试）；playgrounds/（试跑场：vite-playground、nextjs-playground 等）。
- 核心源码：packages/tailwindcss/src/index.ts（入口）、compile.ts（编译）、candidate.ts（候选类名解析）、css-parser.ts（CSS 解析）、design-system.ts（设计系统）、compat/（v3 兼容层，colors/default-theme/plugin 均在此）；测试与源码同目录放（*.test.ts＋__snapshots__）。
- 写法约定：TypeScript；测试文件与源码同名加 `.test.ts` 后缀；基准测试用 `.bench.ts`。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改核心编译/候选解析 | packages/tailwindcss/src/compile.ts、candidate.ts ＋同目录 *.test.ts |
| 改 CSS 解析/设计系统 | packages/tailwindcss/src/css-parser.ts、design-system.ts ＋同目录测试 |
| 改 v3 兼容（颜色/默认主题/插件 API） | packages/tailwindcss/src/compat/ ＋同目录测试 |
| 改 Vite/PostCSS/CLI 等集成端 | packages/@tailwindcss-{vite,postcss,cli,…}/ 对应包 |
| 改 Rust 侧（扫描/忽略/分类） | crates/ 对应目录（改后必跑 `cargo test`） |
| 改构建/发版脚本 | scripts/（version-packages.mjs、changelog.mjs、pack-packages.mjs） |
| 改文档/贡献指南 | .github/CONTRIBUTING.md（仓根无 CONTRIBUTING.md，勿新建错位置） |

## 5. 测试
- 行为改动先加用例：测试与源码同目录，`*.test.ts` 就近放，跑 `pnpm tdd` 监听验证。
- 双语言回归：改 TS 跑 vitest，改 Rust 跑 `cargo test`，两者都改两者都跑，`pnpm test` 一次全过才算完工。
- 集成测试：改动影响最终 CSS 输出时，`pnpm build` 后跑 `pnpm test:integrations`。
- 浏览器测试：涉及 CSS 变量解析等浏览器行为时，`pnpm build` 后跑 `pnpm test:ui`（playwright）。
- 快照是契约：__snapshots__ 变化先逐项看 diff，意料外的 diff 说明改动面超预期，先收敛再提交。

## 6. 边界
- ✅ 总是：改完跑 `pnpm test`＋`pnpm run lint`；修 bug 必带测试；集成/UI 测试前先 `pnpm build`
- ⚠️ 先问：新增运行时依赖、改 prettier 口径、改 crates/ 目录划分、改公开 exports（packages/tailwindcss/package.json 的 exports 表）
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- crates/ 完整目录清单与各 crate 分工：本稿只实读到 node、ignore、classification-macros 三个目录名，未逐目录核实，改动前以对应目录内代码与测试为准。
- 发版流程（scripts/version-packages.mjs 与 changelog.mjs 的触发条件、changeset 口径）：本稿只确认脚本存在于根 scripts 一节，未核实触发方式，不写流程断言。
- packages/@tailwindcss-* 各集成包的 src 分工：本稿只确认包名清单，未逐包实读，改动前以对应包内代码与测试为准。
- PR 是否必须先开 issue：本稿实读的 CONTRIBUTING.md 部分未写明，以仓内贡献指南全文为准，本稿不臆断。
