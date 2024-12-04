import re
file_list = [
    'penis_1_1.png', 'penis_1_2.jpeg', 'penis_1_3.png', 'penis_1_4.png',
    'penis_1_5.png', 'penis_1_6.png', 'penis_1_7.png', 'penis_1_8.png',
    'penis_1_9.png', 'penis_1_10.png', 'penis_1_11.png', 'penis_1_12.png',
    'penis_1_13.png'
]

# Функция извлечения чисел для сортировки


def extract_numbers(filename):
    match = re.search(r'_(\d+)_(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0


# Сортируем список
sorted_files = sorted(file_list, key=extract_numbers)

print(sorted_files)
