import pycat
# информация о pytest:
# https://practicum.yandex.ru/blog/pytest-testirovanie-prilozhenij-na-python/    

def test_numbering_empty_list():
    assert pycat.numbering([]) == []

def test_numbering_single_element():
    assert pycat.numbering(['single line']) == ['1: single line\n']

def test_numbering_multiple_elements():
    assert pycat.numbering(['first line', 'second line', 'third line']) == [
        '1: first line\n',
        '2: second line\n',
        '3: third line\n'
    ]

def test_numbering_leading_trailing_spaces():
    assert pycat.numbering(['  first line  ', '  second line  ']) == [
        '1: first line\n',
        '2: second line\n'
    ]

def test_numbering_special_characters():
    assert pycat.numbering(['line with special chars @#$%', 'another line!']) == [
        '1: line with special chars @#$%\n',
        '2: another line!\n'
    ]

def test_numbering_long_lines():
    long_line = 'a' * 1000  # строка из 1000 символов 'a'
    assert pycat.numbering([long_line]) == [f'1: {long_line}\n']

def test_numbering_numbers_in_lines():
    assert pycat.numbering(['line 1', 'line 2', 'line 3']) == [
        '1: line 1\n',
        '2: line 2\n',
        '3: line 3\n'
    ]

def test_numbering_mixed_content():
    assert pycat.numbering(['Hello World!', '', 'Line with numbers 123', 'Last line.']) == [
        '1: Hello World!\n',
        '2: \n',
        '3: Line with numbers 123\n',
        '4: Last line.\n'
    ]
