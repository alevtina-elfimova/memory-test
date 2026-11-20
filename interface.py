import tkinter as tk
from tkinter import ttk, messagebox

from memory_test import MemoryTest
from results import format_results

class MemoryApp:
    """Главный класс графического приложения"""

    def __init__(self, root):
        """Настройка главного окна приложения"""
        self.root = root
        self.root.title("Тест на память")
        self.root.geometry("700x500")
        self.root.minsize(550, 400)
        self.root.resizable(True, True)
        self.root.configure(bg="#F4F6FA")

        self.test = MemoryTest(max_errors=3)
        self.timer_id = None
        self.answer_entry = None
        self.sequence_label = None
        self.status_label = None
        self.next_button = None
        self.content = None

        self.setup_styles()
        self.create_menu()
        self.show_main_menu()

        # Обработка ошибок, возникших во время работы интерфейса
        self.root.report_callback_exception = (
            self.handle_callback_exception
        )

        # Подтверждение выхода из приложения
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def setup_styles(self):
        """Настройка внешнего вида элементов интерфейса"""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background="#F4F6FA"
        )

        style.configure(
            "TLabel",
            background="#F4F6FA",
            foreground="#263445",
            font=("Arial", 11)
        )

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold"),
            foreground="#2457A6"
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 12),
            foreground="#64748B"
        )

        style.configure(
            "TButton",
            font=("Arial", 11),
            padding=10
        )

        style.configure(
            "Primary.TButton",
            background="#3478D4",
            foreground="white",
            font=("Arial", 11, "bold")
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#2457A6")]
        )

    def create_menu(self):
        """Создание главного меню"""
        menu_bar = tk.Menu(self.root)

        # Раздел "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label="Начать тестирование",
            command=self.start_test
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Выход",
            command=self.close_application
        )
        menu_bar.add_cascade(
            label="Файл",
            menu=file_menu
        )

        # Раздел "Тестирование"
        test_menu = tk.Menu(menu_bar, tearoff=0)
        test_menu.add_command(
            label="Правила тестирования",
            command=self.show_rules
        )
        test_menu.add_command(
            label="Результаты",
            command=self.show_results
        )
        menu_bar.add_cascade(
            label="Тестирование",
            menu=test_menu
        )

        # Раздел "Справка"
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(
            label="О программе",
            command=self.show_about
        )
        menu_bar.add_cascade(
            label="Справка",
            menu=help_menu
        )

        self.root.config(menu=menu_bar)

    def clear_screen(self):
        """Удаление элементов текущего экрана"""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.content is not None:
            self.content.destroy()

        self.content = ttk.Frame(self.root, padding=30)
        self.content.pack(fill="both", expand=True)

    def show_main_menu(self):
        """Отображение главного меню"""
        self.clear_screen()

        ttk.Label(
            self.content,
            text="ТЕСТ НА ПАМЯТЬ",
            style="Title.TLabel"
        ).pack(pady=(50, 15))

        ttk.Label(
            self.content,
            text="Проверь свои способности запоминать числа!",
            style="Subtitle.TLabel"
        ).pack(pady=10)

        ttk.Button(
            self.content,
            text="Начать тестирование",
            style="Primary.TButton",
            command=self.start_test
        ).pack(pady=15, ipadx=25)

        ttk.Button(
            self.content,
            text="Правила тестирования",
            command=self.show_rules
        ).pack(pady=8, ipadx=25)

        ttk.Button(
            self.content,
            text="О программе",
            command=self.show_about
        ).pack(pady=8, ipadx=25)

    def start_test(self):
        """Начало нового тестирования"""
        try:
            self.test.reset()
            self.show_test_screen()
            self.show_sequence()
        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось начать тестирование:\n{error}"
            )

    def show_test_screen(self):
        """Создание экрана прохождения теста"""
        self.clear_screen()

        ttk.Label(
            self.content,
            text="Тестирование памяти",
            style="Title.TLabel"
        ).pack(pady=5)

        self.status_label = ttk.Label(
            self.content,
            text="",
            font=("Arial", 11)
        )
        self.status_label.pack(pady=5)

        self.sequence_label = ttk.Label(
            self.content,
            text="",
            font=("Arial", 32, "bold"),
            foreground="#2457A6"
        )
        self.sequence_label.pack(pady=12)

        self.instruction_label = ttk.Label(
            self.content,
            text="Запомните последовательность чисел",
            style="Subtitle.TLabel"
        )
        self.instruction_label.pack(pady=5)

        self.answer_entry = ttk.Entry(
            self.content,
            font=("Arial", 16),
            justify="center",
            width=20
        )
        self.answer_entry.pack(pady=8)
        self.answer_entry.bind(
            "<Return>",
            lambda event: self.check_answer()
        )

        self.check_button = ttk.Button(
            self.content,
            text="Проверить ответ",
            style="Primary.TButton",
            command=self.check_answer,
            width = 25
        )
        self.check_button.pack(pady=5)

        self.next_button = ttk.Button(
            self.content,
            text="Следующий раунд",
            command=self.show_sequence
        )

        ttk.Button(
            self.content,
            text="В главное меню",
            command=self.show_main_menu
        ).pack(pady=8)

        self.update_status()

    def update_status(self):
        """Обновление информации о текущем тестировании"""
        self.status_label.config(
            text=(
                f"Уровень: {self.test.current_length} | "
                f"Правильных ответов: "
                f"{self.test.correct_answers} | "
                f"Ошибок: {self.test.errors}/"
                f"{self.test.max_errors}"
            )
        )

    def show_sequence(self):
        """Генерация и временное отображение числа в тесте"""
        try:
            if self.test.finished:
                self.show_results()
                return

            self.next_button.pack_forget()
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.pack_forget()
            self.check_button.pack_forget()

            sequence = self.test.generate_sequence()

            self.sequence_label.config(text=sequence)
            self.instruction_label.config(
                text="Запомните последовательность чисел"
            )

            self.update_status()

            # Через 3 секунды последовательность исчезнет.
            self.timer_id = self.root.after(
                3000,
                self.hide_sequence
            )

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при показе числа:\n{error}"
            )

    def hide_sequence(self):
        """Скрытие последовательности и открытие поля ввода"""
        self.timer_id = None

        self.sequence_label.config(text="???")
        self.instruction_label.config(
            text="Введите запомнившуюся последовательность"
        )

        self.answer_entry.pack(pady=15)
        self.check_button.pack(pady=10)
        self.answer_entry.focus_set()

    def check_answer(self):
        """Обработка и проверка ответа пользователя"""
        try:
            answer = self.answer_entry.get().strip()

            if not answer:
                messagebox.showwarning(
                    "Предупреждение",
                    "Введите последовательность чисел."
                )
                return

            if not answer.isdigit() or not answer.isdecimal():
                messagebox.showwarning(
                    "Некорректный ввод",
                    "Ответ должен содержать только цифры от 0 до 9"
                )
                return

            result = self.test.check_answer(answer)

            self.answer_entry.pack_forget()
            self.check_button.pack_forget()
            self.sequence_label.config(text="")

            if result["correct"]:
                self.instruction_label.config(
                    text="Правильно! Вы хорошо запомнили число."
                )
            else:
                self.instruction_label.config(
                    text="Неправильно! Попробуйте ещё раз."
                )

            self.update_status()

            if result["finished"]:
                self.root.after(1200, self.show_results)
            else:
                self.next_button.pack(pady=15)

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось проверить ответ:\n{error}"
            )

    def show_rules(self):
        """Отображение окна с правилами"""
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила тестирования")
        rules_window.geometry("430x330")
        rules_window.resizable(False, False)
        rules_window.transient(self.root)

        ttk.Label(
            rules_window,
            text="Правила тестирования",
            font=("Arial", 17, "bold")
        ).pack(pady=20)

        rules_text = (
            "1. Нажмите кнопку «Начать тестирование».\n\n"
            "2. Запомните появившуюся последовательность цифр.\n\n"
            "3. Через 3 секунды число исчезнет.\n\n"
            "4. Введите запомнившуюся последовательность.\n\n"
            "5. За правильный ответ сложность увеличивается.\n\n"
            "6. После трёх ошибок тестирование завершается."
        )

        ttk.Label(
            rules_window,
            text=rules_text,
            justify="left",
            wraplength=380
        ).pack(padx=20, pady=10)

        ttk.Button(
            rules_window,
            text="Закрыть",
            command=rules_window.destroy
        ).pack(pady=15)

        rules_window.grab_set()

    def show_about(self):
        """Отображение информации о программе"""
        messagebox.showinfo(
            "О программе",
            "Тест на память\n\n"
            "Версия: 1.0\n"
            "Язык программирования: Python\n"
            "Графическая библиотека: Tkinter\n\n"
            "Программа предназначена для оценки "
            "способности пользователя запоминать числа."
        )

    def show_results(self):
        """Отображение итоговых результатов"""

        if self.test.attempts == 0:
            messagebox.showinfo(
                "Результаты",
                "Вы ещё не проходили тестирование."
            )
            return

        try:
            statistics = self.test.get_statistics()
            result_text = format_results(statistics)

            self.clear_screen()

            ttk.Label(
                self.content,
                text="Результаты тестирования",
                style="Title.TLabel"
            ).pack(pady=25)

            ttk.Label(
                self.content,
                text=result_text,
                font=("Arial", 13),
                justify="center"
            ).pack(pady=20)

            ttk.Button(
                self.content,
                text="Пройти тест снова",
                style="Primary.TButton",
                command=self.start_test
            ).pack(pady=10)

            ttk.Button(
                self.content,
                text="Главное меню",
                command=self.show_main_menu
            ).pack(pady=10)

        except Exception as error:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось отобразить результаты:\n{error}"
            )

    def close_application(self):
        """Безопасное завершение работы"""
        if messagebox.askyesno(
                "Выход",
                "Вы действительно хотите закрыть приложение?"
        ):
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

            self.root.destroy()

    def handle_callback_exception(
            self,
            exception_type,
            exception_value,
            traceback_object
    ):
        """Обработка непредвиденных ошибок интерфейса"""
        messagebox.showerror(
            "Ошибка приложения",
            f"Во время работы возникла ошибка:\n"
            f"{exception_value}\n\n"
            "Программа продолжит работу."
        )
