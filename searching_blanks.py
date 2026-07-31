def is_perfect_code(text):
    cleaned = text.rstrip("\n\r")
    if not cleaned.strip():
        return False
    has_space = any(ch in " \t" for ch in cleaned)
    has_chinese = any(0x4E00 <= ord(ch) <= 0x9FFF for ch in cleaned)
    return not has_space and not has_chinese


def searching_blanks(aa):
    text = aa.rstrip("\n\r")
    if not text.strip():
        return "请输入内容"
    if is_perfect_code(text):
        return "这是个完美的代码"

    Base1 = []
    flag = False
    quote_char = None
    line_start = True
    line = 1
    col = 1

    keywords = {
        'import', 'from', 'def', 'class', 'return', 'if', 'elif',
        'else', 'for', 'while', 'with', 'try', 'except', 'finally',
        'pass', 'break', 'continue', 'raise', 'yield', 'assert',
        'global', 'nonlocal', 'as', 'and', 'or', 'not'
    }
    punctuation = '.,:;()[]{}+-*/%<>=!&|^~,?'

    def get_prev_token(index):
        j = index - 1
        while j >= 0 and (aa[j].isalnum() or aa[j] in '._'):
            j -= 1
        return aa[j + 1:index]

    for i, ch in enumerate(text):
        if ch in ('"', "'"):
            if flag and ch == quote_char:
                flag = False
                quote_char = None
            elif not flag:
                flag = True
                quote_char = ch
            col += 1
            continue

        if flag:
            if ch == '\n':
                line_start = True
                line += 1
                col = 1
            elif ch == '\r':
                line_start = True
                col = 1
            else:
                line_start = False
                col += 1
            continue

        if ch == '\n':
            line_start = True
            line += 1
            col = 1
            continue
        if ch == '\r':
            line_start = True
            col = 1
            continue

        if ch in (' ', '\t'):
            if line_start:
                col += 1
                continue
            if i > 0 and text[i - 1] in '\n\r':
                col += 1
                continue
            if i + 1 < len(text) and text[i + 1] in '\n\r':
                col += 1
                continue

            prev_token = get_prev_token(i)
            prev_char = text[i - 1] if i > 0 else ''
            next_char = text[i + 1] if i + 1 < len(text) else ''

            if prev_token in keywords:
                col += 1
                continue
            if prev_char == '=' or next_char == '=':
                col += 1
                continue
            if prev_char in punctuation or next_char in punctuation:
                col += 1
                continue

            Base1.append((line, col))
            col += 1
            continue

        line_start = False
        col += 1

    return "空格位置为: " + str(Base1)