import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(BASE_DIR, relative_path)
LANGUAGE_FILES = {
    "中文": "zh_CN.json",
    "English": "en_US.json",
    "日本語": "ja_JP.json",
    "Français": "fr_FR.json",
    "हिन्दी": "hi_IN.json",
    "Русский": "ru_RU.json",
}


def load_translations(language_name):
    file_name = LANGUAGE_FILES.get(language_name, "zh_CN.json")
    file_path = get_resource_path(file_name)
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_suspicious_characters(text):
    if not text:
        return {}

    text = text.strip()
    if not text:
        return {}

    suspicious_groups = {
        "中文": [],
        "日本語": [],
        "Русский": [],
        "हिन्दी": [],
        "Français": [],
        "English": [],
    }

    chinese_chars = "，。！？；：、（）【】《》“”‘’…—・"
    japanese_chars = "「」・゛゜"
    russian_chars = "«»—…"
    hindi_chars = "。॥॰"
    french_chars = "«»œæŒÆÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸàâäçéèêëîïôöùûüÿ"

    for ch in text:
        if '一' <= ch <= '鿿' or ch in chinese_chars:
            suspicious_groups["中文"].append(ch)
        elif '぀' <= ch <= 'ヿ' or ch in japanese_chars:
            suspicious_groups["日本語"].append(ch)
        elif 'Ѐ' <= ch <= 'ӿ' or ch in russian_chars:
            suspicious_groups["Русский"].append(ch)
        elif 'ऀ' <= ch <= 'ॿ' or ch in hindi_chars:
            suspicious_groups["हिन्दी"].append(ch)
        elif ch in french_chars or ch in "éèêàçùœæÉÈÊÀÇÙŒÆ":
            suspicious_groups["Français"].append(ch)
        elif ch.isalpha():
            suspicious_groups["English"].append(ch)

    return {language: chars for language, chars in suspicious_groups.items() if chars}


def detect_language(text):
    if not text:
        return "中文"

    text = text.strip()
    if not text:
        return "中文"

    groups = collect_suspicious_characters(text)
    if not groups:
        return "中文"

    best_language = max(groups.items(), key=lambda item: len(item[1]))[0]
    return best_language
