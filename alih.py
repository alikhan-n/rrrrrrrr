import csv
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class CourseRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Регистрация на учебные курсы")
        self.root.geometry("1050x820")
        self.root.minsize(650, 500)
        self.root.configure(bg="#f2f5f9")
        self.students = []
        self.next_id = 1
        self.make_variables()
        self.make_styles()
        self.make_interface()
        self.refresh_table()

    def make_variables(self):
        self.full_name = tk.StringVar()
        self.age = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.school = tk.StringVar()
        self.course = tk.StringVar()
        self.study = tk.StringVar()
        self.certificate = tk.BooleanVar()
        self.videos = tk.BooleanVar()
        self.practice = tk.BooleanVar()
        self.search = tk.StringVar()

    def make_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#f2f5f9")
        style.configure("TLabelframe", background="white", padding=9)
        style.configure("TLabelframe.Label", background="white",
                        foreground="#24364b", font=("Arial", 10, "bold"))
        style.configure("TLabel", background="white", font=("Arial", 9))
        style.configure("Treeview", rowheight=25, font=("Arial", 9))
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))

    def make_interface(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="Регистрация на учебные курсы",
                 bg="#f2f5f9", fg="#20344d",
                 font=("Arial", 19, "bold")).pack(anchor="w", pady=(0, 10))

        upper = ttk.Frame(main)
        upper.pack(fill="x")
        upper.columnconfigure(0, weight=3)
        upper.columnconfigure(1, weight=2)
        personal = ttk.LabelFrame(upper, text="Данные студента")
        personal.grid(row=0, column=0, sticky="nsew", padx=(0, 7), pady=4)
        options = ttk.LabelFrame(upper, text="Параметры обучения")
        options.grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=4)

        self.add_entry(personal, "Фамилия, имя и отчество:", self.full_name, 0)
        self.add_entry(personal, "Возраст:", self.age, 1)
        self.add_entry(personal, "Номер телефона:", self.phone, 2)
        self.add_entry(personal, "Электронная почта:", self.email, 3)
        self.add_entry(personal, "Учебное заведение:", self.school, 4)

        ttk.Label(options, text="Учебный курс:").grid(row=0, column=0, sticky="w", pady=3)
        courses = ["Основы Python", "Разработка приложений в Tkinter",
                   "Веб-разработка", "Работа с базами данных",
                   "Компьютерная графика"]
        ttk.Combobox(options, textvariable=self.course, values=courses,
                     state="readonly", width=30).grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(options, text="Форма обучения:").grid(row=2, column=0, sticky="w")
        for i, value in enumerate(("Очное обучение", "Дистанционное обучение", "Смешанный формат")):
            ttk.Radiobutton(options, text=value, variable=self.study,
                            value=value).grid(row=3+i, column=0, sticky="w", pady=2)
        ttk.Label(options, text="Дополнительные возможности:").grid(row=6, column=0, sticky="w", pady=(8, 2))
        ttk.Checkbutton(options, text="Получение сертификата",
                        variable=self.certificate).grid(row=7, column=0, sticky="w")
        ttk.Checkbutton(options, text="Доступ к видеозаписям",
                        variable=self.videos).grid(row=8, column=0, sticky="w")
        ttk.Checkbutton(options, text="Дополнительные практические занятия",
                        variable=self.practice).grid(row=9, column=0, sticky="w")

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="Зарегистрироваться",
                   command=self.register).pack(side="left", padx=(0, 5))
        ttk.Button(buttons, text="Очистить форму",
                   command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(buttons, text="Сохранить в файл",
                   command=self.save_csv).pack(side="left", padx=5)
        ttk.Button(buttons, text="Закрыть программу",
                   command=self.close).pack(side="right")

        table_box = ttk.LabelFrame(main, text="Зарегистрированные студенты")
        table_box.pack(fill="both", expand=True, pady=(4, 0))
        search_row = ttk.Frame(table_box)
        search_row.pack(fill="x", pady=(0, 7))
        ttk.Label(search_row, text="Поиск по Ф. И. О. или курсу:").pack(side="left", padx=(0, 6))
        ttk.Entry(search_row, textvariable=self.search).pack(side="left", fill="x", expand=True)
        ttk.Button(search_row, text="Сбросить",
                   command=lambda: self.search.set("")).pack(side="left", padx=6)
        self.search.trace_add("write", lambda *_: self.refresh_table())

        columns = ("name", "age", "course", "study", "phone")
        self.tree = ttk.Treeview(table_box, columns=columns, show="headings", height=8)
        for col, heading, width in [
            ("name", "Ф. И. О.", 190), ("age", "Возраст", 65),
            ("course", "Курс", 220), ("study", "Форма обучения", 150),
            ("phone", "Телефон", 130)
        ]:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, minwidth=60)
        ybar = ttk.Scrollbar(table_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ybar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ybar.pack(side="right", fill="y")

        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=(7, 0))
        ttk.Button(bottom, text="Показать подробности",
                   command=self.details).pack(side="left", padx=(0, 5))
        ttk.Button(bottom, text="Удалить выбранную запись",
                   command=self.delete).pack(side="left", padx=5)
        self.status = tk.Label(main, text="Зарегистрировано студентов: 0",
                               bg="#f2f5f9", fg="#526579", anchor="w")
        self.status.pack(fill="x", pady=(6, 0))

    def add_entry(self, parent, label, variable, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(2, 8), pady=5)
        ttk.Entry(parent, textvariable=variable, width=34).grid(
            row=row, column=1, sticky="ew", padx=2, pady=5)
        parent.columnconfigure(1, weight=1)

    def validate(self):
        name, age_text = self.full_name.get().strip(), self.age.get().strip()
        phone, email = self.phone.get().strip(), self.email.get().strip()
        school, course, study = self.school.get().strip(), self.course.get().strip(), self.study.get().strip()
        if not all((name, age_text, phone, email, school)):
            messagebox.showerror("Ошибка ввода", "Заполните все обязательные поля.")
            return None
        try:
            age = int(age_text)
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Возраст должен быть целым числом.")
            return None
        if not 14 <= age <= 80:
            messagebox.showerror("Ошибка ввода", "Возраст должен быть от 14 до 80 лет.")
            return None
        if not re.fullmatch(r"\+?\d+", phone):
            messagebox.showerror("Ошибка ввода", "Телефон должен содержать только цифры и необязательный + в начале.")
            return None
        if "@" not in email or "." not in email:
            messagebox.showerror("Ошибка ввода", "Email должен содержать символы @ и .")
            return None
        if not course:
            messagebox.showerror("Ошибка ввода", "Выберите учебный курс.")
            return None
        if not study:
            messagebox.showerror("Ошибка ввода", "Выберите форму обучения.")
            return None
        extras = []
        if self.certificate.get():
            extras.append("Получение сертификата")
        if self.videos.get():
            extras.append("Доступ к видеозаписям")
        if self.practice.get():
            extras.append("Дополнительные практические занятия")
        return {
            "id": self.next_id, "name": name, "age": age, "phone": phone,
            "email": email, "school": school, "course": course, "study": study,
            "extras": extras, "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

    def register(self):
        student = self.validate()
        if student is None:
            return
        self.students.append(student)
        self.next_id += 1
        self.refresh_table()
        extras = ", ".join(student["extras"]) if student["extras"] else "Не выбраны"
        messagebox.showinfo(
            "Регистрация успешна",
            f'Студент {student["name"]} зарегистрирован!\n'
            f'Курс: {student["course"]}\nФорма: {student["study"]}\n'
            f'Дополнительные возможности: {extras}'
        )
        self.clear_form()

    def refresh_table(self):
        if not hasattr(self, "tree"):
            return
        query = self.search.get().strip().casefold()
        self.tree.delete(*self.tree.get_children())
        shown = 0
        for s in self.students:
            if query and query not in s["name"].casefold() and query not in s["course"].casefold():
                continue
            self.tree.insert("", "end", iid=str(s["id"]),
                             values=(s["name"], s["age"], s["course"], s["study"], s["phone"]))
            shown += 1
        self.status.config(text=f"Всего зарегистрировано: {len(self.students)} | Показано: {shown}")

    def selected_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Запись не выбрана", "Сначала выберите студента в таблице.")
            return None
        student_id = int(selected[0])
        return next((s for s in self.students if s["id"] == student_id), None)

    def details(self):
        s = self.selected_student()
        if not s:
            return
        extras = "\n".join("• " + x for x in s["extras"]) if s["extras"] else "Не выбраны"
        messagebox.showinfo("Подробности регистрации",
            f'Ф. И. О.: {s["name"]}\nВозраст: {s["age"]}\nТелефон: {s["phone"]}\n'
            f'Email: {s["email"]}\nУчебное заведение: {s["school"]}\n'
            f'Курс: {s["course"]}\nФорма обучения: {s["study"]}\n'
            f'Дополнительные возможности:\n{extras}\nДата регистрации: {s["date"]}')

    def delete(self):
        s = self.selected_student()
        if not s:
            return
        if messagebox.askyesno("Подтверждение", f'Удалить запись «{s["name"]}»?'):
            self.students.remove(s)
            self.refresh_table()

    def clear_form(self):
        for variable in (self.full_name, self.age, self.phone, self.email,
                         self.school, self.course, self.study):
            variable.set("")
        self.certificate.set(False)
        self.videos.set(False)
        self.practice.set(False)

    def save_csv(self):
        if not self.students:
            messagebox.showwarning("Нет данных", "Список студентов пока пуст.")
            return
        filename = filedialog.asksaveasfilename(
            title="Сохранить список студентов", defaultextension=".csv",
            filetypes=[("CSV-файл", "*.csv"), ("Все файлы", "*.*")],
            initialfile="students_registration.csv")
        if not filename:
            return
        try:
            with open(filename, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Ф. И. О.", "Возраст", "Телефон", "Электронная почта",
                                 "Учебное заведение", "Курс", "Форма обучения",
                                 "Дополнительные возможности", "Дата регистрации"])
                for s in self.students:
                    writer.writerow([s["name"], s["age"], s["phone"], s["email"],
                                     s["school"], s["course"], s["study"],
                                     ", ".join(s["extras"]), s["date"]])
            messagebox.showinfo("Сохранение", f"Данные сохранены:\n{filename}")
        except (OSError, csv.Error) as error:
            messagebox.showerror("Ошибка сохранения", str(error))

    def close(self):
        if messagebox.askyesno("Выход", "Закрыть программу?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseRegistrationApp(root)
    root.mainloop()
