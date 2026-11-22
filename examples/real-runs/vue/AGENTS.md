# AGENTS.md（vue / Vue 3）

Vue 3.5.46，渐进式 JavaScript 框架（vuejs/core），MIT 协议。Monorepo，pnpm workspace（packageManager pnpm@12.21.0，Node 用 `.node-version` 的 lts/*；`preinstall` 为 `npx only-allow pnpm`，不要用 npm/yarn 装依赖）。根 `package.json` 的 license 字段未填，以根目录 LICENSE 文件与 README「MIT」为准。12 个包在 `packages/` 下，另有 `packages-private/`（dts-test、dts-built-test、sfc-playground、template-explorer）。

## 0. 不要做什么（最高优先级）
- 不要用 npm 或 yarn 安装依赖：只能用 pnpm（`pnpm i`），`preinstall` 会拦其他包管理器。
- 不要只为风格重构代码：贡献指南明言不接受纯风格重构，只接受能提升性能或有充分理由证明客观提升代码质量的重构。
- 不要把新功能直接做成 PR：新 API 须先确认是广泛适用的用例；涉及新 API 表面或显著改变常用用法的大功能，须先走 RFC 讨论（vuejs/rfcs），无事先讨论的 PR 会被搁置。
- 不要把带新 API 表面的功能 PR 提到 main：新 API 功能提 `minor` 分支，其余提 `main` 分支。
- 不要不带复现就报修：bug 修复须有明确复现（关联 issue 或 PR 内自带），只说「修了什么」不解释「修的是什么」会被拒。
- 不要绕过提交信息校验：提交信息须合规（见第 2 节），simple-git-hooks 会在提交前校验，不合规则提交失败。
- 不要直接改 `dist/` 产物：构建产物由 `node scripts/build.js` 生成，改源码后重新构建。

## 1. 常用命令
- 安装依赖：`pnpm i`（推荐同时装 `@antfu/ni`，用 `nr` 跑脚本）
- 开发：`node scripts/dev.js`（默认目标 vue；可加 `-f esm-bundler` 等改格式，见 `scripts/dev.js`）
- 构建全部：`node scripts/build.js`；只构建某包：`node scripts/build.js vue -f global`（格式 global/esm-bundler/esm-browser/cjs 等，`-p` 产出生产版）
- 类型检查：`pnpm check`（`tsc --incremental --noEmit`）
- 风格：`pnpm lint`（eslint --cache .）、`pnpm format`（prettier --write --cache .）
- 测试：`pnpm test`（vitest 监听）；单次：`pnpm test-unit`（`vitest --project unit*`）；覆盖率：`pnpm test-coverage`
- E2E：`pnpm test-e2e`（先构建 global 版 vue 再跑 e2e 与 e2e-browser 两个 project）
- 类型测试：`pnpm test-dts`（先 `build-dts` 再跑两套 dts tsconfig）
- 发版：`node scripts/release.js`（维护者操作）；变更日志：`pnpm changelog`

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 报 bug 先走 https://new-issue.vuejs.org/ 建 issue；修 bug 的 PR 标题里加 `(fix #xxxx)`，如 `update entities encoding/decoding (fix #3899)`。
- PR 前勾选「Allow edits from maintainers」，让维护者可直接小改。
- 新功能：附测试用例＋有说服力的加入理由；先开 suggestion issue 获批再动手更稳妥。
- 提交信息格式（commit-convention.md，Angular 规范改编）：`^(revert: )?(feat|fix|docs|dx|style|refactor|perf|test|workflow|build|ci|chore|types|wip)(\(.+\))?: .{1,50}`，如 `feat(compiler): add 'comments' option`；破坏性变更在正文写 BREAKING CHANGE。
- 完工证据：`pnpm check`＋`pnpm lint`＋相关包单元测试全绿；改动核心路径后跑 `pnpm test-coverage` 确认覆盖未掉。
- 文档改动在 vuejs.org 仓，不在本仓；本仓 README 只写项目总览。

## 3. 项目指纹
- 技术栈：TypeScript（strict，`tsc --incremental --noEmit`）；构建 Rollup（`rollup.config.js`＋`scripts/build.js`，formats 由 `scripts/aliases.js` 与各包 `package.json` 的 buildOptions 定）；测试 Vitest（projects：unit、unit-gc、unit-jsdom、e2e、e2e-browser）；风格 ESLint＋Prettier（`.prettierrc`：semi false、singleQuote true、arrowParens avoid）；包管理 pnpm workspace；提交钩子 simple-git-hooks（`postinstall` 装钩子）。
- 结构：`packages/`（compiler-core、compiler-dom、compiler-sfc、compiler-ssr、reactivity、runtime-core、runtime-dom、runtime-test、server-renderer、shared、vue、vue-compat）；`packages-private/`（dts-test、dts-built-test、sfc-playground、template-explorer）；`scripts/`（build.js、dev.js、release.js、verify-commit.js、verify-treeshaking.js、aliases.js、inline-enums.js）；根配置 `vitest.config.ts`、`rollup.config.js`、`rollup.dts.config.js`、`tsconfig.json`、`tsconfig.build.json`、`eslint.config.js`。
- 写法约定：`reactivity` 可独立作框架无关包；`runtime-core` 为平台无关核心（含虚拟 DOM 渲染器与组件实现），`runtime-dom` 接浏览器 DOM；`vue` 包是含编译器的完整版（runtime＋compiler）；`shared` 放跨包内部工具；编译器分层为 compiler-core（平台无关）→ compiler-dom（浏览器插件）→ compiler-sfc（单文件组件）→ compiler-ssr（SSR 优化渲染函数）。
- 测试分层：unit（各包 `__tests__/`，jsdom 与 node 两个环境）、unit-gc（GC 相关）、e2e（真实浏览器，须先构建 global 版）、e2e-browser；dts 类型测试在 `packages-private/dts-test` 与 `dts-built-test`。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改响应式（ref/reactive/computed/watch） | packages/reactivity/src/ ＋ packages/reactivity/__tests__/ |
| 改组件/渲染器/虚拟 DOM | packages/runtime-core/src/ ＋ packages/runtime-core/__tests__/ |
| 改浏览器 DOM 行为（属性/事件/指令） | packages/runtime-dom/src/ ＋ packages/runtime-dom/__tests__/ |
| 改模板编译器 | packages/compiler-core/src/（平台无关）或 packages/compiler-dom/src/（浏览器）＋对应 __tests__/ |
| 改单文件组件编译 | packages/compiler-sfc/src/ ＋ packages/compiler-sfc/__tests__/ |
| 改 SSR 渲染 | packages/server-renderer/src/、packages/compiler-ssr/src/ ＋对应 __tests__/ |
| 改跨包内部工具 | packages/shared/src/（改动影响多包，须跑全量单元测试） |
| 改公开入口/打包格式 | packages/vue/ ＋ scripts/build.js、rollup.config.js |
| 改类型声明 | 各包 src 内类型＋ packages-private/dts-test/（构建后类型测 dts-built-test） |
| 改构建/发版脚本 | scripts/（build.js、dev.js、release.js） |

## 5. 测试
- 行为改动先加用例：新功能须附测试（贡献指南 PR 清单），用例放对应包 `__tests__/`；修 bug 附复现用例。
- 单包验证：`pnpm vitest run --project unit packages/reactivity`（按包过滤，vitest 监听模式外加 `run` 一次跑完）。
- 全量验证：`pnpm check`＋`pnpm lint`＋`pnpm test-unit`；涉及 SSR/E2E 再跑 `pnpm test-e2e`；改类型声明跑 `pnpm test-dts`。
- 覆盖率：`pnpm test-coverage`（只看改动包的覆盖变化，不追求全仓数字）。
- 性能相关改动：`pnpm bench`（vitest bench，`--compare=temp/bench.json` 对比基线）。

## 6. 边界
- ✅ 总是：pnpm 装依赖；新功能附测试；提交信息合规；新 API 功能提 minor 分支
- ⚠️ 先问：新增公开 API、大范围重构、改构建格式、改包间依赖
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- 各包 `buildOptions` 的完整格式矩阵：本稿未逐包读 `package.json` 的 buildOptions 字段，只确认根脚本与 rollup.config.js 的格式入口，不写逐包格式断言。
- `vue-compat`（Vue 2 兼容构建）的维护状态与改动口径：本稿未读其 README 与源码头注释，不写断言。
- `packages-private/sfc-playground` 与 `template-explorer` 的本地启动前置：本稿只确认 `dev-sfc` 系列脚本存在，未实跑，不写启动断言。
- 贡献指南中「广泛适用」的裁决实例：本稿只引原文标准，未列已接受/已拒实例，不写举例断言。
