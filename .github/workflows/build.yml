import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import winocr


def screenshot():
    try:
        image = ImageGrab.grab()

        result = winocr.recognize_pil_sync(image, lang="ru-RU")
        text = result.text.strip()

        if not text:
            result = winocr.recognize_pil_sync(image, lang="en-US")
            text = result.text.strip()

        if not text:
            text = "Текст на экране не найден."

        messagebox.showinfo("Результат анализа", text)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


root = tk.Tk()
root.title("HolyWorld Analyzer")
root.geometry("450x300")

tk.Label(
    root,
    text="HolyWorld Analyzer",
    font=("Arial", 18, "bold")
).pack(pady=30)

tk.Button(
    root,
    text="Сканировать экран",
    command=screenshot,
    width=25,
    height=2
).pack()

root.mainloop()
