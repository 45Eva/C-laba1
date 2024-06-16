import os
import re


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


if __name__ == "__main__":
    filename = input("Введіть шлях до вхідного файлу: ")
    process_file(filename)
