# 🌌 imissu - Google Antigravity 深度原生全量汉化包与复刻工具箱

适用于 **Google Antigravity 2.0**（独立伴侣客户端）与 **Antigravity IDE**（VS Code 核心开发环境）的双核心深度原生全量简体中文汉化项目。

---

## 🌟 为什么做这个项目？

目前社区对于 Antigravity 的汉化大多仅支持旧版或单侧架构，面对 Antigravity 新版的**双端架构**时常常出现以下问题：
1. **设置页面大面积英文**：常规设置、执行策略（`Queue` / `Send Immediately`）、安全预设（`Turbo Mode` / `Default` / `Full machine`）等依然显示英文。
2. **高级权限与规则未翻译**：网络访问规则（`Network Access Rules`）、工具权限卡片（`Tool Permissions`）、工件审查策略等关键配置缺失翻译。
3. **Windows 环境乱码困扰**：非标准编码写入导致中文字符串变 `\ufffd` 替换符，导致 DOM 拦截引擎完全失效。

**imissu** 提供了**架构级深度双向补丁**：
- **Antigravity 2.0 原生 DOM 拦截引擎**：高精度实时翻译 Electron 网页端呈现的所有卡片、徽章数字、下拉菜单和提示词。
- **Antigravity IDE 核心 Bundle 本地化**：深度修补工作台与 Agent React 组件，并经过 AST 语法树自检校验。
- **100% 纯净与零依赖**：基于 Python 标准库，无任何第三方包依赖，纯原生运行。

---

## 🚀 快速开始（一键安装）

### 方式一：Windows PowerShell 一键运行（推荐）

在本项目根目录下打开终端，直接运行：

```powershell
.\install.ps1
```

### 方式二：Python 跨平台运行

支持 Windows / macOS / Linux：

```bash
python install.py
```

如果软件安装在非默认路径，可指定路径参数：

```bash
python install.py --antigravity-dir "D:\ruanjian\IED\Antigravity" --ide-dir "C:\Users\<用户名>\AppData\Local\Programs\Antigravity IDE"
```

---

## 🛠️ 汉化覆盖明细

| 界面模块 | 英文原版 | imissu 精校中文 |
| :--- | :--- | :--- |
| **排队策略** | `Queue` / `Send Immediately` | **排队** / **立即发送** |
| **快捷键入口** | `Keyboard shortcuts` | **键盘快捷键** |
| **安全预设** | `Security Preset` | **安全预设** |
| **模式选项** | `Turbo Mode` / `Default` / `Full machine` | **极速模式** / **默认模式** / **完全访问** |
| **工具权限** | `Tool Permissions` (含徽章数) | **工具权限** |
| **网络规则** | `Network Access Rules` | **网络访问规则** |
| **工件策略** | `Artifact Review Policy` | **工件审查策略** |
| **沙盒外执行** | `Commands Outside Sandbox` | **沙盒外命令执行权限** |
| **终端命令** | `Terminal Commands` | **终端命令** |
| **文件访问** | `File Access Rules` | **文件访问规则** |
| **外部工具** | `MCP Tools` | **MCP 工具** |
| **云盘与 GitHub**| `Google Drive` / `GitHub` | **Google 云端硬盘** / **GitHub 权限** |

---

## 🔄 卸载与一键还原

如果需要完全还原为官方英文原始版本，只需运行：

```bash
python install.py --uninstall
```

本工具在首次运行时会自动创建 `.bak` 备份文件，卸载时将 1:1 还原官方原版。

---

## 🤝 贡献与规范

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 提交规范与 [git-push-conventions](https://github.com/xiaonangou/hermes-memory-wiki-xiaotu) 防火墙标准：
- 提交格式：`<type>(<scope>): <中文描述>`（例：`feat(汉化): 添加全量设置与权限汉化`）
- 描述字数 ≤ 50 字符，结尾不加句号。
- 推送前自动运行敏感信息与密钥检测 (`scripts/check-secrets.sh`)。

---

## 📄 开源许可证

本项目采用 [MIT License](LICENSE) 授权。
