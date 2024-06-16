import os
import re
from collections import Counter, defaultdict


def process_file(filename):
    # Перевірка розширення файлу
    if not filename.endswith('.txt'):
        print("Я приймаю тільки файл з txt розширенням")
        return

    # Перевірка розміру файлу
    if os.path.getsize(filename) < 1 * 1024 * 1024:  # 1 МБ
        print("Я приймаю файли 1Мб або більше , додайте більше текст :)")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Фільтрація тексту
    filtered_content = re.sub(r'[^а-яА-ЯёЁ ]+', ' ', content)  # залишаємо тільки символи російської мови та пробіли
    filtered_content = re.sub(r'\s+', ' ', filtered_content)  # послідовність пробілів замінюємо на один пробіл
    filtered_content = filtered_content.lower()  # замінюємо прописні літери на стрічні

    # Створення Dash+filename.txt
    dash_filename = 'Dash-' + os.path.basename(filename)
    with open(dash_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_content)

    # Створення WithoutDash+filename.txt
    without_dash_filename = 'WithoutDash-' + os.path.basename(filename)
    filtered_content_no_spaces = filtered_content.replace(' ', '')
    with open(without_dash_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_content_no_spaces)

    print(f'Файли "{dash_filename}" та "{without_dash_filename}" створені.')

    # Обробка файлу Dash
    process_dash_file(dash_filename)
    # Обробка файлу WithoutDash
    process_without_dash_file(without_dash_filename)


def process_dash_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    total_chars = len(content)
    counter = Counter(content)
    frequencies = {char: count / total_chars for char, count in counter.items()}

    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)

    print(f'\nЗагальна кількість символів у тексті файлу {filename}: {total_chars}')
    print(f'Таблиця частот символів для файлу {filename}:\n')
    for char, freq in sorted_frequencies:
        print(f'Символ: {char} | Кількість: {counter[char]} | Частота: {freq:.5f}')

    # Підрахунок біграм
    dash_bigrams_with_cross, dash_total_bigrams_with_cross = count_bigrams(content, with_cross=True)
    dash_bigrams_without_cross, dash_total_bigrams_without_cross = count_bigrams(content, with_cross=False)

    print(f'\nЗагальна кількість біграм з перетином у файлі {filename}: {dash_total_bigrams_with_cross}')
    print(f'Матриця біграм з перетином для файлу {filename}:\n')
    print_bigram_matrix(dash_bigrams_with_cross)

    print(f'\nЗагальна кількість біграм без перетину у файлі {filename}: {dash_total_bigrams_without_cross}')
    print(f'Матриця біграм без перетину для файлу {filename}:\n')
    print_bigram_matrix(dash_bigrams_without_cross)


def process_without_dash_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    total_chars = len(content)
    counter = Counter(content)
    frequencies = {char: count / total_chars for char, count in counter.items()}

    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)

    print(f'\nЗагальна кількість символів у тексті файлу {filename}: {total_chars}')
    print(f'Таблиця частот символів для файлу {filename}:\n')
    for char, freq in sorted_frequencies:
        print(f'Символ: {char} | Кількість: {counter[char]} | Частота: {freq:.5f}')

    # Підрахунок біграм
    without_dash_bigrams_with_cross, without_dash_total_bigrams_with_cross = count_bigrams(content, with_cross=True)
    without_dash_bigrams_without_cross, without_dash_total_bigrams_without_cross = count_bigrams(content,
                                                                                                 with_cross=False)

    print(f'\nЗагальна кількість біграм з перетином у файлі {filename}: {without_dash_total_bigrams_with_cross}')
    print(f'Матриця біграм з перетином для файлу {filename}:\n')
    print_bigram_matrix(without_dash_bigrams_with_cross)

    print(f'\nЗагальна кількість біграм без перетину у файлі {filename}: {without_dash_total_bigrams_without_cross}')
    print(f'Матриця біграм без перетину для файлу {filename}:\n')
    print_bigram_matrix(without_dash_bigrams_without_cross)


def count_bigrams(text, with_cross=True):
    bigram_counter = defaultdict(int)
    total_bigrams = 0
    step = 1 if with_cross else 2

    for i in range(0, len(text) - 1, step):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigram_counter[bigram] += 1
            total_bigrams += 1

    # Підрахунок ймовірностей
    bigram_frequencies = {bigram: count / total_bigrams for bigram, count in bigram_counter.items()}

    return bigram_frequencies, total_bigrams


def print_bigram_matrix(bigram_frequencies):
    alphabet = list(' абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    size = len(alphabet)
    matrix = [[0.0] * size for _ in range(size)]

    for bigram, freq in bigram_frequencies.items():
        first_char, second_char = bigram
        i = alphabet.index(first_char)
        j = alphabet.index(second_char)
        matrix[i][j] = freq

    print('  ' + ' '.join(alphabet))
    for i, row in enumerate(matrix):
        print(alphabet[i] + ' ' + ' '.join(f'{cell:.5f}' for cell in row))


if __name__ == "__main__":
    filename = input("Введіть шлях до вхідного файлу: ")
    process_file(filename)
