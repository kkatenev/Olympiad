import json
from datetime import datetime


with open('results_RUN.txt', 'r', encoding='utf-8') as results_file:
    results_data = results_file.readlines()


results = {}


for result_line in results_data:
    result_parts = result_line.strip().split()
    number = int(result_parts[0])
    action = result_parts[1]
    time_str = result_parts[2]

    if number not in results:
        results[number] = {'start_time': None, 'finish_time': None}

    time = datetime.strptime(time_str, '%H:%M:%S,%f')
    if action == 'start':
        results[number]['start_time'] = time
    elif action == 'finish':
        results[number]['finish_time'] = time


with open('competitors2.json', 'r', encoding='utf-8') as competitors_file:
    competitors_data = json.load(competitors_file)


sorted_results = sorted(results.items(), key=lambda x: (x[1]['finish_time'] - x[1]['start_time']).total_seconds())


table_rows = []
for place, (number, times) in enumerate(sorted_results, start=1):
    if str(number) in competitors_data:
        first_name = competitors_data[str(number)]['Name']
        last_name = competitors_data[str(number)]['Surname']
        result_time = times['finish_time'] - times['start_time']
        formatted_time = '{:02d}:{:02d}.{:06d}'.format(
            result_time.seconds // 60, result_time.seconds % 60, result_time.microseconds)
        table_rows.append([place, number, first_name, last_name, formatted_time])


print('-----------------------------------------------------------------------------')
print('| Занятое место  | Нагрудный номер |    Имя     |  Фамилия   |  Результат   |')
print('-----------------------------------------------------------------------------')
for row in table_rows:
    print('|{:>15} |{:>16} |{:>11} |{:>11} |{:>10}  |'.format(*row))
print('-----------------------------------------------------------------------------')
