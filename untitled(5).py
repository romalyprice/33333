import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Основное окно
root = tk.Tk()
root.title("Training Planner")
root.geometry("800x600")

# Переменные для ввода
date_var = tk.StringVar()
type_var = tk.StringVar()
duration_var = tk.StringVar()

# Ввод формы
tk.Label(root, text="Дата (ДД-ММ-ГГГГ)").grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=date_var, width=15).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Тип тренировки").grid(row=1, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=type_var, width=20).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Длительность (мин)").grid(row=2, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=duration_var, width=10).grid(row=2, column=1, padx=5, pady=5)

# Таблица
columns = ("Дата", "Тип", "Длительность")
tree = ttk.Treeview(root, columns=columns, show='headings', height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)
tree.grid(row=8, column=0, columnspan=4, padx=5, pady=10)

# Хранение данных
trainings = []

def clear_fields():
    date_var.set("")
    type_var.set("")
    duration_var.set("")

def add_training():
    date_str = date_var.get().strip()
    t_type = type_var.get().strip()
    duration_str = duration_var.get().strip()

    # Вводная проверка
    # Проверка формата даты
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ДД-ММ-ГГГГ.")
        return

    # Проверка длительности
    if not duration_str.isdigit() or int(duration_str) <= 0:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
        return

    # Проверка пустых полей
    if not date_str or not t_type or not duration_str:
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения.")
        return

    duration = int(duration_str)
    training = {
        "Дата": date_str,
        "Тип": t_type,
        "Длительность": duration
    }
    trainings.append(training)
    tree.insert('', tk.END, values=(date_str, t_type, duration))
    clear_fields()

# Кнопка добавления
tk.Button(root, text="Добавить тренировку", command=add_training).grid(row=3, column=0, padx=5, pady=10)

# --- Фильтры ---
filter_type_var = tk.StringVar()
filter_date_var = tk.StringVar()

tk.Label(root, text="Фильтр по типу").grid(row=4, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=filter_type_var, width=20).grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по дате (ДД-ММ-ГГГГ)").grid(row=5, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=filter_date_var, width=15).grid(row=5, column=1, padx=5, pady=5)

def apply_filter():
    filter_type = filter_type_var.get().lower()
    filter_date_str = filter_date_var.get().strip()

    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)

    for training in trainings:
        # по типу
        if filter_type and filter_type not in training["Тип"].lower():
            continue
        # по дате
        if filter_date_str:
            try:
                filter_date_obj = datetime.strptime(filter_date_str, "%d-%m-%Y")
                training_date_obj = datetime.strptime(training["Дата"], "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты фильтра.")
                return
            if training_date_obj != filter_date_obj:
                continue
        # вывод
        tree.insert('', tk.END, values=(
            training["Дата"],
            training["Тип"],
            training["Длительность"]
        ))

def reset_filter():
    filter_type_var.set("")
    filter_date_var.set("")
    # заново выводим все
    for item in tree.get_children():
        tree.delete(item)
    for training in trainings:
        tree.insert('', tk.END, values=(
            training["Дата"],
            training["Тип"],
            training["Длительность"]
        ))

tk.Button(root, text="Применить фильтр", command=apply_filter).grid(row=6, column=0, padx=5, pady=10)
tk.Button(root, text="Сбросить фильтр", command=reset_filter).grid(row=6, column=1, padx=5, pady=10)

# --- Сохранение/Загрузка ---
DATA_FILE = "trainings.json"

def save_data():
    try:
        with open(DATA_FILE, "w", encoding='utf-8') as f:
            json.dump(trainings, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding='utf-8') as f:
                loaded = json.load(f)
            for training in loaded:
                trainings.append(training)
                tree.insert('', tk.END, values=(
                    training["Дата"],
                    training["Тип"],
                    training["Длительность"]
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {e}")

load_data()

tk.Button(root, text="Сохранить в JSON", command=save_data).grid(row=7, column=0, padx=5, pady=10)

# Запуск
root.mainloop()