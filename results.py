def get_result_description(max_length):
    """Определение условной характеристики результата"""

    if max_length <= 3:
        return "Начальный уровень"
    elif max_length <= 5:
        return "Средний уровень"
    elif max_length <= 7:
        return "Хороший уровень"
    else:
        return "Высокий уровень"

def format_results(statistics):
    """Формирование итогового отчета о тесте"""

    correct = statistics["correct_answers"]
    errors = statistics["errors"]
    attempts = statistics["attempts"]
    max_length = statistics["max_length"]

    if attempts > 0:
        accuracy = round(correct / attempts * 100)
    else:
        accuracy = 0

    description = get_result_description(max_length)

    result_text = (
        "ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!\n\n"
        f"Правильных ответов: {correct}\n"
        f"Количество ошибок: {errors}\n"
        f"Всего попыток: {attempts}\n"
        f"Точность ответов: {accuracy}%\n"
        f"Максимальная длина числа: {max_length}\n\n"
        f"Результат: {description}"
    )

    return result_text
