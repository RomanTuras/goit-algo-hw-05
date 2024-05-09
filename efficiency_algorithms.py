import timeit

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# Завантаження текстових файлів
with open("1.txt", "r") as file:
    text1 = file.read()
with open("2.txt", "r") as file:
    text2 = file.read()

# Задання підрядків
existing_pattern_for_text_1 = "Жадібний алгоритм у цьому випадку полягає"
existing_pattern_for_text_2 = "визначена програма дослідження"
fictional_pattern = "Лорем іпсум долор сіт"

# Функції для вимірювання часу виконання алгоритмів
def measure_time(algorithm, text, pattern):
    start_time = timeit.default_timer()
    algorithm(text, pattern)
    return timeit.default_timer() - start_time

# Вимірюємо час виконання кожного алгоритму для обох текстів та обох підрядків
boyer_moore_time_1_existing = measure_time(boyer_moore, text1, existing_pattern_for_text_1)
kmp_time_1_existing = measure_time(kmp, text1, existing_pattern_for_text_1)
rabin_karp_time_1_existing = measure_time(rabin_karp, text1, existing_pattern_for_text_1)

boyer_moore_time_1_fictional = measure_time(boyer_moore, text1, fictional_pattern)
kmp_time_1_fictional = measure_time(kmp, text1, fictional_pattern)
rabin_karp_time_1_fictional = measure_time(rabin_karp, text1, fictional_pattern)

boyer_moore_time_2_existing = measure_time(boyer_moore, text2, existing_pattern_for_text_2)
kmp_time_2_existing = measure_time(kmp, text2, existing_pattern_for_text_2)
rabin_karp_time_2_existing = measure_time(rabin_karp, text2, existing_pattern_for_text_2)

boyer_moore_time_2_fictional = measure_time(boyer_moore, text2, fictional_pattern)
kmp_time_2_fictional = measure_time(kmp, text2, fictional_pattern)
rabin_karp_time_2_fictional = measure_time(rabin_karp, text2, fictional_pattern)

# Виводимо результати
print("1.txt - Існуючий підрядок:")
print("Боєра-Мура:", boyer_moore_time_1_existing)
print("Кнута-Морріса-Пратта:", kmp_time_1_existing)
print("Рабіна-Карпа:", rabin_karp_time_1_existing)

print("\n1.txt - Вигаданий підрядок:")
print("Боєра-Мура:", boyer_moore_time_1_fictional)
print("Кнута-Морріса-Пратта:", kmp_time_1_fictional)
print("Рабіна-Карпа:", rabin_karp_time_1_fictional)

print("\n2.txt - Існуючий підрядок:")
print("Боєра-Мура:", boyer_moore_time_2_existing)
print("Кнута-Морріса-Пратта:", kmp_time_2_existing)
print("Рабіна-Карпа:", rabin_karp_time_2_existing)

print("\n2.txt - Вигаданий підрядок:")
print("Боєра-Мура:", boyer_moore_time_2_fictional)
print("Кнута-Морріса-Пратта:", kmp_time_2_fictional)
print("Рабіна-Карпа:", rabin_karp_time_2_fictional)

bmt_med = (boyer_moore_time_1_existing + boyer_moore_time_1_fictional + boyer_moore_time_2_existing + boyer_moore_time_2_fictional)/4
kmp_med = (kmp_time_1_existing + kmp_time_1_fictional + kmp_time_2_existing + kmp_time_2_fictional)/4
rk_med = (rabin_karp_time_1_existing + rabin_karp_time_1_fictional + rabin_karp_time_2_existing + rabin_karp_time_2_fictional)/4

if bmt_med<kmp_med and bmt_med<rk_med:
    print("\nБоєра-Мура: найкращще рішення")
elif kmp_med<bmt_med and kmp_med<rk_med:
    print("\nКнута-Морріса-Пратта: найкращще рішення")
elif rk_med<bmt_med and rk_med<kmp_med:
    print("\nРабіна-Карпа: найкращще рішення")
