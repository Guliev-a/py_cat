
import pycat
import os

def test_reader_non_empty_file():
    with open('test_file.txt', 'w') as f:
        f.write('This is a test line.\nAnother line.')

    assert len(pycat.reader('test_file.txt')) > 0

    os.remove('test_file.txt')

def test_reader_empty_file():
    with open('empty_file.txt', 'w') as f:
        pass

    assert pycat.reader('empty_file.txt') == []

    os.remove('empty_file.txt')

def test_reader_non_existent_file():
    try:
        pycat.reader('non_existent_file.txt')
        assert False, "Expected an exception for a non-existent file."
    except FileNotFoundError:
        assert True  
def test_reader_file_with_special_characters():
    with open('special_char_file.txt', 'w') as f:
        f.write('Line with special characters: @#$%^&*()\nAnother line!')

    lines = pycat.reader('special_char_file.txt')
    assert len(lines) > 0
    assert lines[0] == 'Line with special characters: @#$%^&*()\n'
    
    os.remove('special_char_file.txt')

def test_reader_large_file():
    with open('large_file.txt', 'w') as f:
        for i in range(1000):
            f.write(f'This is line {i}\n')

    lines = pycat.reader('large_file.txt')
    assert len(lines) == 1000

    os.remove('large_file.txt')