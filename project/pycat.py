'''
    Модуль содержит функции, реализующие  аналог команды "cat" (Linux)
    functions:
        printer     - выводит в указанный поток вывода список строк в отсортированном или нет виде
        reader      - читает содержимое потока ввода и возвращает в виде списка строк
        numbering   - принимает список строк и возвращает список пронумерованных строк списка
        numbering_nonblank - принимает список строк и возвращает список пронумерованных непустых строк списка
        help_out    - формирует справку по работе с программой и передает ее в функцию вывода (printer)
        pycat       - считывает аргументы командной строки и выводит указанное содержимое в файл или в консоль 
'''
import os
import sys

def printer(output: list, out_file: str = '', method: str = '', out_style: str = ''):
    '''
        Функция выводит в стандартный поток вывода или в указанный файл содержимое переданного списка строк 

        Args:
            output (list): список строк выводимого содержимого.
            out_file (str): файл, в который выводится содержимое или стандартный вывод, если пусто
            method (str): метод вывода: '>' новый файл, '>>' дописать в существующий
            out_style (str): стиль вывода: 'sort' - отсортированные строки
        Returns: 
            None: Выводит содержимое в стандартный поток вывода или в файл
    '''
    if out_style == '--asc':
        output = ''.join(sorted(output))
    elif out_style == '--desc':    
        output = ''.join(sorted(output, reverse = True))
    else:
        output = ''.join(output)    
    
    if not out_file:
        print(output)
    else:
        if method == '>':
            with open(out_file,'w') as f:
                f.write(output)
        elif method == '>>':
            with open(out_file,'a') as f:
                f.write(output)

def reader(path: str, method: str = '') -> list:
    '''
        Функция читает содержимое файла или каталога или стандартного ввода и возвращает его в виде str
        Args:
            path (str): имя файла или каталога - содержимое которого необходимо считать. 
            method (str): метод чтения - если пусто, то чтение из файла или каталога, если "stdin", то из стандартного потока ввода
        Returns:
            list: содержимое файла или каталога или стандартного потока ввода в виде списка строк
    '''
    if not method and path:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as file:
                return file.readlines()
        content = os.listdir(path)
    else:
        content = sys.stdin.readlines()
    return content

def numbering(content: list) -> list:
    '''
        Функция возвращает нумерованное содержимое списка строк в виде списка строк
        Args:
            content (list): список строк, которые необходимо пронумеровать
        Returns:
            list: список пронумерованных строк содержимого
    '''
    return [f"{i+1}: {line.strip()}\n" for i, line in enumerate(content)]

def numbering_nonblank(content: list) -> list:
    '''
        Функция возвращает нумерованное содержимое списка строк в виде списка строк
        Args:
            content (list): список строк, которые необходимо пронумеровать (только непустые)
        Returns:
            list: список пронумерованных строк содержимого. Нумеруются только непустые строки
    '''
    newcont = []
    for i, line in enumerate(content):
        if line.strip():
            newcont += [f'{i+1}:  {line.strip()}\n']
        else:
            newcont += ['\n']
    return newcont

def help_out(out_file: str = '', method: str =''):
    '''
        Функция выводит справку по использованию pycat
        Args:
            out_file (str): строка: имя файла или пустая. Определяет поток вывода
            method (str): строка: метод вывода: '>' новый файл, '>>' дописать в существующий
        Returns: 
            none:  выводит содержимое в стандартный поток вывода
    '''
    help_str = ''
    """
        The function implements an analog of the cat command in Linux

        USAGE: cat [OPTIONS]... [FILES]...
        Concatenate content of FILES and print on the output stream: stdout or file.
        OPTIONS:
            -n, --number            : Number lines
            -b, --number-nonblank   : Number non-empty output lines, overrides -n
            -s, --squezze-blank     : Suppress repeated empty output lines
            -E, --show-ends         : Display $ at end of each line
            -T, --show-tabs         : Display TAB characters as ^I
            --asc                   : Alphabetically ascending sort the output content lines
            --desc                  : Alphabetically descending sort the output content lines
            ->                      : redirect output stream to file. Replace information in a file 
            ->>                     : redirect output stream to file. Add information to the end of file 
        """
    printer(help_str, out_file, method)


def pycat():
    """
        Функция реализует аналог команды "cat" (Linux)
        Соединяет содержимое файлов и выводит в стандартный поток вывода или перенаправляет вывод в файл.
        Запуск в консоли: python pycat.py [OPTIONS] [FILES] ...
            OPTIONS:
                -n, --number            : Number lines
                -b, --number-nonblank   : Number non-empty output lines, overrides -n
                -s, --squezze-blank     : Suppress repeated empty output lines
                -E, --show-ends         : Display $ at end of each line
                -T, --show-tabs         : Display TAB characters as ^I    arguments_list = sys.argv[1:]
                --asc                   : Alphabetically ascending sort the output content lines
                --desc                  : Alphabetically descending sort the output content lines
                ->                      : redirect output stream to file. Replace information in a file 
                ->>                     : redirect output stream to file. Add information to the end of file 
            FILES:
                    Список имен файлов или каталогов (через пробел), содержимое которых необходимо соединить.
                    Если файлы не указаны, то ввод строк из стандартного потока ввода
        Args:
            (list):  список аргументов командной строки
        Returns:
            str: вывод в стандартный поток вывода или в файл
    """
    arguments_list = sys.argv[1:]   # считываем аргументы командной строки
    methods_list = []
    files_list = []
    methods = ['--help', '-n', '-b', '-T', '-s', '-E', '-A', '-v', '--number', '--number-nonblank', '--squeezed-blank', '--show-ends', '--show-tabs', '--show-all', '--show-nonprinting', '--asc', '--desc']
    collecting_options = True
    fl_out = 'stdout'
    out_file = ''
    out_method = ''
    out_style = ''
    for prop in arguments_list:
        if prop == '->' or prop == '->>':
            fl_out = 'file'
            out_method = prop.replace('-','')
        elif fl_out == 'file':
            out_file = prop            
        elif prop[0]=='-' and prop in methods:
            methods_list.append(prop)
        elif os.path.isfile(prop) or os.path.isdir(prop):
            collecting_options = False
            files_list.append(prop)
        else:
            if collecting_options:
                printer(prop)
                return
            else:
                printer(f"Warning: '{prop}' is not a valid file.")
                return

    if len(methods_list) == 0 and len(files_list) == 0:
        content = reader('', 'stdin')         # ввод из стандартного потока ввода
        printer(content, out_file, out_method)
    elif len(methods_list) == 0:
        for file in files_list:
            printer(reader(file, ''), out_file, out_method)    # ввод из стандартного потока ввода
    elif len(methods_list) == 1 and methods_list[0] == '--help' and len(files_list) == 0:
        help_out(out_file, out_method)
        return
   
    out_content = []
    for file in files_list:     # считываем все строки из файлов
        out_content += reader(file)
   
    if len(out_content) == 0:    # ввод из стандартного потока ввода
        out_content = reader('','stdin')
    
    for m in methods_list:      # применяем методы обработки к потоку ввода 
        if m == '--number' or m == '-n':
            out_content = numbering(out_content)
        elif m == '--number-nonblank' or m == '-b':
            out_content = numbering_nonblank(out_content)
        elif m == '--squeezed-blank' or m == '-s':
            out_content = [i.replace('\n\n', '\n') for i in out_content]
        elif m == '--show-ends' or m == '-E':
            out_content = [i.replace('\n', '\n$') for i in out_content]
        elif m == '--show-tabs' or m == '-T':
            out_content = [i.replace('\t', '^I') for i in out_content]
        if m == '--asc' or m == '--desc':
            out_style = m
    printer(out_content,out_file, out_method, out_style)
            
if __name__ == "__main__":
    pycat()





