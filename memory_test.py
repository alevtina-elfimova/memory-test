import random

class MemoryTest:
    """Класс с логикой тестирования памяти"""

    def __init__(self, max_errors=3, initial_length=3):
        """Инициализация параметров"""
        self.max_errors = max_errors
        self.initial_length = initial_length
        self.reset()

    def reset(self):
        """Сброс результатов перед новым тестированием"""
        self.current_length = self.initial_length
        self.correct_answers = 0
        self.errors = 0
        self.attempts = 0
        self.max_length = 0
        self.current_sequence = ""
        self.finished = False

    def generate_sequence(self):
        """Создание случайной последовательности цифр"""
        if self.finished:
            return ""
        self.current_sequence = "".join(
            random.choices("0123456789", k=self.current_length)
        )

        self.max_length = max(
            self.max_length,
            self.current_length
        )

        return self.current_sequence

    def check_answer(self, answer):
        """Проверка ответов пользователя"""
        if self.finished or not self.current_sequence:
            return {
                "correct": False,
                "finished": self.finished
            }

        self.attempts += 1

        is_correct = answer == self.current_sequence

        if is_correct:
            self.correct_answers += 1
            self.current_length += 1
        else:
            self.errors += 1

        self.current_sequence = ""

        if self.errors >= self.max_errors:
            self.finished = True

        return {
            "correct": is_correct,
            "finished": self.finished
        }

    def get_statistics(self):
        """Статистика прохождения теста"""
        return {
            "correct_answers": self.correct_answers,
            "errors": self.errors,
            "attempts": self.attempts,
            "max_length": self.max_length,
            "max_errors": self.max_errors
        }
