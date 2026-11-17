# AGENTS.md（slash）

把 Windows 反斜杠路径转成正斜杠路径的单函数 npm 包（`foo\\bar` → `foo/bar`），ESM only，由 npm 使用者直接 import。

## 0. 不要做什么（最高优先级）
- 不要转换扩展长度路径：以 `\\?\` 开头的路径必须原样返回（这是 index.js 里唯一的特殊分支，test.js 有专门用例，改错就是行为回归）。
- 不要给包加运行时依赖：package.json 无 dependencies 是刻意的，单函数零依赖是这个包的立身之本。
- 不要单方面改默认导出签名：`export default function slash(path: string): string`，index.js 与 index.d.ts 必须同步修改。
- 不要引入构建步骤：没有打包器，index.js 直接发布（package.json 的 files 只含 index.js、index.d.ts）。
- 注释只写为什么，不写「以防万一」的分支。

## 1. 常用命令
- 测试（全套）：`npm test`（依次跑 xo 风格检查、ava 单元测试、tsd 类型测试）
- 分项：单元测试 `npx ava`；类型 `npx tsd`；风格 `npx xo`
- 自查：`git diff` 看改动面；本仓没有 build 命令，不要臆造

## 2. 工作流
- 3 步以上改动先写计划（文件→改动点→验证），确认再动手。
- 修 bug：先看 test.js 两个既有用例各覆盖哪条语义，再改 index.js，最后跑 `npm test`。
- 完工证据：`npm test` 全绿输出；交工前自查 diff，确认只动了该动的文件。

## 3. 项目指纹
- 技术栈：JavaScript（ESM，package.json 声明 `"type": "module"`）＋手写 TypeScript 类型声明 index.d.ts；Node >=14.16（engines），CI 实测 Node 14/16/18。
- 结构：根目录平铺——index.js（实现，约 10 行）、index.d.ts（类型）、test.js（ava 用例）、index.test-d.ts（tsd 用例）、readme.md（API 文档）。
- 写法约定：Tab 缩进、LF、UTF-8（见 .editorconfig）；readme 与 index.d.ts 里的路径示例保持一致，字符串示例注意反斜杠转义。

## 4. 任务→文件映射
| 任务 | 改哪里 |
|---|---|
| 改转换逻辑 | index.js ＋ test.js 补用例 |
| 改类型或文档注释 | index.d.ts（与 readme.md 的 API 一节对齐） |
| 改发布内容或引擎范围 | package.json 的 files / engines 字段 |

## 5. 测试
- 行为改动先在 test.js 加用例：现有两条语义（普通路径转换、扩展长度路径不转换）一条都不许丢。
- 类型改动同步改 index.test-d.ts，`npm test` 里的 tsd 段会卡住。

## 6. 边界
- ✅ 总是：改完跑 `npm test`；保持零运行时依赖
- ⚠️ 先问：新增导出、给 slash() 加参数选项、提高 Node 最低版本
- 🚫 永不：见第 0 节

## 待确认（补答后删此节）
- 是否接受给 slash() 增加选项参数：仓内无成文规定，readme 只记录了单参数 API。
- 发布节奏与版本号规则：仓内无 CHANGELOG 文件，无从读出。
