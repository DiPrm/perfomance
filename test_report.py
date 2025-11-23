import pytest
from report import read_and_print_files
from unittest.mock import patch
import sys

# Тест, проверяющий, что функция всегда отрабатывает без ошибок
def test_read_and_print_files_no_errors(capsys):
    test_cases = [
        (["example1.csv", "example2.csv","example3.csv"],"performance"),  # Обычный случай
        (["example1.csv", "example2.csv","example3.txt"],"performance"),  # Один из файлов имеет не корректный формат
        ([],"performance"),  # Пустое имя и пустой список файлов
        ( ["file1.txt"],"performance"),  # Один файл
        ( ["a", "b", "c"],"123"),  # Числовое имя и несуществующие файлы
    ]

    for files, report in test_cases:
        try:
            # Проверяем, что функция что-то вывела в консоль
            read_and_print_files(files, report)
            captured = capsys.readouterr()
            output_lines = captured.out.strip().split('\n')
            assert len(output_lines) > 4  # Если результат содержит строки больше 4, то фунция работает корректно
        except Exception as e:
            pytest.fail(f"Функция выбросила исключение для {report}, {files}: {e}")

# Тест для проверки обязательных аргументов
def test_required_arguments():
    #sys.exit()
    test_args = ["report.py"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as e:
            from report import main
            main()
        assert e.type == SystemExit
        assert e.value.code != 0