# Gramcher

> 由 VWO 团队开发 · 发起日 2026Y7M26D · 始终处于 **Debugging Period**（但愿）

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![GUI](https://img.shields.io/badge/GUI-tkinter-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

[English](README.en.md) | 中文

Gramcher 是一个基于 **Python + tkinter** 的桌面小工具，帮助程序员在代码中发现三类易被忽视的问题：

- **代码里的可疑空格**（全角空格、行尾空格、缩进异常）
- **特殊中文字符**（中文标点混入英文代码、全角符号）
- **不同语言的易混淆字符**（中文 / 日语 / 俄语 / 印地语 / 法语 / 英语 的相似字符）

界面采用深色主题，支持 6 种界面语言，窗口可自由缩放。

---

## 功能特性

- **查找代码空格** —— 检测代码中不符合规范的空格，并报告其行号与列号
- **查找特殊中文字符** —— 找出文本中的中文字符与全角标点符号（如 `（）`、`，`、`：`）
- **判断不同语言特殊字符** —— 对输入文本按语言分组，列出其中的易混淆字符
- **深色主题响应式界面** —— 圆角卡片布局，窗口缩放时控件自动适配
- **6 种界面语言** —— 中文、English、日本語、Français、हिन्दी、Русский，一键切换
- **快捷键** —— `Ctrl+Enter` 直接运行检测，复制结果、清空输入一键完成
- **可打包为 EXE** —— 提供 PyInstaller 打包脚本，无需 Python 环境即可运行

## 界面预览

<!-- TODO: 在此处放置界面截图 -->
<!-- ![主界面](screenshots/main.png) -->

## 快速开始

### 环境要求

- Python 3.8+
- Windows（界面使用 tkinter，其他平台未测试）

> 无需安装任何第三方依赖，仅使用 Python 标准库。

### 运行

```bash
git clone https://github.com/ChewEmo/Gramcher.git
cd Gramcher
python main.py
```

### 打包为 EXE

```bash
python build_exe.py
```

打包完成后，可执行文件位于 `dist/Gramcher.exe`。

## 使用方法

1. 在上方 **输入框** 粘贴或输入代码 / 文本
2. 点击下方按钮选择检测方式：

| 按钮 | 功能 |
| --- | --- |
| **查找代码空格**（主操作） | 检测可疑空格位置，输出 `(行, 列)` 列表 |
| **查找特殊中文字符** | 输出去重后的中文字符与全角符号 |
| **判断不同语言特殊字符** | 按语言分组列出易混淆字符 |
| **清空输入** | 一键清空输入框 |
| **复制结果** | 将输出框内容复制到剪贴板 |

> 提示：在输入框内按 `Ctrl+Enter` 可直接运行「查找代码空格」。

### 输出示例

```
空格位置为: [(1, 9), (2, 15)]
```

```
检测到容易误判字符：
- 中文: ，
- English: l
```

## 多语言支持

界面语言可在工具栏中切换，翻译文件位于项目根目录：

| 语言 | 文件 |
| --- | --- |
| 中文 | `zh_CN.json` |
| English | `en_US.json` |
| 日本語 | `ja_JP.json` |
| Français | `fr_FR.json` |
| हिन्दी | `hi_IN.json` |
| Русский | `ru_RU.json` |

欢迎提交新的语言翻译（只需新增一个 JSON 文件并在 `language_utils.py` 中注册）。

## 项目结构

```
Gramcher/
├── main.py                  # 主程序入口（界面 + 逻辑调度）
├── searching_blanks.py      # 查找代码空格
├── specialchinesechara.py   # 查找特殊中文字符
├── language_utils.py        # 语言检测 + 翻译加载
├── *.json                   # 6 种语言的界面翻译
├── background.png           # 背景图
├── tubiao.ico               # 程序图标
├── build_exe.py             # PyInstaller 打包脚本
└── build_exe.bat            # 一键打包批处理
```

## 技术栈

- **Python 3** + **tkinter** —— 界面与交互
- **PyInstaller** —— 打包分发
- 零第三方运行时依赖

## 开发状态

本项目由 VWO 团队开发，目前**缺少经验、未使用 AI Coding**，成品可能存在欠缺，恳请谅解。欢迎提交 Issue 与 PR，帮助我们改进。

## 致谢与联系

- 抖音搜索：**VMO星辰**
- GitHub：[ChewEmo/Gramcher](https://github.com/ChewEmo/Gramcher)

---

**License**：本项目暂未指定开源协议，如需使用请先联系作者。
