import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def analyze():
    messagebox.showinfo(
        "HolyWorld Analyzer",
        "Анализ готов.\n\n"
        "Пока данных нет — следующим шагом добавим "
        "анализ цен, ЗСП, яиц и Скупщика."
    )

root = tk.Tk()
root.title("HolyWorld Analyzer")
root.geometry("400x250")

title = tk.Label(
    root,
    text="HolyWorld Analyzer",
    font=("Arial", 18, "bold")
)
title.pack(pady=25)

button = tk.Button(
    root,
    text="Провести анализ",
    command=analyze,
    width=25,
    height=2
)
button.pack()

time_label = tk.Label(root, text="")
time_label.pack(pady=20)

def update_time():
    time_label.config(
        text="Последнее открытие: " +
             datetime.now().strftime("%H:%M:%S")
    )
    root.after(1000, update_time)

update_time()
root.mainloop()
