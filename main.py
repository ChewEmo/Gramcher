import os
import sys
import tkinter
import searching_blanks
import specialchinesechara
import language_utils

main_window = tkinter.Tk()
main_window.title("Gramcher GUI")
main_window.geometry("1024x768")
main_window.configure(bg="#0f172a")
try:
    main_window.iconbitmap(get_resource_path("tubiao.ico"))
except Exception:
    pass

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(base_dir, relative_path)


def load_background_image():
    image_path = get_resource_path("background.png")
    if not os.path.exists(image_path):
        return None
    try:
        return tkinter.PhotoImage(file=image_path)
    except Exception:
        try:
            from PIL import Image, ImageTk
            return ImageTk.PhotoImage(Image.open(image_path))
        except Exception:
            return None


def draw_rounded_box(canvas, x1, y1, x2, y2, radius, fill, outline, width=2):
    radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)
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
    canvas.create_polygon(points, fill=fill, outline=outline, width=width, smooth=True, joinstyle="round")
    canvas.create_polygon(points, fill="", outline="#ffffff", width=2, smooth=True, joinstyle="round")


bg_image = load_background_image()
if bg_image is not None:
    bg_label = tkinter.Label(main_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_image


toolbar_frame = tkinter.Frame(main_window, bg="#111827", bd=0, highlightthickness=0)
toolbar_frame.pack(fill="x", padx=20, pady=(12, 0))

toolbar_header_frame = tkinter.Frame(toolbar_frame, bg="#111827", bd=0, highlightthickness=0)
toolbar_header_frame.pack(fill="x", padx=0, pady=(0, 6))

toolbar_title_label = tkinter.Label(
    toolbar_header_frame,
    text="工具栏",
    fg="#f8fafc",
    bg="#111827",
    font=("Arial", 12, "bold"),
)
toolbar_title_label.pack(side="left", padx=(0, 12))

toolbar_toggle_button = tkinter.Button(
    toolbar_header_frame,
    text="展开工具栏",
    command=lambda: None,
    bg="#ffffff",
    fg="#0f172a",
    activebackground="#e2e8f0",
    activeforeground="#0f172a",
    bd=0,
    padx=10,
    pady=4,
    font=("Arial", 10, "bold"),
)
toolbar_toggle_button.pack(side="right")

toolbar_content_frame = tkinter.Frame(toolbar_frame, bg="#111827", bd=0, highlightthickness=0)

language_var = tkinter.StringVar(value="中文")

language_label = tkinter.Label(
    toolbar_content_frame,
    text="语言",
    fg="#e2e8f0",
    bg="#111827",
    font=("Arial", 10),
)
language_label.pack(side="left", padx=(0, 6))

language_menu = tkinter.OptionMenu(
    toolbar_content_frame,
    language_var,
    "中文",
    "English",
    "日本語",
    "Français",
    "हिन्दी",
    "Русский",
)
language_menu.config(
    bg="#ffffff",
    fg="#0f172a",
    activebackground="#e2e8f0",
    activeforeground="#0f172a",
    bd=0,
    highlightthickness=0,
)
language_menu.pack(side="left")

content_frame = tkinter.Frame(main_window, bg="#0f172a", bd=0, highlightthickness=0)
content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

input_label = tkinter.Label(
    content_frame,
    text="输入框",
    fg="#f8fafc",
    bg="#0f172a",
    font=("Arial", 12, "bold"),
    anchor="w",
)
input_label.pack(padx=20, pady=(16, 6), anchor="w")

input_canvas = tkinter.Canvas(content_frame, width=760, height=180, bg="#0f172a", highlightthickness=0)
input_canvas.pack(padx=20, pady=(0, 10))
draw_rounded_box(input_canvas, 0, 0, 760, 180, 24, "#f8fafc", "#ffffff", 1)
input_canvas.create_rectangle(1, 1, 758, 178, outline="#ffffff", width=1, stipple="gray50")

input_box = tkinter.Text(
    input_canvas,
    width=88,
    height=8,
    wrap="word",
    font=("Consolas", 11),
    fg="#0f172a",
    bg="#f8fafc",
    padx=14,
    pady=12,
    relief="flat",
    insertbackground="#0f172a",
    selectbackground="#cbd5e1",
    selectforeground="#0f172a",
)
input_canvas.create_window(20, 20, anchor="nw", window=input_box)

output_label = tkinter.Label(
    content_frame,
    text="输出框",
    fg="#f8fafc",
    bg="#0f172a",
    font=("Arial", 12, "bold"),
    anchor="w",
)
output_label.pack(padx=20, pady=(4, 6), anchor="w")

output_canvas = tkinter.Canvas(content_frame, width=760, height=140, bg="#0f172a", highlightthickness=0)
output_canvas.pack(padx=20, pady=(0, 12))
draw_rounded_box(output_canvas, 0, 0, 760, 140, 24, "#f8fafc", "#ffffff", 1)
output_canvas.create_rectangle(1, 1, 758, 138, outline="#ffffff", width=1, stipple="gray50")

output_text = tkinter.Text(
    output_canvas,
    width=88,
    height=6,
    wrap="word",
    font=("Arial", 11),
    fg="#0f172a",
    bg="#f8fafc",
    padx=14,
    pady=12,
    relief="flat",
    state="disabled",
)
output_canvas.create_window(20, 20, anchor="nw", window=output_text)

button_frame = tkinter.Frame(content_frame, bg="#0f172a")
button_frame.pack(pady=6)


def set_output_text(text):
    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", text)
    output_text.config(state="disabled")


def get_input_text():
    return input_box.get("1.0", "end-1c")


def run_searching_blanks():
    text = get_input_text()
    result = searching_blanks.searching_blanks(text)
    set_output_text(result)


def run_special_chinese_chars():
    text = get_input_text()
    result = specialchinesechara.specialchinesechara(text)
    set_output_text(result)


def run_language_detection():
    text = get_input_text()
    suspicious_groups = language_utils.collect_suspicious_characters(text)
    if suspicious_groups:
        lines = ["检测到容易误判字符："]
        for language, chars in sorted(suspicious_groups.items(), key=lambda item: len(item[1]), reverse=True):
            unique_chars = "".join(dict.fromkeys(chars))
            lines.append(f"- {language}: {unique_chars}")
        result = "\n".join(lines)
    else:
        result = "未检测到容易误判字符。"
    set_output_text(result)


search_button = tkinter.Button(
    button_frame,
    text="查找代码空格",
    command=run_searching_blanks,
    bg="#ffffff",
    fg="#0f172a",
    activebackground="#e2e8f0",
    activeforeground="#0f172a",
    bd=0,
    padx=16,
    pady=8,
    font=("Arial", 11, "bold"),
)
search_button.pack(side="left", padx=8)

special_button = tkinter.Button(
    button_frame,
    text="查找特殊中文字符",
    command=run_special_chinese_chars,
    bg="#ffffff",
    fg="#0f172a",
    activebackground="#e2e8f0",
    activeforeground="#0f172a",
    bd=0,
    padx=16,
    pady=8,
    font=("Arial", 11, "bold"),
)
special_button.pack(side="left", padx=8)

detect_language_button = tkinter.Button(
    button_frame,
    text="判断不同语言特殊字符",
    command=run_language_detection,
    bg="#ffffff",
    fg="#0f172a",
    activebackground="#e2e8f0",
    activeforeground="#0f172a",
    bd=0,
    padx=16,
    pady=8,
    font=("Arial", 11, "bold"),
)
detect_language_button.pack(side="left", padx=8)

watermark = tkinter.Label(
    main_window,
    text="VMO Developed",
    fg="#e2e8f0",
    bg="#0f172a",
    font=("Arial", 11, "bold"),
)
watermark.place(relx=0.98, rely=0.98, anchor="se", x=-12, y=-12)


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
    watermark.config(text=translations.get("watermark", "VMO Developed"))


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

toolbar_expanded = False
toolbar_content_frame.pack_forget()
apply_language()

main_window.mainloop()