# 更新日志 (Changelog)

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-09-10

### 新增 (Added)
- **双核心深度全量汉化**：同时支持 **Antigravity 2.0**（Electron 独立客户端）与 **Antigravity IDE**（VS Code 核心）。
- **DOM 动态翻译与正则引擎**：通过 `preload.js` 实时拦截和翻译网页端渲染的卡片、设置项、下拉菜单与动态字符串。
- **全量设置与权限管理汉化**：
  - 常规、执行策略、排队消息传递策略（`Queue` -> `排队`、`Send Immediately` -> `立即发送`）。
  - Agent 安全预设方案（`Turbo Mode` / `极速模式`、`Default` / `默认模式`、`Full machine` / `完全访问`）。
  - 工具与权限规则页面（文件访问规则、网络访问规则、终端命令、沙盒外命令执行权限、MCP 工具）。
  - 工件审查策略（`Artifact Review Policy` -> `工件审查策略`）。
- **自动化跨平台安装器 (`install.py`)**：
  - 自动探测默认安装路径与支持自定义路径传入。
  - 自动备份原始文件为 `.bak`，支持一键安全回滚 (`--uninstall`)。
  - 强制 UTF-8 编码，杜绝 Windows 平台中文乱码。
  - 内置 JavaScript AST 语法树自检 (`node --check`) 与 `app.asar` 自动解包重打包。
