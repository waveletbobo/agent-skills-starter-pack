# AGENTS.md（axios）

axios 1.13.3，Promise 风格的 HTTP 客户端（浏览器＋Node.js，package.json 原文："Promise based HTTP client for the browser and node.js"），MIT。入口：`index.js`（ESM，`module` 字段）、`./dist/node/axios.cjs`（CJS，`main` 字段）；类型 `index.d.ts`／`index.d.cts`。运行时依赖只有 3 个：follow-redirects、form-data、proxy-from-env。

## 0. 不要做什么（最高优先级）
- 不要直接改 `dist/`：它是 Rollup 构建产物（`npm run build` = `gulp clear && cross-env NODE_ENV=production rollup -c -m`）；改 `lib/` 后重建，`dist/` 不手改。
- 不要改公开 exports 映射而不跑 `test:exports`：`package.json` exports 分流 node／browser／bun／react-native 四档，外加 `./unsafe/*` 直指 `./lib/*`；改映射必须跑 `npm run test:exports`（`test/module/test.js`）。
- 不要跳过类型检查就改类型声明：`index.d.ts`／`index.d.cts` 改动必须过 `npm run test:dtslint`（dtslint＋本地 TypeScript）。
- 不要绕过 lint：`npm run test:eslint` 只扫 `lib/**/*.js`（`node bin/ssl_hotfix.js eslint lib/**/*.js`）；修格式用 `npm run fix`（`eslint --fix lib/**/*.js`），不要全局格式化。
- 不要用错提交信息格式：CONTRIBUTING.md 要求 conventional commits；`prepare` 脚本装 husky commit-msg 钩子（commitlint），提交信息不合规会被钩子拦。
- 不要交失败 CI 的 PR：CONTRIBUTING.md 原文——测试未更新、GitHub Actions 失败的 PR 不会被接受；先本地跑通再推。
- 不要改 `package.json` 的 `version` 字段手工发版：`preversion` 是 `gulp version`、`version` 脚本跑 `npm run build` 并 `git add package.json`，发版走 `release-it`（`npm run release`），不要手改版本号。

## 1. 常用命令
- 安装：`npm install`（`prepare` 钩子装 husky）
- 构建：`npm run build`（gulp clear＋Rollup）；只校构建版本：`npm run test:build:version`
- 全量测试：`npm run test`（`test:node`＋`test:browser`＋`test:package` 三段）
- Node 单元测试：`npm run test:mocha`（mocha `test/unit/**/*.js`，timeout 30000，`--exit`）
- 浏览器测试：`npm run test:karma`（`bin/run-karma-tests.js`）；Firefox 变体：`npm run test:karma:firefox`
- 包级检查：`npm run test:package`（eslint＋dtslint＋exports 三项）
- 覆盖率：`npm run test:node:coverage`（c8）
- 风格：`npm run test:eslint`；自动修：`npm run fix`
- 沙箱手动验证：`npm start`（`sandbox/server.js`，开 127.0.0.1:3000）；示例：`npm run examples`（`examples/server.js`）
- 发版：`npm run release`（release-it）；演练：`npm run release:dry`

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先在 `test/unit/` 找到对应模块的覆盖，再改 `lib/` 对应模块，最后跑 `npm run test:mocha`＋相关包级检查。
- 改行为先加用例：CONTRIBUTING.md 要求 PR 同步更新测试，测试不全的 PR 不接受。
- 改 API 同步改文档：文档在 axios-http.com（CONTRIBUTING.md 原文），API 与文档不一致不算完工。
- 完工证据：`npm run test` 全绿（node＋browser＋package 三段）；只跑 mocha 不算完工。
- 手动验证用沙箱：`npm start` 后在浏览器（127.0.0.1:3000）或终端（`node ./sandbox/client`）跑真实请求，见 CONTRIBUTING.md「Running Examples」。

## 3. 项目指纹
- 技术栈：纯 JS（ESM 源码＋Rollup 打包）；测试用 Mocha（Node）＋Karma（浏览器）＋dtslint（类型）；发版用 release-it＋gulp version；CI 在 `.github/workflows/run-ci.yml`。
- 结构：`lib/`（`axios.js` 入口、`core/`：Axios／AxiosError／AxiosHeaders／InterceptorManager／dispatchRequest／mergeConfig／settle／transformData；`adapters/`：fetch／http／xhr 三适配器；`defaults/`；`helpers/`；`cancel/`：CancelToken／CanceledError／isCancel；`env/`；`utils.js`）；`index.js`（ESM 入口）／`index.d.ts`／`index.d.cts`；`test/`（`unit/`、`specs/`、`helpers/`、`module/`、`manual/`）；`examples/`；`sandbox/`；`bin/`（`ssl_hotfix.js`、`run-karma-tests.js`、`check-build-version.js`）。
- 写法约定：核心请求链走 `lib/core/dispatchRequest.js`；适配器三分流（浏览器 fetch／xhr、Node http）；配置合并走 `mergeConfig`；拦截器走 `InterceptorManager`；错误统一 `AxiosError`。
- 测试分层：Mocha 单元测试（`test/unit/`）＋浏览器 Karma 测试＋包级检查（eslint／dtslint／exports）＋手动测试（`test/manual/`、sandbox、examples）。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改请求发送/响应处理 | `lib/core/dispatchRequest.js`、`lib/core/settle.js` ＋ `test/unit/` 对应单测 |
| 改配置/默认值/合并逻辑 | `lib/defaults/index.js`、`lib/core/mergeConfig.js` ＋对应单测 |
| 改拦截器 | `lib/core/InterceptorManager.js`、`lib/core/Axios.js` ＋对应单测 |
| 改某一环境适配器 | `lib/adapters/http.js`（Node）／`xhr.js`／`fetch.js`（浏览器） ＋对应单测 |
| 改请求头/错误类型 | `lib/core/AxiosHeaders.js`／`lib/core/AxiosError.js` ＋对应单测 |
| 改取消逻辑 | `lib/cancel/`（CancelToken／CanceledError／isCancel） ＋对应单测 |
| 改类型声明 | `index.d.ts`／`index.d.cts`，必跑 `test:dtslint` |
| 改构建/发版流程 | `rollup.config.js`、`gulpfile.js`、`.github/workflows/` ＋ `test:build:version` |
| 改文档 | axios-http.com 文档（本仓只放 README.md 概览，不写 API 全文） |

## 5. 测试
- 行为改动先加用例：Mocha 单测放 `test/unit/` 对应模块文件。
- 构建产物改动：`npm run build` 必须全过，只改源码不重建不算完工。
- 类型改动同步检查：`npm run test:dtslint` 跑通再交。
- 浏览器相关改动：`npm run test:karma` 跑通再交；失败先看 `karma.conf.cjs` 与 `bin/run-karma-tests.js`。
- 导出改动：`npm run test:exports` 必跑（四档 exports＋`./unsafe/*` 映射）。

## 6. 边界
- ✅ 总是：改完跑 `npm run test` 三段全绿；改 API 同步改测试与文档；提交信息用 conventional commits
- ⚠️ 先问：新增运行时依赖（现仅 3 个）、改 exports 映射、改构建/发版配置、改默认行为
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- 最低 Node 版本：package.json 无 engines 字段，本稿未读 `.github/workflows/run-ci.yml` 的 CI 矩阵，不写版本断言，改动前以 CI 配置为准。
- CONTRIBUTING.md「Developing」节称 `npm run test` 跑 jasmine 与 mocha 测试，但 package.json 的 test 链路是 mocha＋karma，无 jasmine；以 package.json 为准，CONTRIBUTING 该句疑似过期表述。
- husky 钩子实际状态：package.json `prepare` 脚本引用 husky install 与 commit-msg 钩子，但 main 树内无 `.husky/` 目录；钩子是否实际生效未核实，不写钩子断言。
- `mise.toml` 的用途：本稿未读该文件，不写断言。
