def is_perfect_code(text):
    cleaned = text.rstrip("\n\r")
    if not cleaned.strip():
        return False
    has_space = any(ch in " \t" for ch in cleaned)
    has_chinese = any(0x4E00 <= ord(ch) <= 0x9FFF for ch in cleaned)
    return not has_space and not has_chinese


def specialchinesechara(am):
    text = am.rstrip("\n\r")
    if not text.strip():
        return "请输入内容"
    if is_perfect_code(text):
        return "这是个完美的代码"

    inthearea = False
    Base0 = []
    SPeca = ["（", "）",
             "［", "］", "｛", "｝", "：", "，", "．", "’",
             "＜", "＞", "＝", "－", "＿", "＋", "＊", "／",
             "＼", "？", "！", "“", "”", "＃", "＠", "＆",
             "％", "＄", "＾", "￥", "｜", "｀", "‘"]
    for i in text:
        if i == '"' or i == "'":
            inthearea = not inthearea
            continue
        if inthearea:
            continue
        if ord(i) >= 0x4E00 and ord(i) <= 0x9FFF:
            if i not in Base0:
                Base0.append(i)
        elif i in SPeca:
            if i not in Base0:
                Base0.append(i)
    return "特殊字符有: " + str(Base0)

