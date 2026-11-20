import tkinter as tk

from interface import MemoryApp


def main():
    """Запуск приложения"""
    try:
        root = tk.Tk()
        app = MemoryApp(root)
        root.mainloop()

    except Exception as error:
        print(f"Ошибка запуска приложения: {error}")


if __name__ == "__main__":
    main()