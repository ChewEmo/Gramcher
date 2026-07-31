import os
import sys
import tkinter
import searching_blanks
import specialchinesechara
import language_utils

# ---------------------------------------------------------------- 调色板
COLORS = {
    "bg": "#0f172a",
    "panel": "#111827",
    "card": "#1e293b",
    "border": "#334155",
    "text": "#f8fafc",
    "text_dim": "#94a3b8",
    "accent": "#3b82f6",
    "accent_hover": "#2563eb",
    "accent_active": "#1d4ed8",
    "field_bg": "#f8fafc",
    "field_fg": "#0f172a",
    "btn_bg": "#1e293b",
    "btn_hover": "#334155",
    "btn_active": "#475569",
    "btn_fg": "#f8fafc",
}

FONT_UI = ("Microsoft YaHei UI", 10)
FONT_UI_BOLD = ("Microsoft YaHei UI", 10, "bold")
FONT_TITLE = ("Microsoft YaHei UI", 12, "bold")
FONT_CODE = ("Consolas", 11)

LANGUAGES = ["中文", "English", "日本語", "Français", "हिन्दी", "Русский"]

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(base_dir, relative_path)


main_window = tkinter.Tk()
main_window.title("Gramcher GUI")
main_window.geometry("1024x768")
main_window.minsize(720, 560)
main_window.configure(bg=COLORS["bg"])
try:
    main_window.iconbitmap(get_resource_path("tubiao.ico"))
except Exception:
    pass

# ---------------------------------------------------------------- 背景图（有 PIL 时缩放适配窗口，无 PIL 时纯色）
bg_image_ref = {"photo": None, "label": None, "pil": None}


_bg_resize_job = None


def _background_resize(event=None):
    """窗口尺寸变化时防抖调度重绘，避免拖拽时反复全量重采样背景图。"""
    global _bg_resize_job
    if _bg_resize_job is not None:
        try:
            main_window.after_cancel(_bg_resize_job)
        except Exception:
            pass
    _bg_resize_job = main_window.after(120, _do_background_resize)


def _do_background_resize():
    global _bg_resize_job
    _bg_resize_job = None
    pil = bg_image_ref["pil"]
    if pil is None:
        return
    try:
        from PIL import Image, ImageTk

        w = main_window.winfo_width() or 1024
        h = main_window.winfo_height() or 768
        if w <= 1 or h <= 1:
            return
        # cover 模式：等比放大填满窗口后居中裁剪，不变形
        tw, th = pil.size
        scale = max(w / tw, h / th)
        new_w, new_h = int(tw * scale), int(th * scale)
        # Pillow >= 9.1 用 Image.Resampling，旧版回退 Image.LANCZOS
        resampling = getattr(Image, "Resampling", Image)
        img = pil.resize((new_w, new_h), resampling.LANCZOS)
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        img = img.crop((left, top, left + w, top + h))
        photo = ImageTk.PhotoImage(img)
        bg_image_ref["photo"] = photo
        bg_image_ref["label"].configure(image=photo)
        bg_image_ref["label"].image = photo
    except Exception:
        pass


def _show_static_background(image_path):
    """无 PIL 时：tkinter 原生加载 PNG 原图，居中显示（不缩放）。"""
    try:
        photo = tkinter.PhotoImage(file=image_path)
    except Exception:
        return
    label = tkinter.Label(main_window, image=photo, bg=COLORS["bg"])
    label.place(x=0, y=0, relwidth=1, relheight=1)
    label.image = photo


def load_background_image():
    image_path = get_resource_path("background.png")
    if not os.path.exists(image_path):
        return
    try:
        from PIL import Image
    except Exception:
        _show_static_background(image_path)
        return
    try:
        bg_image_ref["pil"] = Image.open(image_path).convert("RGB")
    except Exception:
        _show_static_background(image_path)
        return
    label = tkinter.Label(main_window, bg=COLORS["bg"])
    label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_image_ref["label"] = label
    main_window.bind("<Configure>", _background_resize)
    _background_resize()


# ---------------------------------------------------------------- 圆角卡片
def draw_rounded_box(canvas, x1, y1, x2, y2, radius, fill, outline, width=2, tag=None):
    radius = max(0, min(radius, (x2 - x1) / 2, (y2 - y1) / 2))
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    opts = {"fill": fill, "outline": outline, "width": width, "smooth": True, "joinstyle": "round"}
    if tag:
        opts["tags"] = tag
    canvas.create_polygon(points, **opts)


def create_text_card(parent, text_kwargs):
    """创建可随窗口缩放的圆角文本卡片，返回 (canvas, text)。"""
    canvas = tkinter.Canvas(parent, bg=COLORS["bg"], highlightthickness=0, bd=0)
    text = tkinter.Text(
        canvas,
        relief="flat",
        bd=0,
        padx=14,
        pady=10,
        wrap="word",
        **text_kwargs,
    )
    win_id = canvas.create_window(20, 20, anchor="nw", window=text)

    def redraw(event):
        w, h = event.width, event.height
        if w < 40 or h < 40:
            return
        canvas.delete("card")
        draw_rounded_box(canvas, 1, 1, w - 1, h - 1, 18, COLORS["card"], COLORS["border"], 2, tag="card")
        canvas.itemconfigure(win_id, width=w - 40, height=h - 40)

    canvas.bind("<Configure>", redraw)
    return canvas, text


# ---------------------------------------------------------------- 按钮
def make_button(parent, text, command, primary=False):
    btn = tkinter.Button(
        parent,
        text=text,
        command=command,
        bg=COLORS["accent"] if primary else COLORS["btn_bg"],
        fg="#ffffff" if primary else COLORS["btn_fg"],
        activebackground=COLORS["accent_active"] if primary else COLORS["btn_active"],
        activeforeground="#ffffff",
        bd=0,
        relief="flat",
        padx=16,
        pady=8,
        font=FONT_UI_BOLD,
        cursor="hand2",
        takefocus=False,
    )

    def on_enter(_):
        if str(btn["state"]) == "disabled":
            return
        btn.config(bg=COLORS["accent_hover"] if primary else COLORS["btn_hover"])

    def on_leave(_):
        if str(btn["state"]) == "disabled":
            return
        btn.config(bg=COLORS["accent"] if primary else COLORS["btn_bg"])

    def on_press(_):
        if str(btn["state"]) == "disabled":
            return
        btn.config(bg=COLORS["accent_active"] if primary else COLORS["btn_active"])

    def on_release(e):
        # 仅在鼠标仍停留在按钮内时恢复 hover 色，避免拖出后颜色残留
        if str(btn["state"]) == "disabled":
            return
        try:
            inside = 0 <= e.x <= btn.winfo_width() and 0 <= e.y <= btn.winfo_height()
        except Exception:
            # 无法获取尺寸时直接恢复默认色
            btn.config(bg=COLORS["accent"] if primary else COLORS["btn_bg"])
            return
        if inside:
            on_enter(e)
        else:
            on_leave(e)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)
    return btn


# 背景图须在其他控件创建之前加载，保证位于最底层
load_background_image()


# ---------------------------------------------------------------- 状态栏
status_bar = tkinter.Frame(main_window, bg=COLORS["panel"], bd=0, highlightthickness=0)
status_bar.pack(fill="x", side="bottom")

run_hint_label = tkinter.Label(
    status_bar, text="", bg=COLORS["panel"], fg=COLORS["text_dim"], font=FONT_UI
)
run_hint_label.pack(side="right", padx=16, pady=6)

watermark = tkinter.Label(
    status_bar, text="VMO Developed", bg=COLORS["panel"], fg=COLORS["text_dim"], font=FONT_UI_BOLD
)
watermark.pack(side="right", pady=6)

stats_label = tkinter.Label(
    status_bar, text="", bg=COLORS["panel"], fg=COLORS["text_dim"], font=FONT_UI, anchor="w"
)
stats_label.pack(side="left", padx=16, pady=6)

# ---------------------------------------------------------------- 工具栏
toolbar_frame = tkinter.Frame(main_window, bg=COLORS["panel"], bd=0, highlightthickness=0)
toolbar_frame.pack(fill="x", padx=20, pady=(12, 0))

toolbar_header_frame = tkinter.Frame(toolbar_frame, bg=COLORS["panel"], bd=0, highlightthickness=0)
toolbar_header_frame.pack(fill="x", padx=0, pady=(0, 6))

toolbar_title_label = tkinter.Label(
    toolbar_header_frame,
    text="工具栏",
    fg=COLORS["text"],
    bg=COLORS["panel"],
    font=FONT_TITLE,
)
toolbar_title_label.pack(side="left", padx=(0, 12))

toolbar_toggle_button = tkinter.Button(
    toolbar_header_frame,
    text="展开工具栏",
    command=lambda: None,
    bg=COLORS["btn_bg"],
    fg=COLORS["btn_fg"],
    activebackground=COLORS["btn_active"],
    activeforeground=COLORS["text"],
    bd=0,
    relief="flat",
    padx=10,
    pady=4,
    font=FONT_UI_BOLD,
    cursor="hand2",
    takefocus=False,
)
toolbar_toggle_button.pack(side="right")

toolbar_content_frame = tkinter.Frame(toolbar_frame, bg=COLORS["panel"], bd=0, highlightthickness=0)

language_var = tkinter.StringVar(value="中文")

language_label = tkinter.Label(
    toolbar_content_frame,
    text="语言",
    fg=COLORS["text"],
    bg=COLORS["panel"],
    font=FONT_UI,
)
language_label.pack(side="left", padx=(0, 6))

language_menu = tkinter.OptionMenu(toolbar_content_frame, language_var, *LANGUAGES)
language_menu.config(
    bg=COLORS["btn_bg"],
    fg=COLORS["text"],
    activebackground=COLORS["accent"],
    activeforeground="#ffffff",
    bd=0,
    highlightthickness=0,
    font=FONT_UI,
    cursor="hand2",
)
language_menu["menu"].config(
    bg=COLORS["card"],
    fg=COLORS["text"],
    activebackground=COLORS["accent"],
    activeforeground="#ffffff",
    bd=0,
    font=FONT_UI,
)
language_menu.pack(side="left")

# ---------------------------------------------------------------- 主内容区
content_frame = tkinter.Frame(main_window, bg=COLORS["bg"], bd=0, highlightthickness=0)
content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

content_frame.columnconfigure(0, weight=1)
content_frame.rowconfigure(1, weight=3)
content_frame.rowconfigure(3, weight=2)

input_label = tkinter.Label(
    content_frame,
    text="输入框",
    fg=COLORS["text"],
    bg=COLORS["bg"],
    font=FONT_TITLE,
    anchor="w",
)
input_label.grid(row=0, column=0, sticky="w", padx=4, pady=(14, 6))

input_canvas, input_box = create_text_card(
    content_frame,
    {
        "width": 60,
        "height": 8,
        "font": FONT_CODE,
        "fg": COLORS["field_fg"],
        "bg": COLORS["field_bg"],
        "insertbackground": COLORS["field_fg"],
        "selectbackground": "#cbd5e1",
        "selectforeground": COLORS["field_fg"],
    },
)
input_canvas.grid(row=1, column=0, sticky="nsew", padx=4)

output_label = tkinter.Label(
    content_frame,
    text="输出框",
    fg=COLORS["text"],
    bg=COLORS["bg"],
    font=FONT_TITLE,
    anchor="w",
)
output_label.grid(row=2, column=0, sticky="w", padx=4, pady=(10, 6))

output_canvas, output_text = create_text_card(
    content_frame,
    {
        "width": 60,
        "height": 6,
        "font": FONT_UI,
        "fg": COLORS["field_fg"],
        "bg": COLORS["field_bg"],
        "state": "disabled",
    },
)
output_canvas.grid(row=3, column=0, sticky="nsew", padx=4)

button_frame = tkinter.Frame(content_frame, bg=COLORS["bg"])
button_frame.grid(row=4, column=0, pady=(12, 4))

# ---------------------------------------------------------------- 逻辑函数
def set_output_text(text):
    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", text)
    output_text.config(state="disabled")
    output_text.see("1.0")


def get_input_text():
    return input_box.get("1.0", "end-1c")


def run_searching_blanks():
    set_output_text(searching_blanks.searching_blanks(get_input_text()))


def run_special_chinese_chars():
    set_output_text(specialchinesechara.specialchinesechara(get_input_text()))


def run_language_detection():
    text = get_input_text()
    suspicious_groups = language_utils.collect_suspicious_characters(text)
    translations = language_utils.load_translations(language_var.get())
    if suspicious_groups:
        lines = [translations.get("detect_found", "Detected potentially confusing characters:")]
        for language, chars in sorted(suspicious_groups.items(), key=lambda item: len(item[1]), reverse=True):
            unique_chars = "".join(dict.fromkeys(chars))
            lines.append(f"- {language}: {unique_chars}")
        result = "\n".join(lines)
    else:
        result = translations.get("detect_none", "No potentially confusing characters detected.")
    set_output_text(result)


_copy_hint_job = None


def copy_output():
    global _copy_hint_job
    content = output_text.get("1.0", "end-1c")
    if not content:
        return
    main_window.clipboard_clear()
    main_window.clipboard_append(content)
    translations = language_utils.load_translations(language_var.get())
    stats_label.config(text=translations.get("copied", "Copied"))
    if _copy_hint_job is not None:
        try:
            main_window.after_cancel(_copy_hint_job)
        except Exception:
            pass
    _copy_hint_job = main_window.after(1500, update_stats)


def clear_input():
    input_box.delete("1.0", "end")
    update_stats()
    input_box.focus_set()


def update_stats():
    content = input_box.get("1.0", "end-1c")
    char_count = len(content)
    line_count = content.count("\n") + 1 if content else 0
    translations = language_utils.load_translations(language_var.get())
    stats_label.config(
        text="{}: {}    {}: {}".format(
            translations.get("stats_chars", "Characters"),
            char_count,
            translations.get("stats_lines", "Lines"),
            line_count,
        )
    )


# ---------------------------------------------------------------- 按钮行
search_button = make_button(button_frame, "查找代码空格", run_searching_blanks, primary=True)
search_button.pack(side="left", padx=6)

special_button = make_button(button_frame, "查找特殊中文字符", run_special_chinese_chars)
special_button.pack(side="left", padx=6)

detect_language_button = make_button(button_frame, "判断不同语言特殊字符", run_language_detection)
detect_language_button.pack(side="left", padx=6)

clear_button = make_button(button_frame, "清空输入", clear_input)
clear_button.pack(side="left", padx=6)

copy_button = make_button(button_frame, "复制结果", copy_output)
copy_button.pack(side="left", padx=6)

# ---------------------------------------------------------------- 语言切换 / 快捷键
toolbar_expanded = False


def apply_language():
    translations = language_utils.load_translations(language_var.get())
    main_window.title(translations.get("title", "Gramcher GUI"))
    toolbar_title_label.config(text=translations.get("toolbar_title", "Toolbar"))
    toolbar_toggle_button.config(
        text=translations.get("collapse" if toolbar_expanded else "expand", "Collapse Toolbar")
    )
    language_label.config(text=translations.get("language", "Language"))
    input_label.config(text=translations.get("input", "Input Box"))
    output_label.config(text=translations.get("output", "Output Box"))
    search_button.config(text=translations.get("search_blanks", "Find Code Whitespace"))
    special_button.config(text=translations.get("special_chars", "Find Special Chinese Characters"))
    detect_language_button.config(text=translations.get("detect_language", "Detect Language"))
    clear_button.config(text=translations.get("clear_input", "Clear Input"))
    copy_button.config(text=translations.get("copy_result", "Copy Result"))
    run_hint_label.config(text=translations.get("run_hint", "Run with Ctrl+Enter"))
    watermark.config(text=translations.get("watermark", "VMO Developed"))
    update_stats()


def toggle_toolbar():
    global toolbar_expanded
    if toolbar_expanded:
        toolbar_content_frame.pack_forget()
        toolbar_expanded = False
    else:
        toolbar_content_frame.pack(fill="x", padx=0, pady=(0, 8))
        toolbar_expanded = True
    apply_language()


toolbar_toggle_button.config(command=toggle_toolbar)
language_var.trace_add("write", lambda *_: apply_language())
# 返回 "break" 阻止 Text 默认行为，避免 Ctrl+Enter 时往输入框插入换行
input_box.bind("<Control-Return>", lambda _: run_searching_blanks() or "break")
input_box.bind("<Control-KP_Enter>", lambda _: run_searching_blanks() or "break")
input_box.bind("<KeyRelease>", lambda _: update_stats())
input_box.bind("<ButtonRelease-1>", lambda _: update_stats())

toolbar_content_frame.pack_forget()
apply_language()

main_window.mainloop()
