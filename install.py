#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
imissu - Antigravity 2.0 & Antigravity IDE 深度原生全量汉化一键安装器
支持自动检测、安全备份、语法自检与一键回滚。
"""

import os
import sys
import json
import shutil
import argparse
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

def log(msg):
    print(f"\033[1;32m[imissu 汉化]\033[0m {msg}")

def log_warn(msg):
    print(f"\033[1;33m[警告]\033[0m {msg}")

def log_err(msg):
    print(f"\033[1;31m[错误]\033[0m {msg}", file=sys.stderr)

def find_default_antigravity_paths():
    candidates = []
    # 1. Environment / Custom drive
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    home = os.path.expanduser("~")

    # Windows candidates
    candidates.extend([
        r"D:\ruanjian\IED\Antigravity",
        os.path.join(local_app_data, "Programs", "Antigravity"),
        os.path.join(prog_files, "Antigravity"),
    ])

    # Linux & macOS
    candidates.extend([
        os.path.join(home, ".local", "share", "antigravity"),
        "/Applications/Antigravity.app/Contents/Resources"
    ])

    for c in candidates:
        if c and os.path.exists(c) and os.path.exists(os.path.join(c, "resources")):
            return c
    return None

def find_default_ide_paths():
    candidates = []
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    home = os.path.expanduser("~")

    candidates.extend([
        os.path.join(local_app_data, "Programs", "Antigravity IDE"),
        r"D:\ruanjian\IED\Antigravity IDE",
        os.path.join(prog_files, "Antigravity IDE"),
        os.path.join(home, ".local", "share", "antigravity-ide"),
        "/Applications/Antigravity IDE.app/Contents/Resources"
    ])

    for c in candidates:
        if c and os.path.exists(c) and os.path.exists(os.path.join(c, "resources")):
            return c
    return None

def patch_antigravity_2(antigravity_dir, uninstall=False):
    log(f"正在处理 Antigravity 2.0 (路径: {antigravity_dir})...")
    res_dir = os.path.join(antigravity_dir, "resources")
    app_dist_preload = os.path.join(res_dir, "app", "dist", "preload.js")
    asar_file = os.path.join(res_dir, "app.asar")
    asar_bak = asar_file + ".bak"

    if uninstall:
        log("执行卸载与恢复操作...")
        if os.path.exists(asar_bak):
            shutil.copyfile(asar_bak, asar_file)
            log(f"已从 {asar_bak} 恢复 app.asar")
        if os.path.exists(app_dist_preload + ".bak"):
            shutil.copyfile(app_dist_preload + ".bak", app_dist_preload)
            log(f"已从备份恢复 preload.js")
        log("Antigravity 2.0 恢复完成。")
        return True

    # 1. Load dictionary data
    with open(os.path.join(DATA_DIR, "dict.json"), "r", encoding="utf-8") as f:
        dict_data = json.load(f)
    with open(os.path.join(DATA_DIR, "placeholders.json"), "r", encoding="utf-8") as f:
        placeholders_data = json.load(f)

    # 2. Check and backup asar
    if os.path.exists(asar_file) and not os.path.exists(asar_bak):
        shutil.copyfile(asar_file, asar_bak)
        log(f"已创建原始 app.asar 备份: {asar_bak}")

    # 3. Build preload code
    dict_json = json.dumps(dict_data, ensure_ascii=False, indent=4)
    ph_json = json.dumps(placeholders_data, ensure_ascii=False, indent=4)

    # Read original base if preload exists
    original_base = ""
    if os.path.exists(app_dist_preload):
        if not os.path.exists(app_dist_preload + ".bak"):
            shutil.copyfile(app_dist_preload, app_dist_preload + ".bak")
        with open(app_dist_preload + ".bak", "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        # Keep original exports up to line 110
        kept = []
        for l in lines:
            if "/* antigravity-chinese" in l or "/* zh-hans" in l:
                break
            kept.append(l)
        original_base = "".join(kept)

    engine_code = f'''
/* antigravity-chinese-dom-engine-v2 */
(function() {{
    if (typeof window === 'undefined') return;

    const DICT = {dict_json};
    const PLACEHOLDERS = {ph_json};

    function translateText(str) {{
        if (!str || typeof str !== 'string') return str;
        const trimmed = str.trim();
        if (!trimmed) return str;

        if (DICT[trimmed]) return str.replace(trimmed, DICT[trimmed]);

        if (/^Tool Permissions\\s*\\d*$/i.test(trimmed)) return trimmed.replace(/Tool Permissions/i, "工具权限");
        if (/^Network Access Rules\\s*\\d*$/i.test(trimmed)) return trimmed.replace(/Network Access Rules/i, "网络访问规则");
        if (/^File Access Rules\\s*\\d*$/i.test(trimmed)) return trimmed.replace(/File Access Rules/i, "文件访问规则");
        if (/^Terminal Commands\\s*\\d*$/i.test(trimmed)) return trimmed.replace(/Terminal Commands/i, "终端命令");
        if (/^Commands Outside Sandbox\\s*\\d*$/i.test(trimmed)) return trimmed.replace(/Commands Outside Sandbox/i, "沙盒外命令执行权限");
        if (/^MCP Tools\\s*\\d*$/i.test(trimmed)) return trimmed.replace(/MCP Tools/i, "MCP 工具");

        if (/^Show \\d+ breakdowns?$/i.test(trimmed)) return trimmed.replace(/^Show (\\d+) breakdowns?$/i, "显示 $1 项明细");
        if (/^\\d+ tokens?$/i.test(trimmed)) return trimmed.replace(/^(\\d+) tokens?$/i, "$1 个 Token");
        if (/^\\d+ agents? running$/i.test(trimmed)) return trimmed.replace(/^(\\d+) agents? running$/i, "$1 个智能体运行中");
        if (/^No agents running$/i.test(trimmed)) return "无运行中的智能体";
        if (/^Step \\d+ of \\d+$/i.test(trimmed)) return trimmed.replace(/^Step (\\d+) of (\\d+)$/i, "第 $1 / $2 步");

        if (trimmed.startsWith("Settings - ")) return "设置 - " + (DICT[trimmed.substring(11)] || trimmed.substring(11));
        if (trimmed.startsWith("Learn more about ")) return "了解更多关于 " + (DICT[trimmed.substring(17)] || trimmed.substring(17));

        if (trimmed.includes("used some of your weekly limit")) {{
            return trimmed
                .replace(/You have used some of your weekly limit, it will fully refresh in\\s*/i, "您已使用部分每周限额，将在 ")
                .replace(/(\\d+)\\s*hours?/gi, "$1 小时")
                .replace(/(\\d+)\\s*minutes?/gi, "$1 分钟")
                .replace(/(\\d+)\\s*seconds?/gi, "$1 秒")
                .replace(/,\\s*/g, " ") + " 后完全重置。";
        }}
        return str;
    }}

    function processNode(node) {{
        if (!node) return;
        if (node.nodeType === Node.ELEMENT_NODE) {{
            const tag = node.tagName.toLowerCase();
            if (tag === 'code' || tag === 'pre' || tag === 'script' || tag === 'style') return;
            const cls = node.className || '';
            if (typeof cls === 'string' && (cls.includes('monaco-editor') || cls.includes('cm-content') || cls.includes('cm-editor'))) return;

            if (tag === 'input' || tag === 'textarea') {{
                const ph = node.getAttribute('placeholder');
                if (ph && PLACEHOLDERS[ph]) node.setAttribute('placeholder', PLACEHOLDERS[ph]);
                return;
            }}
            const title = node.getAttribute('title');
            if (title) {{
                const tr = translateText(title);
                if (tr !== title) node.setAttribute('title', tr);
            }}
            const aria = node.getAttribute('aria-label');
            if (aria) {{
                const tr = translateText(aria);
                if (tr !== aria) node.setAttribute('aria-label', tr);
            }}
        }}

        if (node.nodeType === Node.TEXT_NODE) {{
            const val = node.nodeValue;
            if (val && val.trim()) {{
                const tr = translateText(val);
                if (tr !== val) node.nodeValue = tr;
            }}
            return;
        }}

        if (node.childNodes && node.childNodes.length > 0) {{
            for (let i = 0; i < node.childNodes.length; i++) {{
                processNode(node.childNodes[i]);
            }}
        }}
    }}

    function injectStyles() {{
        const style = document.createElement('style');
        style.textContent = `
            * {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif !important;
            }}
        `;
        document.head.appendChild(style);
    }}

    function init() {{
        if (!document.body) {{
            window.addEventListener('DOMContentLoaded', init);
            return;
        }}
        injectStyles();
        processNode(document.body);

        let timer = null;
        const scheduleScan = () => {{
            if (timer) return;
            timer = setTimeout(() => {{
                timer = null;
                processNode(document.body);
            }}, 80);
        }};

        const observer = new MutationObserver((mutations) => {{
            let needsScan = false;
            for (const m of mutations) {{
                if (m.type === 'childList') {{
                    for (let i = 0; i < m.addedNodes.length; i++) {{
                        processNode(m.addedNodes[i]);
                    }}
                }} else if (m.type === 'characterData') {{
                    const node = m.target;
                    const val = node.nodeValue;
                    if (val && val.trim()) {{
                        const tr = translateText(val);
                        if (tr !== val) node.nodeValue = tr;
                    }}
                }} else if (m.type === 'attributes') {{
                    needsScan = true;
                }}
            }}
            if (needsScan) scheduleScan();
        }});

        observer.observe(document.body, {{
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: ['placeholder', 'title', 'aria-label']
        }});
    }}

    if (document.readyState === 'loading') {{
        window.addEventListener('DOMContentLoaded', init);
    }} else {{
        init();
    }}
}})();
'''
    full_preload = original_base + engine_code
    os.makedirs(os.path.dirname(app_dist_preload), exist_ok=True)
    with open(app_dist_preload, "w", encoding="utf-8") as f:
        f.write(full_preload)
    log(f"已成功写入 UTF-8 preload.js ({len(full_preload)} 字符)")

    # 4. AST check
    res = subprocess.run(f'node --check "{app_dist_preload}"', shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        log("JavaScript 语法树自检通过 (AST Syntax: PASSED)")
    else:
        log_err(f"语法检查失败: {res.stderr}")
        return False

    # 5. Pack asar if extracted folder or asar utility exists
    app_folder = os.path.join(res_dir, "app")
    if os.path.exists(app_folder):
        log("正在重新打包 app.asar...")
        cmd = f'npx asar pack "{app_folder}" "{asar_file}"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            log("app.asar 打包成功！")
        else:
            log_warn(f"asar 打包跳过或失败 (非关键，已写入 resources/app 目录): {res.stderr.strip()}")

    log("Antigravity 2.0 汉化补丁应用成功！")
    return True

def patch_antigravity_ide(ide_dir, uninstall=False):
    log(f"正在处理 Antigravity IDE (路径: {ide_dir})...")
    out_dir = os.path.join(ide_dir, "resources", "app", "out")
    wb_js = os.path.join(out_dir, "vs", "workbench", "workbench.desktop.main.js")
    jetski_js = os.path.join(out_dir, "jetskiAgent", "main.js")
    main_js = os.path.join(out_dir, "main.js")

    targets = [wb_js, jetski_js, main_js]

    if uninstall:
        log("恢复 Antigravity IDE 备份...")
        for p in targets:
            if os.path.exists(p + ".bak"):
                shutil.copyfile(p + ".bak", p)
                log(f"已恢复: {os.path.basename(p)}")
        return True

    # Check existence
    if not any(os.path.exists(p) for p in targets):
        log_err("未在指定目录找到 Antigravity IDE 核心 JS 文件。")
        return False

    # Replacements dictionary
    replacements = [
        ('case z1.NEXT_INVOCATION:return"Send Immediately";case z1.WHEN_IDLE:default:return"Queue"', 'case z1.NEXT_INVOCATION:return"立即发送";case z1.WHEN_IDLE:default:return"排队"'),
        ('children:"Keyboard shortcuts"', 'children:"键盘快捷键"'),
        ('label:"Security Preset"', 'label:"安全预设"'),
        ('U("Security Preset",', 'U("安全预设",'),
        ('Choose a predefined security preset for the agent. This controls terminal auto-execution policy, and file access policy.', '为 Agent 选择预定义的安全预设方案。这将控制终端命令自动执行策略与文件访问权限策略。'),
        ('children:["Learn more about"," "', 'children:["了解更多关于 "," "'),
        ('displayName:"Turbo mode"', 'displayName:"极速模式"'),
        ('shortDisplayName:"Turbo"', 'shortDisplayName:"极速"'),
        ('displayName:"Default"', 'displayName:"默认模式"'),
        ('shortDisplayName:"Default"', 'shortDisplayName:"默认"'),
        ('displayName:"Full machine"', 'displayName:"完全访问"'),
        ('Yr==="use_global"?"Inherit General":Yr==="custom"?"Custom"', 'Yr==="use_global"?"继承常规设置":Yr==="custom"?"自定义"'),
        ('label:"Network Access Rules"', 'label:"网络访问规则"'),
        ('description:"Configure allowed and denied URLs for reading."', 'description:"配置允许和拒绝读取的 URL 规则。"'),
        ('label:"File Access Rules"', 'label:"文件访问规则"'),
        ('description:"Configure allowed and denied paths for file reads and writes."', 'description:"配置允许和拒绝进行文件读取与写入的路径。"'),
        ('label:"Terminal Commands"', 'label:"终端命令"'),
        ('description:"Configure allowed terminal commands."', 'description:"配置允许执行的终端命令。"'),
        ('label:"Commands Outside Sandbox"', 'label:"沙盒外命令执行权限"'),
        ('description:"Configure allowed commands outside the sandbox."', 'description:"配置允许在沙盒外部执行的命令。"'),
        ('label:"MCP Tools"', 'label:"MCP 工具"'),
        ('description:"Configure external tools via Model Context Protocol."', 'description:"通过模型上下文协议 (MCP) 配置外部工具。"'),
        ('description:"Configure Google Drive access permissions."', 'description:"配置 Google 云端硬盘访问权限。"'),
        ('label:"GitHub",description:"Configure GitHub access policies."', 'label:"GitHub 权限",description:"管理 GitHub 仓库访问与操作权限。"'),
        ('title:"File Permissions",onBack:', 'title:"文件权限",onBack:'),
        ('title:"Network Permissions",onBack:', 'title:"网络权限",onBack:'),
        ('label:"Artifact Review Policy"', 'label:"工件审查策略"'),
        ('U("Artifact Review Policy",', 'U("工件审查策略",'),
        ('Yr==="use_global"?"Inherit General":Yr==="turbo"?"Always Proceed":"Always Ask"', 'Yr==="use_global"?"继承常规设置":Yr==="turbo"?"始终继续":"始终询问"'),
        ('label:"Prevent Sleep",description:"Prevent the computer from sleeping while the app is running."', 'label:"阻止系统休眠",description:"在应用程序运行期间阻止计算机进入休眠状态。"'),
        ('label:"Keep In Menu Bar",description:"Keep the app accessible from the menu bar and running in the background when all windows are closed."', 'label:"保持在系统托盘/菜单栏",description:"在所有窗口关闭后，仍保持应用在菜单栏/系统托盘中后台运行。"'),
        ('label:"Automatic Check for Updates",description:"When enabled, you will be automatically prompted to restart the app when there is a new update available. When disabled, you can check for updates manually from the app menu."', 'label:"自动检查更新",description:"启用后，当有新版本可用时将自动提示重启应用。禁用后，您可从应用菜单手动检查更新。"'),
        ('label:"Enable Remote Control",description:"Work with local agents from another device. If enabled, you can manage your conversations from the companion website."', 'label:"启用远程控制",description:"从其他设备使用本地智能体进行协作。启用后，您可以从配套网站管理您的对话。"'),
        ('label:"Notification Settings",description:"To modify notification settings, open your operating system\'s system preferences."', 'label:"通知设置",description:"若要修改通知设置，请打开操作系统的系统首选项/系统设置。"'),
        ('children:"Open System Preferences"', 'children:"打开系统设置"'),
    ]

    for p in targets:
        if not os.path.exists(p):
            continue
        bak = p + ".bak"
        if not os.path.exists(bak):
            shutil.copyfile(p, bak)
            log(f"已创建备份: {os.path.basename(bak)}")

        # Read from bak
        with open(bak, "r", encoding="utf-8", errors="ignore") as f:
            c = f.read()

        applied = 0
        for old_s, new_s in replacements:
            if old_s in c:
                c = c.replace(old_s, new_s)
                applied += 1

        with open(p, "w", encoding="utf-8") as f:
            f.write(c)

        # Check AST
        res = subprocess.run(f'node --check "{p}"', shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            log(f"{os.path.basename(p)} 补丁生效并校验通过 (应用 {applied} 处替换)")
        else:
            log_err(f"{os.path.basename(p)} 语法检查失败: {res.stderr}")

    log("Antigravity IDE 汉化补丁应用成功！")
    return True

def main():
    parser = argparse.ArgumentParser(description="imissu - Antigravity 深度原生汉化安装器")
    parser.add_argument("--antigravity-dir", help="Antigravity 2.0 安装根目录")
    parser.add_argument("--ide-dir", help="Antigravity IDE 安装根目录")
    parser.add_argument("--uninstall", action="store_true", help="卸载汉化补丁，还原初始备份")
    args = parser.parse_args()

    print("=" * 60)
    print("  imissu - Google Antigravity 2.0 & IDE 深度全量汉化")
    print("=" * 60)

    ag_dir = args.antigravity_dir or find_default_antigravity_paths()
    ide_dir = args.ide_dir or find_default_ide_paths()

    if not ag_dir and not ide_dir:
        log_err("未自动检测到 Antigravity 安装目录，请通过参数指定：")
        print("  python install.py --antigravity-dir <路径> --ide-dir <路径>")
        sys.exit(1)

    success = True
    if ag_dir:
        if not patch_antigravity_2(ag_dir, uninstall=args.uninstall):
            success = False
    else:
        log_warn("跳过 Antigravity 2.0（未找到路径）")

    if ide_dir:
        if not patch_antigravity_ide(ide_dir, uninstall=args.uninstall):
            success = False
    else:
        log_warn("跳过 Antigravity IDE（未找到路径）")

    print("=" * 60)
    if success:
        log("🎉 全部汉化处理完成！请重启软件或在窗口按 Ctrl+R 查看效果。")
    else:
        log_warn("处理完成，部分环节存在警告，请查看上方日志。")

if __name__ == "__main__":
    main()
