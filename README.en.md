# Gramcher

> Developed by the VWO team · Launched 2026-07-26 · Permanently in **Debugging Period** (hopefully)

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![GUI](https://img.shields.io/badge/GUI-tkinter-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

English | [中文](README.md)

Gramcher is a desktop utility built with **Python + tkinter** that helps developers spot three kinds of easily-overlooked problems in code:

- **Suspicious whitespace in code** (full-width spaces, trailing whitespace, indentation anomalies)
- **Special Chinese characters** (Chinese punctuation mixed into English code, full-width symbols)
- **Easily-confused characters across languages** (similar characters in Chinese / Japanese / Russian / Hindi / French / English)

The UI uses a dark theme, supports 6 interface languages, and the window is freely resizable.

---

## Features

- **Find Code Whitespace** — detects non-conforming whitespace in code and reports its line and column
- **Find Special Chinese Characters** — finds Chinese characters and full-width punctuation (e.g. `（）`, `，`, `：`)
- **Detect Language-Specific Characters** — groups the input text by language and lists the easily-confused characters
- **Responsive dark-theme UI** — rounded-card layout that adapts when the window is resized
- **6 interface languages** — 中文, English, 日本語, Français, हिन्दी, Русский, switchable with one click
- **Keyboard shortcut** — press `Ctrl+Enter` to run the main detection; copy result / clear input in one click
- **Packageable as EXE** — ships with a PyInstaller build script, runs without a Python environment

## Screenshots

<!-- TODO: add a screenshot here -->
<!-- ![Main UI](screenshots/main.png) -->

## Quick Start

### Requirements

- Python 3.8+
- Windows (the UI is built with tkinter; other platforms not tested)

> No third-party dependencies — only the Python standard library.

### Run

```bash
git clone https://github.com/ChewEmo/Gramcher.git
cd Gramcher
python main.py
```

### Build EXE

```bash
python build_exe.py
```

After building, the executable is located at `dist/Gramcher.exe`.

## Usage

1. Paste or type code / text into the **Input Box** above
2. Click a button below to run a detection:

| Button | Function |
| --- | --- |
| **Find Code Whitespace** (primary) | Detects suspicious whitespace and prints a `(line, column)` list |
| **Find Special Chinese Characters** | Prints the deduplicated Chinese characters and full-width symbols |
| **Detect Language-Specific Characters** | Groups and lists the easily-confused characters by language |
| **Clear Input** | Clears the input box in one click |
| **Copy Result** | Copies the output box content to the clipboard |

> Tip: press `Ctrl+Enter` inside the input box to run "Find Code Whitespace" directly.

### Output Examples

```
空格位置为: [(1, 9), (2, 15)]
```

```
检测到容易误判字符：
- 中文: ，
- English: l
```

## Multi-Language Support

The UI language can be switched in the toolbar. Translation files live in the project root:

| Language | File |
| --- | --- |
| 中文 | `zh_CN.json` |
| English | `en_US.json` |
| 日本語 | `ja_JP.json` |
| Français | `fr_FR.json` |
| हिन्दी | `hi_IN.json` |
| Русский | `ru_RU.json` |

Contributions of new translations are welcome (just add a JSON file and register it in `language_utils.py`).

## Project Structure

```
Gramcher/
├── main.py                  # Main entry (UI + logic dispatch)
├── searching_blanks.py      # Find Code Whitespace
├── specialchinesechara.py   # Find Special Chinese Characters
├── language_utils.py        # Language detection + translation loading
├── *.json                   # UI translations for 6 languages
├── background.png           # Background image
├── tubiao.ico               # Program icon
├── build_exe.py             # PyInstaller build script
└── build_exe.bat            # One-click build batch file
```

## Tech Stack

- **Python 3** + **tkinter** — UI and interaction
- **PyInstaller** — packaging and distribution
- Zero third-party runtime dependencies

## Development Status

This project is developed by the VWO team. The team **lacks experience and does not use AI coding**, so the product may have imperfections — your understanding is appreciated. Issues and PRs are welcome to help us improve.

## Credits & Contact

- Douyin (Chinese TikTok) search: **VMO星辰**
- GitHub: [ChewEmo/Gramcher](https://github.com/ChewEmo/Gramcher)

---

**License**: No license has been specified yet. Please contact the author before using it.
