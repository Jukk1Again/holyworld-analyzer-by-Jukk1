import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageGrab
import winocr
import re


items_data = []
auto_scanning = False
last_signature = None


def clean_number(s):
    return re.sub(r"\s+", "", s.strip())


def find_name_above(lines, idx):
    for k in range(idx - 1, max(idx - 15, -1), -1):
        candidate = lines[k].strip()
        if not candidate:
            continue
        if candidate.startswith(("-", "–", "•", "▶", "►")):
            continue
        if ":" in candidate:
            continue
        if len(candidate) < 2:
            continue
        return candidate
    return "Неизвестно"


def parse_screen(text):
    lines = [l.strip() for l in text.splitlines()]
    n = len(lines)
    found = []
    i = 0

    while i < n:
        line = lines[i]

        if line.startswith("Продавец:"):
            name = find_name_above(lines, i)
            price = None
            price_per_unit = None
            j = i
            end = min(i + 6, n)
            while j < end:
                l2 = lines[j]
                m1 = re.match(r"Цена за 1 ед\.?:\s*([\d\s]+)", l2)
                m2 = re.match(r"Цена:\s*([\d\s]+)", l2)
                if m1:
                    price_per_unit = clean_number(m1.group(1))
                elif m2:
                    price = clean_number(m2.group(1))
                j += 1
            found.append({
                "name": name,
                "type": "Аукцион",
                "price": price or "-",
                "extra": f"За ед.: {price_per_unit}" if price_per_unit else "-",
            })
            i = j
            continue

        if line.startswith("Сдали мало:") or line.startswith("Базовый коэффициент:"):
            name = find_name_above(lines, i)
            standard_price = None
            current_price = None
            j = i
            end = min(i + 8, n)
            while j < end:
                l2 = lines[j]
                m1 = re.match(r"Стандартная цена:\s*([\d\s]+)", l2)
                m2 = re.match(r"Текущая цена:\s*([\d\s]+)", l2)
                if m1:
                    standard_price = clean_number(m1.group(1))
                if m2:
                    current_price = clean_number(m2.group(1))
                j += 1
            found.append({
                "name": name,
                "type": "Скупщик",
                "price": current_price or standard_price or "-",
                "extra": f"Станд.: {standard_price}" if standard_price else "-",
            })
            i = j
            continue

        i += 1

    return found


def add_items(found):
    global last_signature
    for item in found:
        signature = (item["name"], item["type"], item["price"], item["extra"])
        if signature == last_signature:
            continue
        last_signature = signature
        items_data.append(item)
        tree.insert("", "end", values=(item["name"], item["type"], item["price"], item["extra"]))
        tree.yview_moveto(1)


def scan_once(show_empty_message=True):
    try:
        image = ImageGrab.grab()
        result = winocr.recognize_pil_sync(image, lang="ru-RU")
        text = result["text"]
        found = parse_screen(text)

        if found:
            add_items(found)
        elif
