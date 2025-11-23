import sys
import csv
import argparse
from collections import defaultdict
from tabulate import tabulate


#весь список
all_array = []

#позиции заголовков
performance_pos = 0
position_pos = 0

def read_csv(filename) :

    global position_pos
    global performance_pos

    # 1. Открываем CSV-файл
    with open(filename, mode='r', encoding='utf-8') as file:
        global all_array
        # 2. Создаем объект reader для чтения данных
        csv_reader = csv.reader(file)

    # 3. Преобразуем данные в список
        data_array = [row for row in csv_reader]
	#получаем координаты
        for i, row in enumerate(data_array[0]):
            row = str(row.strip())
            if (row=='performance'):
                performance_pos = i
            if (row=='position'):
                position_pos = i

        #удаляем первую строку
        data_array.pop(0)

        #Объединяем массив с предыдущим
        all_array = all_array+data_array


def make_report(report):

    positions = []

    for row in all_array:
        row[position_pos].strip()
        positions.append({"position":row[position_pos],"performance":float(row[performance_pos])})

    # Подсчёт количества и суммы performance для каждого наименования
    counts = defaultdict(int)
    sum_perf = defaultdict(float)
    for item in positions:
        counts[item["position"]] += 1
        sum_perf[item["position"]] += item["performance"]

    # Формируем отчёт: позиция, средняя performance
    report_ = [
            ['', name, round(sum_perf[name] / counts[name], 2)]
        for name in counts
    ]

    #Сортировка по возрастанию
    sorted_report = sorted(report_, key=lambda x: x[2], reverse=True)
    #Добавляем левую колонку
    for i, item in enumerate(sorted_report):
        item[0] = i+1
    #Формируем заголовок
    header = ["position",report]
    print(tabulate(sorted_report, headers=header, tablefmt='grid'))

def read_and_print_files(filenames,report):
    for filename in filenames:
        #оставляем позиции только нужного формата
        if ".csv" in filename:
            try:
                read_csv(filename)
            except FileNotFoundError:
                print(f"Ошибка: файл '{filename}' не найден.")
            except Exception as e:
                print(f"Ошибка при чтении файла '{filename}': {e}")
        elif ".txt" in filename or ".xls" in filename:
            print("Требуются файлы только csv формата")
    if len(all_array) == 0:
        print("Нужно указать как минимум один файл формата .csv")
        sys.exit()

    make_report(report)

#Для тестов логику обработки аргументов обернули отдельной функцией
def main():
    parser = argparse.ArgumentParser(description='Обработка csv файлов')
    parser.add_argument('--files', nargs = '+', required = True, default=[],  help='Список файлов')
    parser.add_argument('--report', type=str, default = 'performance', help='Наименование отчета')
    args = parser.parse_args()
    read_and_print_files(args.files,args.report)


if __name__ == "__main__":
    main()



